"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Domain Models.
Defines first-class knowledge resources, versions, chunks, permissions, graph entities, citations, and embeddings.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid
from pydantic import BaseModel, Field


class ClassificationLevel(str, Enum):
    """Enterprise security classification tiers for governed knowledge."""
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"
    HIGHLY_RESTRICTED = "HIGHLY_RESTRICTED"


class SensitivityLevel(str, Enum):
    """Data sensitivity rating."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class KnowledgeLifecycleState(str, Enum):
    """9-state knowledge lifecycle specification."""
    CREATED = "CREATED"
    INGESTED = "INGESTED"
    VALIDATED = "VALIDATED"
    CLASSIFIED = "CLASSIFIED"
    INDEXED = "INDEXED"
    PUBLISHED = "PUBLISHED"
    ACTIVE = "ACTIVE"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"


class KnowledgeObjectType(str, Enum):
    """Supported types of knowledge entities."""
    DOCUMENT = "DOCUMENT"
    RECORD = "RECORD"
    POLICY = "POLICY"
    CODE = "CODE"
    CONVERSATION = "CONVERSATION"
    DATASET = "DATASET"
    IMAGE = "IMAGE"
    CUSTOM = "CUSTOM"


class SyncMode(str, Enum):
    """Knowledge synchronization ingestion modes."""
    BATCH = "BATCH"
    INCREMENTAL = "INCREMENTAL"
    STREAMING = "STREAMING"
    EVENT_DRIVEN = "EVENT_DRIVEN"


class KnowledgeObject(BaseModel):
    """
    First-class platform resource representing a governed knowledge asset.
    """
    id: str = Field(default_factory=lambda: f"kobj-{uuid.uuid4().hex[:10]}")
    type: KnowledgeObjectType = KnowledgeObjectType.DOCUMENT
    name: str
    description: str = ""
    owner: str = "system"
    organization_id: str = "org-default"
    workspace_id: str = "ws-default"
    department: str = "general"
    classification: ClassificationLevel = ClassificationLevel.INTERNAL
    sensitivity: SensitivityLevel = SensitivityLevel.MEDIUM
    status: KnowledgeLifecycleState = KnowledgeLifecycleState.CREATED
    version: str = "1.0.0"
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class KnowledgeSource(BaseModel):
    """Origin and external repository connection metadata for ingested knowledge."""
    source_id: str = Field(default_factory=lambda: f"ksrc-{uuid.uuid4().hex[:8]}")
    name: str
    provider: str  # Google Drive, Notion, GitHub, Database, Upload, Email, S3
    connector_id: Optional[str] = None
    authentication_reference: Optional[str] = None
    sync_mode: SyncMode = SyncMode.BATCH
    last_sync: Optional[datetime] = None
    status: str = "ACTIVE"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeVersion(BaseModel):
    """Immutable snapshot of a knowledge object at a specific revision."""
    version_id: str = Field(default_factory=lambda: f"kver-{uuid.uuid4().hex[:8]}")
    knowledge_id: str
    version_number: str = "1.0.0"
    created_by: str = "system"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    checksum: str = ""
    change_summary: str = "Initial ingestion"
    status: KnowledgeLifecycleState = KnowledgeLifecycleState.ACTIVE
    metadata: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeDocument(BaseModel):
    """Parsed document payload associated with a knowledge object."""
    id: str = Field(default_factory=lambda: f"kdoc-{uuid.uuid4().hex[:10]}")
    knowledge_id: str
    title: str
    file_type: str = "pdf"  # pdf, docx, txt, html, md, xlsx, code
    raw_content: str = ""
    normalized_text: str = ""
    byte_size: int = 0
    page_count: int = 1
    author: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeChunk(BaseModel):
    """Granular semantic text chunk for vector embedding and hybrid retrieval."""
    chunk_id: str = Field(default_factory=lambda: f"kchk-{uuid.uuid4().hex[:12]}")
    document_id: str
    knowledge_id: str
    parent_chunk_id: Optional[str] = None
    child_chunk_ids: List[str] = Field(default_factory=list)
    position: int = 0
    content: str
    token_count: int = 0
    page_number: int = 1
    heading_hierarchy: List[str] = Field(default_factory=list)
    embedding_reference: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeEmbedding(BaseModel):
    """Vector embedding representation of a knowledge chunk."""
    embedding_id: str = Field(default_factory=lambda: f"kemb-{uuid.uuid4().hex[:10]}")
    chunk_id: str
    model_name: str = "gemini-embedding-001"
    dimension: int = 768
    vector: List[float] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class KnowledgeRelationship(BaseModel):
    """Directed relationship between knowledge entities or knowledge graph nodes."""
    id: str = Field(default_factory=lambda: f"krel-{uuid.uuid4().hex[:8]}")
    source_id: str
    target_id: str
    relation_type: str  # owns, approved_by, created_by, depends_on, references, belongs_to, relates_to
    properties: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0


class KnowledgePermission(BaseModel):
    """Access control rules governing access to a knowledge object."""
    id: str = Field(default_factory=lambda: f"kperm-{uuid.uuid4().hex[:8]}")
    knowledge_id: str
    allowed_users: List[str] = Field(default_factory=list)
    allowed_roles: List[str] = Field(default_factory=lambda: ["*"])
    allowed_departments: List[str] = Field(default_factory=lambda: ["*"])
    min_clearance_level: ClassificationLevel = ClassificationLevel.INTERNAL
    retention_days: int = 365
    encryption_required: bool = True
    data_residency_regions: List[str] = Field(default_factory=lambda: ["global"])


class Citation(BaseModel):
    """Formal evidence and attribution citation for an AI generation."""
    citation_id: str = Field(default_factory=lambda: f"cite-{uuid.uuid4().hex[:8]}")
    source_title: str
    document_id: str
    version_number: str = "1.0.0"
    page_number: int = 1
    chunk_id: str
    snippet: str
    confidence: float = 1.0
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class RetrievalResult(BaseModel):
    """Ranked retrieval candidate with multifaceted scoring components."""
    chunk: KnowledgeChunk
    score: float
    semantic_score: float = 0.0
    keyword_score: float = 0.0
    authority_score: float = 1.0
    freshness_score: float = 1.0
    trust_score: float = 1.0
    citation: Optional[Citation] = None


class KnowledgeSnapshot(BaseModel):
    """Summary snapshot of an entire knowledge collection."""
    snapshot_id: str = Field(default_factory=lambda: f"ksnap-{uuid.uuid4().hex[:8]}")
    knowledge_id: str
    version: str = "1.0.0"
    chunk_count: int = 0
    document_count: int = 0
    summary: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
