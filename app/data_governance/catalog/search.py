"""Enterprise Data Catalog Search Engine (Phase 8B)."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.data_governance.registry.models import DataAsset, ClassificationLevel, AssetType
from app.data_governance.registry.repository import DataAssetRepository
from app.data_governance.catalog.indexing import CatalogIndex


class CatalogSearchResult(BaseModel):
    """Catalog search response item."""
    asset_id: str
    name: str
    asset_type: AssetType
    classification: ClassificationLevel
    department: str
    owner_user_id: str
    source: str
    compliance_tags: List[str]
    is_legal_hold: bool


class EnterpriseDataCatalog:
    """Searchable Enterprise Data Catalog."""

    def __init__(self, repository: DataAssetRepository, index: Optional[CatalogIndex] = None):
        self.repository = repository
        self.index = index or CatalogIndex()

    def index_all(self, organization_id: str) -> int:
        """Reindex all assets for an organization."""
        assets = self.repository.list_assets(organization_id)
        for asset in assets:
            self.index.index_asset(asset)
        return len(assets)

    def search(
        self,
        organization_id: str,
        query: Optional[str] = None,
        classification: Optional[ClassificationLevel] = None,
        asset_type: Optional[AssetType] = None,
        department: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> List[CatalogSearchResult]:
        """Perform faceted keyword search across governed assets."""
        org_assets = self.repository.list_assets(
            organization_id=organization_id,
            asset_type=asset_type,
            classification=classification,
        )

        matching_ids = None
        if query:
            matching_ids = self.index.search_keywords(query)

        results: List[CatalogSearchResult] = []
        for asset in org_assets:
            if matching_ids is not None and asset.asset_id not in matching_ids:
                # Also check direct name match if index didn't pick up
                if query.lower() not in asset.name.lower():
                    continue

            if department and asset.owner.department != department:
                continue
            if owner_id and asset.owner.owner_user_id != owner_id:
                continue

            results.append(
                CatalogSearchResult(
                    asset_id=asset.asset_id,
                    name=asset.name,
                    asset_type=asset.asset_type,
                    classification=asset.classification,
                    department=asset.owner.department,
                    owner_user_id=asset.owner.owner_user_id,
                    source=asset.source,
                    compliance_tags=asset.compliance_tags,
                    is_legal_hold=asset.is_legal_hold,
                )
            )

        return results
