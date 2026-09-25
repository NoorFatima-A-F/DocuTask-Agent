"""
Knowledge Ingestion Engine
"""
from typing import List, Optional
from datetime import datetime, timezone
from ..models.schemas import (
    KnowledgeAsset, KnowledgeLifecycleState,
    KnowledgeSourceType, SecurityClassification, KnowledgeMetadata
)
from .connectors import EnterpriseConnectorFactory
from .pipeline import IngestionPipeline
from ..registry.knowledge_registry import KnowledgeRegistryService

class KnowledgeIngestionEngine:
    def __init__(self, registry: KnowledgeRegistryService):
        self.registry = registry

    def ingest_document(
        self,
        tenant_id: str,
        name: str,
        raw_content: str,
        source_type: KnowledgeSourceType = KnowledgeSourceType.LOCAL_DOCUMENT,
        security_classification: SecurityClassification = SecurityClassification.INTERNAL,
        author: Optional[str] = None,
        custom_tags: Optional[List[str]] = None
    ) -> KnowledgeAsset:
        asset = KnowledgeAsset(
            tenant_id=tenant_id,
            name=name,
            source_type=source_type,
            raw_content=raw_content,
            security_classification=security_classification,
            metadata=KnowledgeMetadata(
                author=author or "System Ingestion",
                custom_tags=custom_tags or [],
                file_type="document"
            ),
            state=KnowledgeLifecycleState.INGESTED
        )
        
        # Process through pipeline
        asset = IngestionPipeline.process_raw_document(asset)
        return self.registry.register_asset(asset)

    def sync_knowledge_source(self, source_id: str, tenant_id: str) -> List[KnowledgeAsset]:
        source = self.registry.get_source(source_id, tenant_id)
        if not source or not source.is_active:
            return []
        
        raw_items = EnterpriseConnectorFactory.sync_source(source.source_type, source.connection_config)
        synced_assets = []
        
        for item in raw_items:
            asset = KnowledgeAsset(
                tenant_id=tenant_id,
                name=item["title"],
                source_type=source.source_type,
                source_id=source.id,
                raw_content=item["content"],
                security_classification=SecurityClassification.INTERNAL,
                metadata=KnowledgeMetadata(
                    author=item["author"],
                    file_type=item["file_type"],
                    source_url=item["url"]
                ),
                state=KnowledgeLifecycleState.INGESTED
            )
            asset = IngestionPipeline.process_raw_document(asset)
            self.registry.register_asset(asset)
            synced_assets.append(asset)
        
        source.last_synced_at = datetime.now(timezone.utc)
        source.total_assets_synced += len(synced_assets)
        return synced_assets
