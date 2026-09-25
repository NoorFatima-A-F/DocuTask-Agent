"""
Execution Domain: Verification Execution, 9-State Lifecycle Machine, Retries, and Sourced Events.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uuid


class ExecutionState(str, Enum):
    CREATED = "CREATED"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    RETRYING = "RETRYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMED_OUT = "TIMED_OUT"


class ExecutionEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"ex_evt_{uuid.uuid4().hex[:8]}")
    execution_id: str
    event_type: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    payload: Dict[str, Any] = Field(default_factory=dict)
    actor: str = "ExecutionOrchestrator"


class ExecutionAttempt(BaseModel):
    attempt_id: str = Field(default_factory=lambda: f"att_{uuid.uuid4().hex[:8]}")
    execution_id: str
    attempt_number: int = 1
    started_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None
    duration_ms: float = 0.0
    is_success: bool = False
    failure_reason: Optional[str] = None


class VerificationExecution(BaseModel):
    execution_id: str = Field(default_factory=lambda: f"exec_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    verification_definition_id: str
    plan_id: str
    dataset_version_id: str
    environment_snapshot_id: str
    configuration_snapshot_id: str
    status: ExecutionState = ExecutionState.CREATED
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_ms: float = 0.0
    triggered_by: str = "Autonomous Verifier"
    attempts: List[ExecutionAttempt] = Field(default_factory=list)
    events: List[ExecutionEvent] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def start(self) -> None:
        self.status = ExecutionState.RUNNING
        self.started_at = datetime.now(timezone.utc).isoformat()

    def complete(self) -> None:
        self.status = ExecutionState.COMPLETED
        self.completed_at = datetime.now(timezone.utc).isoformat()

    def fail(self, reason: str) -> None:
        self.status = ExecutionState.FAILED
        self.completed_at = datetime.now(timezone.utc).isoformat()
