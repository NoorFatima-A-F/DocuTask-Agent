"""Storage provider selection (``STORAGE_BACKEND``). The API and the worker both use this."""

from functools import lru_cache

from app.core.config import settings
from app.storage.base import StorageProvider


def build_storage_provider() -> StorageProvider:
    """A new provider for the configured backend."""
    if settings.STORAGE_BACKEND == "s3":
        from app.storage.s3 import S3StorageProvider

        return S3StorageProvider(
            bucket=settings.S3_BUCKET or "",
            prefix=settings.S3_PREFIX,
            endpoint_url=settings.S3_ENDPOINT_URL,
            region=settings.S3_REGION,
        )
    from app.storage.local import LocalStorageProvider

    return LocalStorageProvider()


@lru_cache(maxsize=1)
def get_storage_provider() -> StorageProvider:
    """Process-wide provider for request handlers. Tests override this dependency."""
    return build_storage_provider()
