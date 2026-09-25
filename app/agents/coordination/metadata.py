"""
Coordination Metadata and Statistics.
Defines envelopes for tracing, correlation, and quantitative coordination telemetry.
"""

from datetime import datetime, timezone
from typing import Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class CoordinationIdentity(BaseModel):
    """Unique identity envelope for a coordinated multi-agent workflow."""
    coordination_id: UUID = Field(default_factory=uuid4)
    goal_id: Optional[UUID] = None
    supervisor_id: Optional[UUID] = None
    tenant_id: str = Field(default="default")
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}


class CoordinationMetadata(BaseModel):
    """Execution context and cloud deployment metadata."""
    engine_version: str = Field(default="21.0.0")
    cloud_region: str = Field(default="us-central1")
    environment: str = Field(default="production")
    tags: Dict[str, str] = Field(default_factory=dict)

    model_config = {"frozen": True}


class CoordinationStatistics(BaseModel):
    """Quantitative runtime statistics for a multi-agent coordination execution."""
    discovery_duration_ms: float = Field(default=0.0, ge=0.0)
    delegation_duration_ms: float = Field(default=0.0, ge=0.0)
    coordination_duration_ms: float = Field(default=0.0, ge=0.0)
    total_duration_ms: float = Field(default=0.0, ge=0.0)
    agents_discovered: int = Field(default=0, ge=0)
    agents_allocated: int = Field(default=0, ge=0)
    teams_created: int = Field(default=0, ge=0)
    messages_routed: int = Field(default=0, ge=0)
    negotiation_rounds: int = Field(default=0, ge=0)
    conflicts_resolved: int = Field(default=0, ge=0)
    work_stolen_count: int = Field(default=0, ge=0)

    model_config = {"frozen": True}
