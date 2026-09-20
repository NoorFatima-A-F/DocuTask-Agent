"""
Decision Metadata, Statistics, and Trace Models.
Provides immutable Pydantic v2 metadata models for decision evaluations.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class DecisionIdentity(BaseModel):
    """Immutable Decision Identity."""
    decision_id: UUID = Field(default_factory=uuid4)
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    execution_id: Optional[str] = Field(default=None)
    goal_id: Optional[str] = Field(default=None)
    task_id: Optional[str] = Field(default=None)
    workflow_id: Optional[str] = Field(default=None)
    tenant_id: str = Field(default="default")
    owner: str = Field(default="system")
    model_config = {"frozen": True}


class DecisionStatistics(BaseModel):
    """Evaluation operational metrics."""
    evaluation_duration_ms: float = Field(default=0.0, ge=0.0)
    rules_evaluated_count: int = Field(default=0, ge=0)
    policies_evaluated_count: int = Field(default=0, ge=0)
    risk_score: float = Field(default=0.0, ge=0.0, le=1.0)
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)
    model_config = {"frozen": True}


class DecisionMetadata(BaseModel):
    """Metadata parameters for a decision record."""
    decision_type: str = Field(default="OPERATIONAL")
    evaluator_version: str = Field(default="v1.0")
    security_classification: str = Field(default="INTERNAL")
    tags: List[str] = Field(default_factory=list)
    labels: Dict[str, str] = Field(default_factory=dict)
    checksum: str = Field(default="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    extra: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class DecisionTrace(BaseModel):
    """Detailed execution trace of decision evaluation."""
    trace_id: str = Field(default_factory=lambda: uuid4().hex)
    evaluated_policy_ids: List[str] = Field(default_factory=list)
    triggered_rule_ids: List[str] = Field(default_factory=list)
    evaluation_timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = {"frozen": True}
