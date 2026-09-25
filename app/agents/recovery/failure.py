"""
Failure Domain Models.
Defines Failure, FailureIdentity, FailureEvidence, FailureSeverity, and FailureCategory.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class FailureSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class FailureCategory(str, Enum):
    TOOL_FAILURE = "ToolFailure"
    WORKER_FAILURE = "WorkerFailure"
    TIMEOUT_FAILURE = "TimeoutFailure"
    RESOURCE_FAILURE = "ResourceFailure"
    MEMORY_FAILURE = "MemoryFailure"
    TOKEN_BUDGET_FAILURE = "TokenBudgetFailure"
    SCHEDULING_FAILURE = "SchedulingFailure"
    DEPENDENCY_FAILURE = "DependencyFailure"
    APPROVAL_FAILURE = "ApprovalFailure"
    ROLLBACK_FAILURE = "RollbackFailure"
    CHECKPOINT_FAILURE = "CheckpointFailure"
    INFRASTRUCTURE_FAILURE = "InfrastructureFailure"
    PROVIDER_FAILURE = "ProviderFailure"
    EXECUTION_FAILURE = "ExecutionFailure"
    UNKNOWN_FAILURE = "UnknownFailure"


class FailureIdentity(BaseModel):
    """Unique identity of a detected runtime failure."""
    failure_id: UUID = Field(default_factory=uuid4)
    execution_id: UUID
    node_id: Optional[str] = None
    worker_id: Optional[str] = None
    tool_name: Optional[str] = None
    model_config = {"frozen": True}


class FailureEvidence(BaseModel):
    """Evidence and telemetry gathered around the point of failure."""
    error_type: str
    error_message: str
    stack_trace: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = {"frozen": True}


class Failure(BaseModel):
    """Canonical strongly typed Failure entity representing an execution fault."""
    identity: FailureIdentity
    category: FailureCategory = Field(default=FailureCategory.UNKNOWN_FAILURE)
    severity: FailureSeverity = Field(default=FailureSeverity.MEDIUM)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    recoverability_score: float = Field(default=0.8, ge=0.0, le=1.0)
    probable_cause: str = Field(default="Unspecified execution fault")
    evidence: FailureEvidence
    model_config = {"frozen": True}
