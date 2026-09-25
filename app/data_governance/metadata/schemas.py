"""Governed Metadata Schemas (Phase 8B).

Categorizes metadata into 4 enterprise dimensions:
1. Technical Metadata
2. Business Metadata
3. AI Metadata
4. Compliance Metadata
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.data_governance.registry.models import ClassificationLevel


class TechnicalMetadata(BaseModel):
    """File format, size, checksum, schema, storage location."""
    format: str
    size_bytes: int
    checksum_sha256: str
    encoding: str = "utf-8"
    storage_provider: str = "local"
    location_uri: str
    schema_definition: Optional[Dict[str, Any]] = None
    created_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    modified_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class BusinessMetadata(BaseModel):
    """Department, owner, business purpose, domain criticality."""
    department: str = "General"
    owner_user_id: str
    purpose: str = "Operational Processing"
    business_criticality: str = "MEDIUM"  # LOW, MEDIUM, HIGH, MISSION_CRITICAL
    usage_context: str = ""
    dependencies: List[str] = Field(default_factory=list)


class AIMetadata(BaseModel):
    """Embedding models, LLM versions, agent cognition, retrieval grounding."""
    embedding_model: Optional[str] = None
    embedding_dimensions: Optional[int] = None
    model_version: Optional[str] = None
    prompt_version: Optional[str] = None
    agent_id: Optional[str] = None
    workflow_id: Optional[str] = None
    retrieval_sources: List[str] = Field(default_factory=list)
    confidence_score: Optional[float] = None


class ComplianceMetadata(BaseModel):
    """Classification, sensitivity, regulatory scope, retention schedule."""
    classification: ClassificationLevel = ClassificationLevel.INTERNAL
    sensitivity: str = "GENERAL"
    retention_days: int = 365
    region: str = "us-east-1"
    regulations: List[str] = Field(default_factory=list)  # GDPR, HIPAA, SOC2, PCI_DSS
    is_legal_hold: bool = False


class ComprehensiveAssetMetadata(BaseModel):
    """Unified 4-dimensional metadata container."""
    asset_id: str
    technical: TechnicalMetadata
    business: BusinessMetadata
    ai: Optional[AIMetadata] = None
    compliance: ComplianceMetadata
