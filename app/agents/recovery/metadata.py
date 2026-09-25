"""
Recovery Metadata, Identity, and Statistics Domain Models.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class RecoveryIdentity(BaseModel):
    """Immutable identity identifying a recovery session across distributed recovery coordinators."""
    recovery_id: UUID = Field(default_factory=uuid4)
    execution_id: UUID
    incident_id: Optional[UUID] = Field(default=None)
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    tenant_id: str = Field(default="default")
    version: str = Field(default="v1.0")
    model_config = {"frozen": True}


class RecoveryStatistics(BaseModel):
    """Telemetry tracking recovery latency, retry counts, and MTTR."""
    diagnosis_duration_ms: float = Field(default=0.0, ge=0.0)
    strategy_selection_duration_ms: float = Field(default=0.0, ge=0.0)
    execution_recovery_duration_ms: float = Field(default=0.0, ge=0.0)
    total_mttr_ms: float = Field(default=0.0, ge=0.0)
    retry_attempts: int = Field(default=0, ge=0)
    checkpoints_evaluated: int = Field(default=0, ge=0)
    nodes_compensated: int = Field(default=0, ge=0)
    model_config = {"frozen": True}


class RecoveryMetadata(BaseModel):
    """Audit metadata describing recovery context and environmental attributes."""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = Field(default=None)
    recovery_trigger: str = Field(default="EXECUTION_FAILURE_EVENT")
    tags: List[str] = Field(default_factory=list)
    labels: Dict[str, str] = Field(default_factory=dict)
    custom: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}
