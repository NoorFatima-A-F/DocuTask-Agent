"""
Enterprise Memory, Knowledge & Context Foundation Package.
Provides MemoryItem, MemoryManager, MemoryRepository, KnowledgeGraph, VectorEmbedding,
ContextAssembler, MemorySnapshot, MemoryFactory, and memory tier contracts.
Decouples Planners from concrete storage providers (Redis, PostgreSQL, Supabase, Vertex AI, AlloyDB AI).
"""

from app.agents.memory.builders import (
    KnowledgeBuilder,
    MemoryBuilder,
    QueryBuilder,
    SnapshotBuilder,
)
from app.agents.memory.cache import MemoryCache
from app.agents.memory.conversation_memory import ConversationMemory
from app.agents.memory.context import ContextAssembler, ContextWindow, TokenBudget
from app.agents.memory.embeddings import BaseEmbeddingProvider, VectorEmbedding
from app.agents.memory.episodic_memory import EpisodicMemory
from app.agents.memory.events import (
    MemoryArchivedEvent,
    MemoryCompactedEvent,
    MemoryCreatedEvent,
    MemoryDeletedEvent,
    MemoryExpiredEvent,
    MemoryMergedEvent,
    MemoryPromotedEvent,
    MemoryRestoredEvent,
    MemoryRetrievedEvent,
    MemoryUpdatedEvent,
)
from app.agents.memory.exceptions import (
    ContextWindowExceededException,
    MemoryException,
    MemoryNotFoundException,
    MemoryValidationException,
    ProviderUnavailableException,
    SnapshotCorruptedException,
)
from app.agents.memory.execution_memory import ExecutionMemory
from app.agents.memory.factory import MemoryFactory
from app.agents.memory.indexing import MemoryIndexer
from app.agents.memory.interfaces import IMemoryManager, IMemoryRetriever
from app.agents.memory.knowledge import (
    KnowledgeCluster,
    KnowledgeEdge,
    KnowledgeGraphNode,
    KnowledgeItem,
    KnowledgeSource,
)
from app.agents.memory.lifecycle import MemoryLifecycleState
from app.agents.memory.long_term_memory import LongTermMemory
from app.agents.memory.manager import MemoryManager
from app.agents.memory.metadata import MemoryIdentity, MemoryMetadata, MemoryStatistics
from app.agents.memory.metrics import MemoryMetricRecord, MemoryMetricsCollector
from app.agents.memory.persistence import MemoryPersistence
from app.agents.memory.policies import (
    CompressionPolicy,
    ExpirationPolicy,
    PromotionPolicy,
    RetentionPolicy,
    SnapshotPolicy,
)
from app.agents.memory.procedural_memory import ProceduralMemory
from app.agents.memory.providers import (
    BaseMemoryProvider,
    CloudProvider,
    InMemoryProvider,
    MockProvider,
    VectorProvider,
)
from app.agents.memory.ranking import MemoryRanker
from app.agents.memory.reflection_memory import ReflectionMemory
from app.agents.memory.repository import MemoryItem
from app.agents.memory.retrieval import MemoryQuery, MemoryRetriever, RetrievalResult
from app.agents.memory.semantic_memory import SemanticMemory
from app.agents.memory.serializers import MemorySerializer
from app.agents.memory.session import MemorySession
from app.agents.memory.short_term_memory import ShortTermMemory
from app.agents.memory.snapshots import (
    ContextSnapshot,
    MemorySnapshot,
    ReflectionSnapshot,
)
from app.agents.memory.validators import MemoryValidator
from app.agents.memory.working_memory import WorkingMemory

__all__ = [
    # Core Aggregates & Models
    "MemoryItem",
    "MemoryIdentity",
    "MemoryMetadata",
    "MemoryStatistics",
    "MemoryLifecycleState",
    "MemorySession",
    # Memory Sub-Tiers
    "WorkingMemory",
    "ShortTermMemory",
    "LongTermMemory",
    "EpisodicMemory",
    "SemanticMemory",
    "ProceduralMemory",
    "ConversationMemory",
    "ExecutionMemory",
    "ReflectionMemory",
    # Knowledge Graph
    "KnowledgeItem",
    "KnowledgeGraphNode",
    "KnowledgeEdge",
    "KnowledgeCluster",
    "KnowledgeSource",
    # Embeddings & Context Window
    "VectorEmbedding",
    "BaseEmbeddingProvider",
    "TokenBudget",
    "ContextWindow",
    "ContextAssembler",
    # Providers & Interfaces
    "BaseMemoryProvider",
    "InMemoryProvider",
    "MockProvider",
    "VectorProvider",
    "CloudProvider",
    "IMemoryManager",
    "IMemoryRetriever",
    # Retrieval & Ranking
    "MemoryRetriever",
    "MemoryQuery",
    "RetrievalResult",
    "MemoryRanker",
    "MemoryIndexer",
    # Manager & Subsystems
    "MemoryManager",
    "MemoryCache",
    "MemoryPersistence",
    "MemorySerializer",
    "MemoryValidator",
    "MemoryMetricsCollector",
    "MemoryMetricRecord",
    "MemoryFactory",
    # Policies & Snapshots & Builders
    "RetentionPolicy",
    "ExpirationPolicy",
    "PromotionPolicy",
    "CompressionPolicy",
    "SnapshotPolicy",
    "MemorySnapshot",
    "ContextSnapshot",
    "ReflectionSnapshot",
    "MemoryBuilder",
    "KnowledgeBuilder",
    "QueryBuilder",
    "SnapshotBuilder",
    # Domain Events
    "MemoryCreatedEvent",
    "MemoryUpdatedEvent",
    "MemoryDeletedEvent",
    "MemoryExpiredEvent",
    "MemoryPromotedEvent",
    "MemoryRetrievedEvent",
    "MemoryMergedEvent",
    "MemoryArchivedEvent",
    "MemoryCompactedEvent",
    "MemoryRestoredEvent",
    # Exceptions
    "MemoryException",
    "MemoryNotFoundException",
    "ProviderUnavailableException",
    "ContextWindowExceededException",
    "SnapshotCorruptedException",
    "MemoryValidationException",
]
