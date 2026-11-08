"""Storage interface for uploaded documents (local disk or S3-compatible object storage)."""

from abc import ABC, abstractmethod


class StorageProvider(ABC):
    """Where uploaded files live. The API and the worker must use the same backend."""

    @abstractmethod
    async def save(self, content: bytes, original_filename: str, subfolder: str = "") -> tuple[str, str, str]:
        """Store ``content``; return ``(stored_filename, relative_path, location)``.

        ``relative_path`` is the key used for every later call; ``location`` is informational
        (an absolute path or an ``s3://`` URI).
        """

    @abstractmethod
    async def read(self, relative_path: str) -> bytes:
        """Return the stored bytes. Raises ``ValidationAppException`` if the file does not exist."""

    @abstractmethod
    async def delete(self, relative_path: str) -> bool:
        """Delete the file; return False if it did not exist or could not be deleted."""

    @abstractmethod
    async def exists(self, relative_path: str) -> bool:
        """Whether a file is stored under ``relative_path``."""

    @abstractmethod
    def generate_unique_filename(self, original_filename: str) -> str:
        """Collision-resistant filename keeping the extension."""

    @abstractmethod
    async def check(self) -> str | None:
        """Readiness: ``None`` when usable, otherwise a short reason."""
