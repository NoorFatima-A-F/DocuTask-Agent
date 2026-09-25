"""
Reflection Metadata and Telemetry Models.
Defines identity, audit headers, and execution statistics for reflection runs.
"""

from datetime import datetime, timezone
from typing import Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ReflectionIdentity(BaseModel):
    """Unique identification and correlation envelope for reflection sessions."""
    reflection_id: UUID = Field(default_factory=uuid4)
    execution_id: UUID
    plan_id: Optional[UUID] = None
    agent_id: str = Field(default="autonomous_agent")
    tenant_id: str = Field(default="default")
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}


class ReflectionMetadata(BaseModel):
    """Runtime execution environment metadata for reflection audit trails."""
    engine_version: str = Field(default="20.0.0")
    source_component: str = Field(default="ReflectionEngine")
    environment: str = Field(default="production")
    cloud_region: str = Field(default="us-central1")
    tags: Dict[str, str] = Field(default_factory=dict)

    model_config = {"frozen": True}


class ReflectionStatistics(BaseModel):
    """Quantitative runtime statistics for a reflection execution."""
    evaluation_duration_ms: float = Field(default=0.0, ge=0.0)
    critique_duration_ms: float = Field(default=0.0, ge=0.0)
    learning_duration_ms: float = Field(default=0.0, ge=0.0)
    total_reflection_duration_ms: float = Field(default=0.0, ge=0.0)
    evaluators_executed: int = Field(default=0, ge=0)
    critiques_generated: int = Field(default=0, ge=0)
    learning_artifacts_created: int = Field(default=0, ge=0)
    recommendations_generated: int = Field(default=0, ge=0)
    adaptation_proposals_created: int = Field(default=0, ge=0)

    model_config = {"frozen": True}
