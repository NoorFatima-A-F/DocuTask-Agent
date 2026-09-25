"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Main Package.
Provides the enterprise operating system for governed knowledge, hybrid retrieval, intelligent chunking,
multi-tier memory, citations, and permission-aware search.
"""

from app.knowledge.analytics.engine import KnowledgeAnalytics, KnowledgeAnalyticsReport
from app.knowledge.chunking.chunker import (
    BaseChunker,
    ChunkingEngine,
    CodeChunker,
    ConversationChunker,
    FixedChunker,
    HeadingChunker,
    HierarchicalChunker,
    SemanticChunker,
    TableChunker,
)
from app.knowledge.citations.engine import CitationEngine
from app.knowledge.context.builder import ContextBuilder, ContextPackage
from app.knowledge.core.exceptions import (
    ChunkingError,
    ClassificationViolationError,
    EmbeddingError,
    IngestionError,
    InvalidKnowledgeStateError,
    KnowledgeError,
    KnowledgeGraphError,
    KnowledgeNotFoundError,
    PermissionDeniedError,
    RetrievalError,
    VectorStoreError,
)
from app.knowledge.core.models import (
    Citation,
    ClassificationLevel,
    KnowledgeChunk,
    KnowledgeDocument,
    KnowledgeEmbedding,
    KnowledgeLifecycleState,
    KnowledgeObject,
    KnowledgeObjectType,
    KnowledgePermission,
    KnowledgeRelationship,
    KnowledgeSnapshot,
    KnowledgeSource,
    KnowledgeVersion,
    RetrievalResult,
    SensitivityLevel,
    SyncMode,
)
from app.knowledge.embeddings.provider import (
    DeterministicEmbeddingProvider,
    EmbeddingProvider,
    GeminiEmbeddingProvider,
    OpenAIEmbeddingProvider,
)
from app.knowledge.governance.engine import (
    CLEARANCE_RANKS,
    KnowledgeGovernanceEngine,
    UserSecurityContext,
)
from app.knowledge.graph.engine import GraphEntity, KnowledgeGraphEngine
from app.knowledge.ingestion.adapter import (
    BatchFileAdapter,
    ConnectorKnowledgeAdapter,
    KnowledgeSourceAdapter,
)
from app.knowledge.lifecycle.manager import KnowledgeLifecycleEvent, KnowledgeLifecycleManager
from app.knowledge.memory.consolidation import ConsolidationReport, MemoryConsolidationEngine
from app.knowledge.memory.engine import (
    MemoryIntelligencePlatform,
    MemoryItem,
    MemoryTier,
)
from app.knowledge.processing.pipeline import (
    DocumentIntelligencePipeline,
    DocumentSection,
    ProcessedDocument,
)
from app.knowledge.ranking.engine import RankingEngine, RankingWeights
from app.knowledge.registry.registry import KnowledgeRegistry
from app.knowledge.retrieval.engine import HybridRetrievalEngine, bm25_score
from app.knowledge.sdk.builder import KnowledgeBuilder, KnowledgeSDK
from app.knowledge.sync.engine import KnowledgeSyncEngine, SyncStatusRecord
from app.knowledge.vector.store import (
    InMemoryVectorStore,
    PgVectorStoreAdapter,
    QdrantStoreAdapter,
    VectorStoreInterface,
    cosine_similarity,
)

__all__ = [
    # Core Domain & Exceptions
    "KnowledgeObject",
    "KnowledgeSource",
    "KnowledgeVersion",
    "KnowledgeDocument",
    "KnowledgeChunk",
    "KnowledgeEmbedding",
    "KnowledgeRelationship",
    "KnowledgePermission",
    "Citation",
    "RetrievalResult",
    "KnowledgeSnapshot",
    "ClassificationLevel",
    "SensitivityLevel",
    "KnowledgeLifecycleState",
    "KnowledgeObjectType",
    "SyncMode",
    "KnowledgeError",
    "KnowledgeNotFoundError",
    "InvalidKnowledgeStateError",
    "PermissionDeniedError",
    "ClassificationViolationError",
    "ChunkingError",
    "EmbeddingError",
    "VectorStoreError",
    "RetrievalError",
    "IngestionError",
    "KnowledgeGraphError",
    # Lifecycle
    "KnowledgeLifecycleManager",
    "KnowledgeLifecycleEvent",
    # Registry
    "KnowledgeRegistry",
    # Ingestion & Processing
    "KnowledgeSourceAdapter",
    "BatchFileAdapter",
    "ConnectorKnowledgeAdapter",
    "DocumentIntelligencePipeline",
    "ProcessedDocument",
    "DocumentSection",
    # Chunking
    "ChunkingEngine",
    "BaseChunker",
    "FixedChunker",
    "SemanticChunker",
    "HeadingChunker",
    "TableChunker",
    "CodeChunker",
    "ConversationChunker",
    "HierarchicalChunker",
    # Embeddings & Vector
    "EmbeddingProvider",
    "DeterministicEmbeddingProvider",
    "GeminiEmbeddingProvider",
    "OpenAIEmbeddingProvider",
    "VectorStoreInterface",
    "InMemoryVectorStore",
    "PgVectorStoreAdapter",
    "QdrantStoreAdapter",
    "cosine_similarity",
    # Retrieval & Ranking
    "HybridRetrievalEngine",
    "bm25_score",
    "RankingEngine",
    "RankingWeights",
    # Context & Citations
    "ContextBuilder",
    "ContextPackage",
    "CitationEngine",
    # Graph
    "KnowledgeGraphEngine",
    "GraphEntity",
    # Memory
    "MemoryIntelligencePlatform",
    "MemoryItem",
    "MemoryTier",
    "MemoryConsolidationEngine",
    "ConsolidationReport",
    # Governance, Sync, Analytics
    "KnowledgeGovernanceEngine",
    "UserSecurityContext",
    "CLEARANCE_RANKS",
    "KnowledgeSyncEngine",
    "SyncStatusRecord",
    "KnowledgeAnalytics",
    "KnowledgeAnalyticsReport",
    # SDK
    "KnowledgeSDK",
    "KnowledgeBuilder",
]
