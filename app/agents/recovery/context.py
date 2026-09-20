"""
Recovery Request, Context, and Result Domain Models.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.recovery.failure import Failure
from app.agents.recovery.lifecycle import RecoveryLifecycleState
from app.agents.recovery.metadata import RecoveryStatistics
from app.agents.recovery.recovery_strategy import RecoveryStrategy


class RecoveryContext(BaseModel):
    """Contextual parameters controlling autonomous recovery execution."""
    tenant_id: str = Field(default="default")
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    max_retries: int = Field(default=3, ge=0)
    allow_compensating_rollback: bool = Field(default=True)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    model_config = {"frozen": True}


class RecoveryRequest(BaseModel):
    """Request payload asking RecoveryEngine to diagnose and remediate a failure."""
    failure: Failure
    context: RecoveryContext = Field(default_factory=RecoveryContext)
    model_config = {"frozen": True}


class RecoveryResult(BaseModel):
    """Result payload emitted upon completion of a recovery operation."""
    recovery_id: UUID
    execution_id: UUID
    lifecycle_state: RecoveryLifecycleState = Field(default=RecoveryLifecycleState.COMPLETED)
    strategy_executed: RecoveryStrategy = Field(default=RecoveryStrategy.RETRY)
    is_remediated: bool = Field(default=True)
    statistics: RecoveryStatistics = Field(default_factory=RecoveryStatistics)
    messages: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}
