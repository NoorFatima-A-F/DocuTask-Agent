"""
Domain models and schemas for Phase V6 — Enterprise Knowledge Platform Verification & Validation Program (EKPVVP).
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any


class VerificationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"


class PartId(str, Enum):
    PART_01_INGESTION = "PART_01_INGESTION"
    PART_02_REGISTRY = "PART_02_REGISTRY"
    PART_03_EMBEDDINGS = "PART_03_EMBEDDINGS"
    PART_04_VECTORDB = "PART_04_VECTORDB"
    PART_05_RETRIEVAL = "PART_05_RETRIEVAL"
    PART_06_RERANKING = "PART_06_RERANKING"
    PART_07_CONTEXT = "PART_07_CONTEXT"
    PART_08_GRAPH = "PART_08_GRAPH"
    PART_09_MEMORY = "PART_09_MEMORY"
    PART_10_QUALITY = "PART_10_QUALITY"
    PART_11_FRESHNESS = "PART_11_FRESHNESS"
    PART_12_DRIFT = "PART_12_DRIFT"
    PART_13_SECURITY = "PART_13_SECURITY"
    PART_14_OPTIMIZATION = "PART_14_OPTIMIZATION"
    PART_15_EXPLAINABILITY = "PART_15_EXPLAINABILITY"
    PART_16_SCALABILITY = "PART_16_SCALABILITY"
    PART_17_BENCHMARKING = "PART_17_BENCHMARKING"
    PART_18_DASHBOARDS = "PART_18_DASHBOARDS"
    PART_19_EVIDENCE = "PART_19_EVIDENCE"


class KnowledgeAssetType(str, Enum):
    PDF = "PDF"
    DOCX = "DOCX"
    CSV = "CSV"
    EXCEL = "EXCEL"
    PPTX = "PPTX"
    HTML = "HTML"
    MARKDOWN = "MARKDOWN"
    JSON = "JSON"
    XML = "XML"
    EMAIL = "EMAIL"
    GIT_REPO = "GIT_REPO"
    WIKI = "WIKI"
    JIRA = "JIRA"
    CONFLUENCE = "CONFLUENCE"
    GDRIVE = "GDRIVE"
    SHAREPOINT = "SHAREPOINT"
    SALESFORCE = "SALESFORCE"


class MemoryTier(str, Enum):
    SHORT_TERM = "SHORT_TERM"
    LONG_TERM = "LONG_TERM"
    ORGANIZATIONAL = "ORGANIZATIONAL"
    PROCEDURAL = "PROCEDURAL"
    AGENT_SHARED = "AGENT_SHARED"
    DEPARTMENT = "DEPARTMENT"
    EXECUTIVE = "EXECUTIVE"
    CONVERSATION = "CONVERSATION"
    TASK = "TASK"
    REFLECTION = "REFLECTION"


class RetrievalMode(str, Enum):
    DENSE_VECTOR = "DENSE_VECTOR"
    SPARSE_BM25 = "SPARSE_BM25"
    HYBRID_WEIGHTED = "HYBRID_WEIGHTED"
    GRAPH_EXPANDED = "GRAPH_EXPANDED"
    CROSS_ENCODER_RERANKED = "CROSS_ENCODER_RERANKED"


@dataclass
class KnowledgeAsset:
    asset_id: str
    tenant_id: str
    asset_type: KnowledgeAssetType
    title: str
    content: str
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)
    security_labels: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "asset_id": self.asset_id,
            "tenant_id": self.tenant_id,
            "asset_type": self.asset_type.value,
            "title": self.title,
            "version": self.version,
            "metadata": self.metadata,
            "security_labels": self.security_labels,
            "created_at": self.created_at,
        }


@dataclass
class RetrievalResult:
    chunk_id: str
    asset_id: str
    content: str
    score: float
    rank: int
    retrieval_mode: RetrievalMode
    provenance_explanation: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "asset_id": self.asset_id,
            "content": self.content,
            "score": round(self.score, 4),
            "rank": self.rank,
            "retrieval_mode": self.retrieval_mode.value,
            "provenance_explanation": self.provenance_explanation,
        }


@dataclass
class GraphNode:
    node_id: str
    entity_type: str
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "entity_type": self.entity_type,
            "name": self.name,
            "properties": self.properties,
        }


@dataclass
class GraphEdge:
    source_id: str
    target_id: str
    relation_type: str
    confidence: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "relation_type": self.relation_type,
            "confidence": round(self.confidence, 4),
        }


@dataclass
class MemoryEntry:
    entry_id: str
    tier: MemoryTier
    tenant_id: str
    agent_id: str
    key: str
    value: Any
    decay_factor: float = 1.0
    access_count: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "tier": self.tier.value,
            "tenant_id": self.tenant_id,
            "agent_id": self.agent_id,
            "key": self.key,
            "value": self.value,
            "decay_factor": round(self.decay_factor, 4),
            "access_count": self.access_count,
        }


@dataclass
class AssertionResult:
    name: str
    passed: bool
    message: str
    execution_time_ms: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
            "execution_time_ms": round(self.execution_time_ms, 3),
            "details": self.details,
        }


@dataclass
class PartVerificationResult:
    part_id: PartId
    title: str
    description: str
    status: VerificationStatus
    score: float
    weight: float
    assertions: List[AssertionResult] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0

    @property
    def passed_assertions_count(self) -> int:
        return sum(1 for a in self.assertions if a.passed)

    @property
    def total_assertions_count(self) -> int:
        return len(self.assertions)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "part_id": self.part_id.value,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "score": round(self.score, 2),
            "weight": round(self.weight, 2),
            "passed_assertions": self.passed_assertions_count,
            "total_assertions": self.total_assertions_count,
            "execution_time_ms": round(self.execution_time_ms, 2),
            "metrics": self.metrics,
            "assertions": [a.to_dict() for a in self.assertions],
        }


@dataclass
class KnowledgeReadinessScorecard:
    parts: Dict[str, PartVerificationResult] = field(default_factory=dict)
    indices: Dict[str, float] = field(default_factory=dict)
    composite_score: float = 100.0
    grade: str = "A+"
    total_assertions: int = 0
    passed_assertions: int = 0
    production_ready: bool = True
    total_execution_time_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "composite_score": round(self.composite_score, 2),
            "grade": self.grade,
            "production_ready": self.production_ready,
            "total_assertions": self.total_assertions,
            "passed_assertions": self.passed_assertions,
            "pass_rate_pct": round((self.passed_assertions / max(1, self.total_assertions)) * 100.0, 2),
            "total_execution_time_ms": round(self.total_execution_time_ms, 2),
            "indices": {k: round(v, 2) for k, v in self.indices.items()},
            "parts": {k: v.to_dict() for k, v in self.parts.items()},
        }
