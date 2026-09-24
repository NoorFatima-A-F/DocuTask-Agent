"""
Enterprise Knowledge Registry Service
Central catalog of all enterprise knowledge assets.
"""
from typing import Dict, List, Optional
from datetime import datetime, timezone
from ..models.schemas import (
    KnowledgeAsset, KnowledgeSource, KnowledgeLifecycleState,
    SecurityClassification
)

class KnowledgeRegistryService:
    def __init__(self):
        self._assets: Dict[str, KnowledgeAsset] = {}
        self._sources: Dict[str, KnowledgeSource] = {}

    def register_asset(self, asset: KnowledgeAsset) -> KnowledgeAsset:
        self._assets[asset.id] = asset
        return asset

    def get_asset(self, asset_id: str, tenant_id: str) -> Optional[KnowledgeAsset]:
        asset = self._assets.get(asset_id)
        if asset and asset.tenant_id == tenant_id:
            return asset
        return None

    def list_assets(
        self,
        tenant_id: str,
        state: Optional[KnowledgeLifecycleState] = None,
        source_type: Optional[str] = None,
        security_classification: Optional[SecurityClassification] = None,
        limit: int = 100
    ) -> List[KnowledgeAsset]:
        results = [a for a in self._assets.values() if a.tenant_id == tenant_id]
        if state:
            results = [a for a in results if a.state == state]
        if source_type:
            results = [a for a in results if a.source_type.value == source_type]
        if security_classification:
            results = [a for a in results if a.security_classification == security_classification]
        return results[:limit]

    def update_asset_state(self, asset_id: str, tenant_id: str, state: KnowledgeLifecycleState) -> Optional[KnowledgeAsset]:
        asset = self.get_asset(asset_id, tenant_id)
        if asset:
            asset.state = state
            asset.updated_at = datetime.now(timezone.utc)
            return asset
        return None

    def register_source(self, source: KnowledgeSource) -> KnowledgeSource:
        self._sources[source.id] = source
        return source

    def get_source(self, source_id: str, tenant_id: str) -> Optional[KnowledgeSource]:
        src = self._sources.get(source_id)
        if src and src.tenant_id == tenant_id:
            return src
        return None

    def list_sources(self, tenant_id: str) -> List[KnowledgeSource]:
        return [s for s in self._sources.values() if s.tenant_id == tenant_id]

    def delete_asset(self, asset_id: str, tenant_id: str) -> bool:
        asset = self.get_asset(asset_id, tenant_id)
        if asset:
            del self._assets[asset_id]
            return True
        return False
