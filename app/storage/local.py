"""
Local File System Storage Provider Implementation.
Persists files to local disk under date-partitioned directory structure (YYYY/MM/DD).
Enforces path traversal safeguards.
"""

import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from app.core.config import settings
from app.core.exceptions import ValidationAppException
from app.core.logging import logger
from app.storage.base import StorageProvider


class LocalStorageProvider(StorageProvider):
    """Concrete StorageProvider persisting files to local file system."""

    def __init__(self, base_directory: Optional[str] = None):
        if base_directory:
            self.base_dir = os.path.abspath(base_directory)
        else:
            self.base_dir = os.path.abspath(settings.STORAGE_LOCAL_DIR)
        
        os.makedirs(self.base_dir, exist_ok=True)

    def _validate_path_safety(self, absolute_path: str) -> None:
        """
        Validates that target absolute path is strictly contained within storage base directory.
        Prevents directory traversal attacks (e.g. '../../etc/passwd').
        """
        resolved_path = os.path.abspath(absolute_path)
        common = os.path.commonpath([self.base_dir, resolved_path])
        if common != self.base_dir:
            logger.security_warning = True
            logger.error(f"Path traversal detected! Attempted path: {resolved_path} outside base: {self.base_dir}")
            raise ValidationAppException("Access denied: Invalid file path")

    def generate_unique_filename(self, original_filename: str) -> str:
        """Generates UUID-v4 based unique filename retaining extension."""
        ext = Path(original_filename).suffix.lower()
        unique_id = uuid.uuid4().hex
        return f"{unique_id}{ext}"

    def _get_date_partition(self) -> str:
        """Returns relative date partition string: YYYY/MM/DD."""
        now = datetime.now(timezone.utc)
        return os.path.join("uploads", now.strftime("%Y"), now.strftime("%m"), now.strftime("%d"))

    def get_absolute_path(self, relative_path: str) -> str:
        """Resolves absolute path from relative path and validates path safety."""
        # Normalize relative path separators
        clean_rel = os.path.normpath(relative_path).lstrip("/\\")
        abs_path = os.path.abspath(os.path.join(self.base_dir, clean_rel))
        self._validate_path_safety(abs_path)
        return abs_path

    def get_relative_path(self, absolute_path: str) -> str:
        """Converts absolute path to storage-root relative path."""
        self._validate_path_safety(absolute_path)
        rel_path = os.path.relpath(absolute_path, self.base_dir)
        return rel_path.replace("\\", "/")

    async def save(self, content: bytes, original_filename: str, subfolder: str = "") -> tuple[str, str, str]:
        """
        Saves file content to date-partitioned directory on disk.
        
        :return: Tuple of (stored_filename, relative_path, absolute_path)
        """
        stored_filename = self.generate_unique_filename(original_filename)
        
        if not subfolder:
            date_dir = self._get_date_partition()
        else:
            date_dir = subfolder.strip("/\\")

        target_dir_abs = os.path.abspath(os.path.join(self.base_dir, date_dir))
        self._validate_path_safety(target_dir_abs)
        os.makedirs(target_dir_abs, exist_ok=True)

        abs_path = os.path.join(target_dir_abs, stored_filename)
        self._validate_path_safety(abs_path)

        with open(abs_path, "wb") as f:
            f.write(content)

        rel_path = self.get_relative_path(abs_path)
        logger.info(f"File stored successfully: {rel_path} ({len(content)} bytes)")

        return stored_filename, rel_path, abs_path

    async def read(self, relative_path: str) -> bytes:
        """Reads file binary data from disk."""
        abs_path = self.get_absolute_path(relative_path)
        if not os.path.isfile(abs_path):
            raise ValidationAppException("Requested file does not exist on disk")

        with open(abs_path, "rb") as f:
            return f.read()

    async def delete(self, relative_path: str) -> bool:
        """Deletes file from disk if present."""
        try:
            abs_path = self.get_absolute_path(relative_path)
            if os.path.isfile(abs_path):
                os.remove(abs_path)
                logger.info(f"File deleted from storage: {relative_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file '{relative_path}': {str(e)}")
            return False

    async def exists(self, relative_path: str) -> bool:
        """Checks if file exists on disk."""
        try:
            abs_path = self.get_absolute_path(relative_path)
            return os.path.isfile(abs_path)
        except Exception:
            return False
