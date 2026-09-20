"""
Execution Metadata, Identity, and Statistics Domain Models.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ExecutionIdentity(BaseModel):
    """Immutable identity identifying an execution session across distributed workers."""
    execution_id: UUID = Field(default_factory=uuid4)
    plan_id: UUID
    session_id: Optional[str] = Field(default=None)
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    tenant_id: str = Field(default="default")
    actor: str = Field(default="system")
    version: str = Field(default="v1.0")
    model_config = {"frozen": True}


class ExecutionStatistics(BaseModel):
    """Runtime execution statistics and resource consumption telemetry."""
    total_nodes_count: int = Field(default=0, ge=0)
    completed_nodes_count: int = Field(default=0, ge=0)
    failed_nodes_count: int = Field(default=0, ge=0)
    retried_nodes_count: int = Field(default=0, ge=0)
    total_duration_seconds: float = Field(default=0.0, ge=0.0)
    total_tokens_consumed: int = Field(default=0, ge=0)
    total_cost_usd: float = Field(default=0.0, ge=0.0)
    peak_memory_mb: float = Field(default=0.0, ge=0.0)
    active_worker_count: int = Field(default=0, ge=0)
    model_config = {"frozen": True}


class ExecutionMetadata(BaseModel):
    """Runtime execution metadata and auditing headers."""
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = Field(default=None)
    environment: str = Field(default="PRODUCTION")
    priority: str = Field(default="MEDIUM")
    tags: List[str] = Field(default_factory=list)
    labels: Dict[str, str] = Field(default_factory=dict)
    custom: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}
