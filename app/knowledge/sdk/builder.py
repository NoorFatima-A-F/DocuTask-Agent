"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Knowledge SDK.
Provides a unified developer SDK and fluent builder for configuring, ingesting, indexing, and querying the Knowledge Fabric.
"""

from __future__ import annotations

import logging
import time
from typing import Dict, List, Optional

from app.knowledge.analytics.engine import KnowledgeAnalytics
from app.knowledge.chunking.chunker import ChunkingEngine
from app.knowledge.citations.engine import CitationEngine
from app.knowledge.context.builder import ContextBuilder, ContextPackage
from app.knowledge.core.models import (
    KnowledgeChunk,
    KnowledgeDocument,
)
from app.knowledge.embeddings.provider import DeterministicEmbeddingProvider, EmbeddingProvider
from app.knowledge.governance.engine import KnowledgeGovernanceEngine, UserSecurityContext
from app.knowledge.graph.engine import KnowledgeGraphEngine
from app.knowledge.ingestion.adapter import KnowledgeSourceAdapter
from app.knowledge.lifecycle.manager import KnowledgeLifecycleManager
from app.knowledge.memory.consolidation import MemoryConsolidationEngine
from app.knowledge.memory.engine import MemoryIntelligencePlatform
from app.knowledge.processing.pipeline import DocumentIntelligencePipeline
from app.knowledge.ranking.engine import RankingEngine
from app.knowledge.registry.registry import KnowledgeRegistry
from app.knowledge.retrieval.engine import HybridRetrievalEngine
from app.knowledge.sync.engine import KnowledgeSyncEngine
from app.knowledge.vector.store import InMemoryVectorStore, VectorStoreInterface

logger = logging.getLogger(__name__)


class KnowledgeSDK:
    """
    Unified developer interface for the Enterprise Knowledge Operating System.
    """

    def __init__(
        self,
        registry: Optional[KnowledgeRegistry] = None,
        lifecycle_manager: Optional[KnowledgeLifecycleManager] = None,
        processing_pipeline: Optional[DocumentIntelligencePipeline] = None,
        chunking_engine: Optional[ChunkingEngine] = None,
        embedding_provider: Optional[EmbeddingProvider] = None,
        vector_store: Optional[VectorStoreInterface] = None,
        retrieval_engine: Optional[HybridRetrievalEngine] = None,
        ranking_engine: Optional[RankingEngine] = None,
        context_builder: Optional[ContextBuilder] = None,
        citation_engine: Optional[CitationEngine] = None,
        graph_engine: Optional[KnowledgeGraphEngine] = None,
        memory_platform: Optional[MemoryIntelligencePlatform] = None,
        consolidation_engine: Optional[MemoryConsolidationEngine] = None,
        governance_engine: Optional[KnowledgeGovernanceEngine] = None,
        sync_engine: Optional[KnowledgeSyncEngine] = None,
        analytics: Optional[KnowledgeAnalytics] = None,
    ):
        self.lifecycle_manager = lifecycle_manager or KnowledgeLifecycleManager()
        self.registry = registry or KnowledgeRegistry(self.lifecycle_manager)
        self.processing_pipeline = processing_pipeline or DocumentIntelligencePipeline()
        self.chunking_engine = chunking_engine or ChunkingEngine()
        self.embedding_provider = embedding_provider or DeterministicEmbeddingProvider()
        self.vector_store = vector_store or InMemoryVectorStore()
        self.retrieval_engine = retrieval_engine or HybridRetrievalEngine(self.vector_store, self.embedding_provider)
        self.ranking_engine = ranking_engine or RankingEngine()
        self.citation_engine = citation_engine or CitationEngine()
        self.context_builder = context_builder or ContextBuilder(self.citation_engine)
        self.graph_engine = graph_engine or KnowledgeGraphEngine()
        self.memory_platform = memory_platform or MemoryIntelligencePlatform()
        self.consolidation_engine = consolidation_engine or MemoryConsolidationEngine(self.memory_platform)
        self.governance_engine = governance_engine or KnowledgeGovernanceEngine()
        self.sync_engine = sync_engine or KnowledgeSyncEngine()
        self.analytics = analytics or KnowledgeAnalytics()

        self._adapters: Dict[str, KnowledgeSourceAdapter] = {}

    def register_source(self, adapter: KnowledgeSourceAdapter) -> None:
        """Registers a knowledge source adapter."""
        self._adapters[adapter.source_model.source_id] = adapter

    def ingest_document(
        self,
        document: KnowledgeDocument,
        chunking_strategy: Optional[str] = None,
    ) -> List[KnowledgeChunk]:
        """
        Executes document processing, chunking, embedding, and vector indexing.
        """
        # Step 1: Document Intelligence Processing
        self.processing_pipeline.process(document)

        # Step 2: Chunking
        chunks = self.chunking_engine.chunk_document(document, strategy=chunking_strategy)

        # Step 3: Embed & Index into Hybrid Retrieval Engine
        for chunk in chunks:
            chunk.metadata["title"] = document.title
            chunk.metadata["file_type"] = document.file_type
            self.retrieval_engine.index_chunk(chunk)

        self.analytics.record_indexed_chunks(len(chunks))
        logger.info(f"Ingested and indexed {len(chunks)} chunks for document '{document.id}'")
        return chunks

    def query_context(
        self,
        query: str,
        user_context: Optional[UserSecurityContext] = None,
        top_k: int = 5,
        max_tokens: int = 2000,
    ) -> ContextPackage:
        """
        Executes permission-aware hybrid search, multi-factor ranking, and context synthesis.
        """
        start = time.perf_counter()

        # Step 1: Hybrid Retrieval (Lexical + Semantic + RRF)
        candidates = self.retrieval_engine.search_hybrid(query, top_k=top_k * 2)

        # Step 2: Permission-Aware Governance Filter
        if user_context:
            objects_map = {obj.id: obj for obj in self.registry.search()}
            candidates = self.governance_engine.filter_retrieval_results(
                candidates, user_context, objects_map
            )

        # Step 3: Multi-factor Reranking
        ranked_candidates = self.ranking_engine.rank(candidates)

        # Step 4: Context Building & Citation Generation
        context_pkg = self.context_builder.build_context(
            ranked_candidates[:top_k],
            max_tokens=max_tokens,
            include_citations=True,
        )

        latency = (time.perf_counter() - start) * 1000.0
        self.analytics.record_query(query, len(context_pkg.chunks), latency)

        return context_pkg


class KnowledgeBuilder:
    """Fluent builder for constructing customized KnowledgeSDK instances."""

    def __init__(self):
        self._embedding_provider: Optional[EmbeddingProvider] = None
        self._vector_store: Optional[VectorStoreInterface] = None

    def with_embedding_provider(self, provider: EmbeddingProvider) -> KnowledgeBuilder:
        self._embedding_provider = provider
        return self

    def with_vector_store(self, store: VectorStoreInterface) -> KnowledgeBuilder:
        self._vector_store = store
        return self

    def build(self) -> KnowledgeSDK:
        return KnowledgeSDK(
            embedding_provider=self._embedding_provider,
            vector_store=self._vector_store,
        )
