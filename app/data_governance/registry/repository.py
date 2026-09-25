"""Data Asset Repository (Phase 8B).

Provides tenant-isolated persistence and querying for governed data assets.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from app.data_governance.registry.models import DataAsset, AssetLifecycleState, ClassificationLevel, AssetType


class DataAssetRepository:
    """In-memory tenant-isolated data asset repository."""

    def __init__(self):
        # org_id -> (asset_id -> DataAsset)
        self._assets: Dict[str, Dict[str, DataAsset]] = {}

    def save(self, asset: DataAsset) -> DataAsset:
        """Store or update a governed asset."""
        if asset.organization_id not in self._assets:
            self._assets[asset.organization_id] = {}
        self._assets[asset.organization_id][asset.asset_id] = asset
        return asset

    def get_by_id(self, asset_id: str, organization_id: str) -> Optional[DataAsset]:
        """Retrieve asset with strict organization isolation."""
        return self._assets.get(organization_id, {}).get(asset_id)

    def list_assets(
        self,
        organization_id: str,
        workspace_id: Optional[str] = None,
        asset_type: Optional[AssetType] = None,
        classification: Optional[ClassificationLevel] = None,
        status: Optional[AssetLifecycleState] = None,
    ) -> List[DataAsset]:
        """List assets matching filter criteria."""
        org_assets = list(self._assets.get(organization_id, {}).values())
        results = org_assets

        if workspace_id:
            results = [a for a in results if a.workspace_id == workspace_id]
        if asset_type:
            results = [a for a in results if a.asset_type == asset_type]
        if classification:
            results = [a for a in results if a.classification == classification]
        if status:
            results = [a for a in results if a.status == status]

        return results

    def delete(self, asset_id: str, organization_id: str) -> bool:
        """Remove asset from active storage."""
        if organization_id in self._assets and asset_id in self._assets[organization_id]:
            del self._assets[organization_id][asset_id]
            return True
        return False
