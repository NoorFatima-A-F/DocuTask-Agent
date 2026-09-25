"""Enterprise Data Governance Registry Models (Phase 8B)."""

from __future__ import annotations

import enum
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


class AssetLifecycleState(str, enum.Enum):
    """8-state Asset Lifecycle FSM."""
    DISCOVERED = "DISCOVERED"
    REGISTERED = "REGISTERED"
    CLASSIFIED = "CLASSIFIED"
    ACTIVE = "ACTIVE"
    UPDATED = "UPDATED"
    SUPERSEDED = "SUPERSEDED"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"


class AssetType(str, enum.Enum):
    """Supported governed data asset types."""
    DOCUMENT = "DOCUMENT"
    PROMPT = "PROMPT"
    EMBEDDING = "EMBEDDING"
    RETRIEVAL_CONTEXT = "RETRIEVAL_CONTEXT"
    AGENT_MEMORY = "AGENT_MEMORY"
    MODEL_OUTPUT = "MODEL_OUTPUT"
    BUSINESS_DATA = "BUSINESS_DATA"
    LOG = "LOG"
    EVENT = "EVENT"
    KNOWLEDGE_CHUNK = "KNOWLEDGE_CHUNK"
    DATASET = "DATASET"


class ClassificationLevel(str, enum.Enum):
    """Data sensitivity classification levels."""
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"
    HIGHLY_RESTRICTED = "HIGHLY_RESTRICTED"


class SensitivityCategory(str, enum.Enum):
    """Specific categories of sensitive information."""
    PII = "PII"
    FINANCIAL = "FINANCIAL"
    HEALTHCARE = "HEALTHCARE"
    LEGAL = "LEGAL"
    INTELLECTUAL_PROPERTY = "INTELLECTUAL_PROPERTY"
    CREDENTIALS = "CREDENTIALS"
    GENERAL = "GENERAL"


class DataOwnership(BaseModel):
    """Explicit data ownership and stewardship metadata."""
    owner_user_id: str
    responsible_team: str = "General"
    department: str = "General"
    data_steward_id: Optional[str] = None
    approver_id: Optional[str] = None
    business_purpose: str = "Enterprise Operations"


class DataAsset(BaseModel):
    """Canonical Governed Data Asset Entity."""
    asset_id: str
    organization_id: str
    workspace_id: str
    project_id: str = "default"
    name: str
    asset_type: AssetType
    source: str
    location_uri: str
    owner: DataOwnership
    creator_id: str
    classification: ClassificationLevel = ClassificationLevel.INTERNAL
    sensitivity_categories: Set[SensitivityCategory] = Field(default_factory=set)
    version: int = 1
    status: AssetLifecycleState = AssetLifecycleState.REGISTERED
    checksum_sha256: str = ""
    size_bytes: int = 0
    mime_type: str = "application/octet-stream"
    retention_policy_id: Optional[str] = None
    is_legal_hold: bool = False
    compliance_tags: List[str] = Field(default_factory=list)
    custom_metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
