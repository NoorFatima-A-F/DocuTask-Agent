"""S3-compatible object storage (AWS S3, Cloudflare R2, MinIO, Backblaze B2 ...).

Lets the API and the Celery worker run on different machines: both read and write the
same bucket. Credentials come from the standard AWS chain (``AWS_ACCESS_KEY_ID`` /
``AWS_SECRET_ACCESS_KEY`` env vars, instance role, ...); they are never stored in settings.

boto3 is synchronous, so every call runs in a worker thread.
"""

from __future__ import annotations

import asyncio
import mimetypes
import uuid
from datetime import UTC, datetime
from pathlib import PurePosixPath
from typing import Any

from app.core.exceptions import ValidationAppException
from app.core.logging import logger
from app.storage.base import StorageProvider

_MISSING_CODES = frozenset({"404", "NoSuchKey", "NotFound"})


def _error_code(exc: Exception) -> str:
    response = getattr(exc, "response", None) or {}
    return str(response.get("Error", {}).get("Code", ""))


class S3StorageProvider(StorageProvider):
    def __init__(
        self,
        bucket: str,
        prefix: str = "documents/",
        *,
        endpoint_url: str | None = None,
        region: str | None = None,
        client: Any = None,
    ):
        if not bucket:
            raise ValueError("S3 bucket name is required")
        self.bucket = bucket
        self.prefix = prefix.strip("/") + "/" if prefix.strip("/") else ""
        if client is None:
            import boto3

            client = boto3.client("s3", endpoint_url=endpoint_url or None, region_name=region or None)
        self.client = client

    def generate_unique_filename(self, original_filename: str) -> str:
        return f"{uuid.uuid4().hex}{PurePosixPath(original_filename).suffix.lower()}"

    def _key(self, relative_path: str) -> str:
        """Validate a key from the database: it must live under our prefix and not traverse."""
        key = relative_path.replace("\\", "/")
        if not key.startswith(self.prefix) or ".." in PurePosixPath(key).parts or key.startswith("/"):
            raise ValidationAppException("Access denied: Invalid file path")
        return key

    async def save(self, content: bytes, original_filename: str, subfolder: str = "") -> tuple[str, str, str]:
        stored = self.generate_unique_filename(original_filename)
        folder = subfolder.strip("/\\") if subfolder else datetime.now(UTC).strftime("%Y/%m/%d")
        key = self._key(f"{self.prefix}{folder}/{stored}")
        content_type = mimetypes.guess_type(original_filename)[0] or "application/octet-stream"
        await asyncio.to_thread(
            self.client.put_object,
            Bucket=self.bucket,
            Key=key,
            Body=content,
            ContentType=content_type,
            ServerSideEncryption="AES256",
        )
        logger.info("Stored s3://%s/%s (%d bytes)", self.bucket, key, len(content))
        return stored, key, f"s3://{self.bucket}/{key}"

    async def read(self, relative_path: str) -> bytes:
        key = self._key(relative_path)
        try:
            response = await asyncio.to_thread(self.client.get_object, Bucket=self.bucket, Key=key)
        except Exception as exc:
            if _error_code(exc) in _MISSING_CODES:
                raise ValidationAppException("Requested file does not exist on disk") from exc
            raise
        body: bytes = await asyncio.to_thread(response["Body"].read)
        return body

    async def exists(self, relative_path: str) -> bool:
        try:
            key = self._key(relative_path)
            await asyncio.to_thread(self.client.head_object, Bucket=self.bucket, Key=key)
            return True
        except ValidationAppException:
            return False
        except Exception as exc:
            if _error_code(exc) in _MISSING_CODES:
                return False
            raise

    async def delete(self, relative_path: str) -> bool:
        try:
            if not await self.exists(relative_path):
                return False
            await asyncio.to_thread(self.client.delete_object, Bucket=self.bucket, Key=self._key(relative_path))
            return True
        except Exception as exc:
            logger.error("Failed to delete s3 object %s: %s", relative_path, type(exc).__name__)
            return False

    async def check(self) -> str | None:
        try:
            await asyncio.to_thread(self.client.head_bucket, Bucket=self.bucket)
        except Exception as exc:
            return f"bucket {self.bucket!r} not reachable ({_error_code(exc) or type(exc).__name__})"
        return None
