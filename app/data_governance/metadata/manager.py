"""Metadata Management Platform (Phase 8B)."""

from __future__ import annotations

from typing import Dict, Optional
from app.data_governance.metadata.schemas import ComprehensiveAssetMetadata


class MetadataManager:
    """Central manager for governed asset metadata."""

    def __init__(self):
        # asset_id -> ComprehensiveAssetMetadata
        self._metadata_store: Dict[str, ComprehensiveAssetMetadata] = {}

    def set_metadata(self, metadata: ComprehensiveAssetMetadata) -> ComprehensiveAssetMetadata:
        """Store or update asset metadata."""
        self._metadata_store[metadata.asset_id] = metadata
        return metadata

    def get_metadata(self, asset_id: str) -> Optional[ComprehensiveAssetMetadata]:
        """Retrieve 4D metadata container for asset."""
        return self._metadata_store.get(asset_id)
