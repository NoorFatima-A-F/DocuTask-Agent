"""In-memory stand-in for a boto3 S3 client. Lives in tests/ only; never imported by app/.

Implements the calls S3StorageProvider makes and raises botocore's real ClientError with
the same error codes S3 returns.
"""

from __future__ import annotations

import io
from typing import Any

from botocore.exceptions import ClientError


def _error(code: str, op: str) -> ClientError:
    return ClientError({"Error": {"Code": code, "Message": code}}, op)


class FakeS3Client:
    def __init__(self, buckets: tuple[str, ...] = ("docs",)):
        self.objects: dict[tuple[str, str], dict[str, Any]] = {}
        self.buckets = set(buckets)

    def _bucket(self, bucket: str, op: str) -> None:
        if bucket not in self.buckets:
            raise _error("NoSuchBucket", op)

    def put_object(self, *, Bucket: str, Key: str, Body: bytes, **extra: Any) -> dict[str, Any]:
        self._bucket(Bucket, "PutObject")
        self.objects[(Bucket, Key)] = {"Body": bytes(Body), **extra}
        return {}

    def get_object(self, *, Bucket: str, Key: str) -> dict[str, Any]:
        self._bucket(Bucket, "GetObject")
        if (Bucket, Key) not in self.objects:
            raise _error("NoSuchKey", "GetObject")
        return {"Body": io.BytesIO(self.objects[(Bucket, Key)]["Body"])}

    def head_object(self, *, Bucket: str, Key: str) -> dict[str, Any]:
        if Bucket not in self.buckets or (Bucket, Key) not in self.objects:
            raise _error("404", "HeadObject")
        return {}

    def delete_object(self, *, Bucket: str, Key: str) -> dict[str, Any]:
        self.objects.pop((Bucket, Key), None)
        return {}

    def head_bucket(self, *, Bucket: str) -> dict[str, Any]:
        if Bucket not in self.buckets:
            raise _error("404", "HeadBucket")
        return {}
