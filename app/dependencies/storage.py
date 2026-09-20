"""
Storage Provider FastAPI Dependency Injector.
Provides singleton instance of LocalStorageProvider.
"""

from app.storage.base import StorageProvider
from app.storage.local import LocalStorageProvider

_storage_provider_instance: StorageProvider = LocalStorageProvider()


def get_storage_provider() -> StorageProvider:
    """Provides active StorageProvider implementation instance."""
    return _storage_provider_instance
