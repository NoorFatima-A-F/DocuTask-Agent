"""
Phase 13.21 - Enterprise AI Knowledge & Context Intelligence Platform (EAKCIP) Schemas
"""
from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid

class KnowledgeLifecycleState(str, Enum):
    DISCOVERED = "DISCOVERED"
    INGESTED = "INGESTED"
    PROCESSED = "PROCESSED"
    INDEXED = "INDEXED"
    AVAILABLE = "AVAILABLE"
    UPDATED = "UPDATED"
    ARCHIVED = "ARCHIVED"

class SecurityClassification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"
    STRICT_SECRET = "STRICT_SECRET"

class KnowledgeSourceType(str, Enum):
    LOCAL_DOCUMENT = "LOCAL_DOCUMENT"
    GOOGLE_DRIVE = "GOOGLE_DRIVE"
    SHAREPOINT = "SHAREPOINT"
    SLACK = "SLACK"
    TEAMS = "TEAMS"
    JIRA = "JIRA"
    SALESFORCE = "SALESFORCE"
    GITHUB = "GITHUB"
    CONFLUENCE = "CONFLUENCE"
    DATABASE = "DATABASE"

class EntityType(str, Enum):
    EMPLOYEE = "EMPLOYEE"
    DEPARTMENT = "DEPARTMENT"
    PROJECT = "PROJECT"
    AI_AGENT = "AI_AGENT"
    SYSTEM = "SYSTEM"
    POLICY = "POLICY"
    DOCUMENT = "DOCUMENT"
    CONTRACT = "CONTRACT"
    VENDOR = "VENDOR"
    CONCEPT = "CONCEPT"

class MemoryTier(str, Enum):
    SHORT_TERM = "SHORT_TERM"       # Working / in-task memory
    LONG_TERM = "LONG_TERM"         # Historical episodic memory
    ORGANIZATIONAL = "ORGANIZATIONAL"# Enterprise wide knowledge
    PROCEDURAL = "PROCEDURAL"       # SOPs and workflow execution patterns

class AccessPolicy(BaseModel):
    allowed_roles: List[str] = Field(default_factory=lambda: ["admin", "member"])
    allowed_users: List[str] = Field(default_factory=list)
    denied_roles: List[str] = Field(default_factory=list)
    require_mfa: bool = False
    max_security_clearance: SecurityClassification = SecurityClassification.CONFIDENTIAL

class KnowledgeMetadata(BaseModel):
    author: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    file_type: str = "text"
    file_size_bytes: int = 0
    token_count: int = 0
    custom_tags: List[str] = Field(default_factory=list)
    extracted_entities: List[str] = Field(default_factory=list)
    source_url: Optional[str] = None

class KnowledgeAsset(BaseModel):
    id: str = Field(default_factory=lambda: f"asset-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    organization_id: str = "default-org"
    workspace_id: str = "default-workspace"
    project_id: str = "default-project"
    name: str
    description: str = ""
    source_type: KnowledgeSourceType = KnowledgeSourceType.LOCAL_DOCUMENT
    source_id: Optional[str] = None
    state: KnowledgeLifecycleState = KnowledgeLifecycleState.DISCOVERED
    security_classification: SecurityClassification = SecurityClassification.INTERNAL
    access_policy: AccessPolicy = Field(default_factory=AccessPolicy)
    raw_content: str = ""
    processed_content: str = ""
    embedding_ids: List[str] = Field(default_factory=list)
    metadata: KnowledgeMetadata = Field(default_factory=KnowledgeMetadata)
    version: int = 1
    freshness_score: float = 1.0
    reliability_score: float = 0.95
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class KnowledgeSource(BaseModel):
    id: str = Field(default_factory=lambda: f"src-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    organization_id: str = "default-org"
    workspace_id: str = "default-workspace"
    name: str
    source_type: KnowledgeSourceType
    connection_config: Dict[str, Any] = Field(default_factory=dict)
    sync_schedule: str = "0 * * * *"  # hourly cron
    is_active: bool = True
    last_synced_at: Optional[datetime] = None
    total_assets_synced: int = 0
    health_status: str = "HEALTHY"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class GraphNode(BaseModel):
    id: str = Field(default_factory=lambda: f"node-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    name: str
    entity_type: EntityType
    properties: Dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = 1.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class GraphEdge(BaseModel):
    id: str = Field(default_factory=lambda: f"edge-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    source_node_id: str
    target_node_id: str
    relation_type: str  # e.g., "works_for", "owns", "uses", "depends_on", "governed_by"
    properties: Dict[str, Any] = Field(default_factory=dict)
    weight: float = 1.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ContextRetrievalRequest(BaseModel):
    tenant_id: str = "default-tenant"
    organization_id: str = "default-org"
    workspace_id: str = "default-workspace"
    user_roles: List[str] = Field(default_factory=lambda: ["member"])
    user_clearance: SecurityClassification = SecurityClassification.CONFIDENTIAL
    goal: str
    max_tokens: int = 2000
    include_graph_context: bool = True
    include_memory: bool = True
    memory_tier: Optional[MemoryTier] = None
    top_k: int = 5
    filter_tags: List[str] = Field(default_factory=list)

class RetrievedSnippet(BaseModel):
    asset_id: str
    title: str
    content: str
    score: float
    source_type: KnowledgeSourceType
    security_classification: SecurityClassification
    matched_via: str = "HYBRID_SEMANTIC"  # "SEMANTIC", "KEYWORD", "GRAPH", "MEMORY"

class ContextRetrievalResponse(BaseModel):
    query: str
    snippets: List[RetrievedSnippet] = Field(default_factory=list)
    graph_context: List[str] = Field(default_factory=list)
    memory_context: List[str] = Field(default_factory=list)
    optimized_context_prompt: str
    total_tokens_estimated: int
    compression_ratio: float = 1.0
    retrieval_latency_ms: float = 0.0

class MemoryEntry(BaseModel):
    id: str = Field(default_factory=lambda: f"mem-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    agent_id: Optional[str] = None
    tier: MemoryTier = MemoryTier.SHORT_TERM
    key: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    importance_score: float = 1.0
    access_count: int = 0
    expires_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class KnowledgeConflict(BaseModel):
    id: str = Field(default_factory=lambda: f"conf-{uuid.uuid4().hex[:8]}")
    tenant_id: str
    asset_id_a: str
    asset_id_b: str
    conflict_topic: str
    statement_a: str
    statement_b: str
    severity: str = "MEDIUM"  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    detected_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "OPEN"  # "OPEN", "RESOLVED", "IGNORED"
    recommended_resolution: str = ""

class KnowledgeQualityReport(BaseModel):
    tenant_id: str
    total_assets: int
    freshness_index: float
    avg_reliability_score: float
    duplicate_assets_count: int
    active_conflicts: List[KnowledgeConflict] = Field(default_factory=list)
    coverage_score: float
    healthy: bool = True
