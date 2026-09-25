"""
Document Processing & Ingestion Pipeline
"""
import re
from ..models.schemas import KnowledgeAsset, KnowledgeLifecycleState

class IngestionPipeline:
    @staticmethod
    def process_raw_document(asset: KnowledgeAsset) -> KnowledgeAsset:
        # 1. Normalize content
        cleaned = re.sub(r'\s+', ' ', asset.raw_content).strip()
        asset.processed_content = cleaned
        
        # 2. Calculate tokens & basic metadata
        tokens = len(cleaned.split())
        asset.metadata.token_count = tokens
        asset.metadata.file_size_bytes = len(asset.raw_content.encode("utf-8"))
        
        # 3. Transition lifecycle
        asset.state = KnowledgeLifecycleState.PROCESSED
        return asset
