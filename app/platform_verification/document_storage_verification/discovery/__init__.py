"""
Discovery package for Document Storage Verification.
"""
from app.platform_verification.document_storage_verification.discovery.storage_inventory_engine import (
    StorageInventoryEngine,
)
from app.platform_verification.document_storage_verification.discovery.storage_classification_engine import (
    StorageClassificationEngine,
)

__all__ = [
    "StorageInventoryEngine",
    "StorageClassificationEngine",
]
