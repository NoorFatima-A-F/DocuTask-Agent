"""
Planning Metadata, Identity, Context, and Statistics Domain Models.
Provides strongly typed, immutable Pydantic v2 models for enterprise planning representation.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class PlanIdentity(BaseModel):
    """Immutable Plan Identity identifying plan instance across distributed executions."""
    plan_id: UUID = Field(default_factory=uuid4)
    goal_id: Optional[str] = Field(default=None)
    workflow_id: Optional[str] = Field(default=None)
    session_id: Optional[str] = Field(default=None)
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    tenant_id: str = Field(default="default")
    owner: str = Field(default="system")
    version: str = Field(default="v1.0")
    model_config = {"frozen": True}


class PlanStatistics(BaseModel):
    """Execution estimates and performance statistics."""
    total_nodes_count: int = Field(default=0, ge=0)
    total_edges_count: int = Field(default=0, ge=0)
    estimated_duration_seconds: float = Field(default=0.0, ge=0.0)
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)
    estimated_tokens: int = Field(default=0, ge=0)
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class PlanContext(BaseModel):
    """Context parameters provided during plan generation and evaluation."""
    document_id: Optional[UUID] = Field(default=None)
    user_id: Optional[UUID] = Field(default=None)
    task_scope: str = Field(default="DOCUMENT_PROCESSING")
    execution_environment: str = Field(default="PRODUCTION")
    parameters: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class PlanMetadata(BaseModel):
    """Comprehensive Plan Metadata."""
    plan_type: str = Field(default="EXECUTION")  # STRATEGIC, TACTICAL, OPERATIONAL, EXECUTION, RECOVERY, MULTI_AGENT
    priority: str = Field(default="MEDIUM")  # LOW, MEDIUM, HIGH, CRITICAL
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    security_classification: str = Field(default="INTERNAL")
    tags: List[str] = Field(default_factory=list)
    labels: Dict[str, str] = Field(default_factory=dict)
    checksum: str = Field(default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    custom: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}
