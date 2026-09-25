"""
Workflow Metadata and Telemetry Models.
Defines identity envelopes, cloud deployment metadata, and quantitative runtime statistics.
"""

from enum import Enum
from datetime import datetime, timezone
from typing import Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class WorkflowPriority(int, Enum):
    """Execution priority levels for workflows."""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4


class WorkflowIdentity(BaseModel):

    """Unique identity and correlation envelope for a workflow instance."""
    workflow_id: UUID = Field(default_factory=uuid4)
    instance_id: UUID = Field(default_factory=uuid4)
    parent_workflow_id: Optional[UUID] = None
    name: str
    version: str = Field(default="1.0.0")
    tenant_id: str = Field(default="default")
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}


class WorkflowMetadata(BaseModel):
    """Execution environment and version metadata."""
    engine_version: str = Field(default="22.0.0")
    cloud_region: str = Field(default="us-central1")
    environment: str = Field(default="production")
    tags: Dict[str, str] = Field(default_factory=dict)

    model_config = {"frozen": True}


class WorkflowStatistics(BaseModel):
    """Quantitative metrics for a workflow run."""
    total_duration_ms: float = Field(default=0.0, ge=0.0)
    steps_executed: int = Field(default=0, ge=0)
    child_workflows_spawned: int = Field(default=0, ge=0)
    compensations_executed: int = Field(default=0, ge=0)
    signals_received: int = Field(default=0, ge=0)
    timers_fired: int = Field(default=0, ge=0)
    checkpoints_saved: int = Field(default=0, ge=0)

    model_config = {"frozen": True}
