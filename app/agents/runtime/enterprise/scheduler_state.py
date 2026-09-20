"""
Distributed Scheduler State Models.
Defines persistent scheduled jobs, execution priorities, retry policies, and worker allocations.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class JobPriority(int, Enum):
    """Job execution priority order (lower value = higher priority)."""
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4


class JobStatus(str, Enum):
    """Lifecycle status of a scheduled job."""
    PENDING = "PENDING"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class ScheduledJob(BaseModel):
    """Persistent job definition managed by the Distributed Scheduler."""
    job_id: UUID = Field(default_factory=uuid4)
    name: str
    tenant_id: str = "default"
    priority: JobPriority = JobPriority.NORMAL
    status: JobStatus = JobStatus.PENDING
    payload: Dict[str, Any] = Field(default_factory=dict)
    run_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    max_retries: int = 3
    retry_count: int = 0
    assigned_worker: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

    def mark_scheduled(self, worker_id: str) -> "ScheduledJob":
        return self.model_copy(
            update={"status": JobStatus.SCHEDULED, "assigned_worker": worker_id}
        )

    def mark_running(self) -> "ScheduledJob":
        return self.model_copy(update={"status": JobStatus.RUNNING})

    def mark_completed(self) -> "ScheduledJob":
        return self.model_copy(
            update={
                "status": JobStatus.COMPLETED,
                "completed_at": datetime.now(timezone.utc),
            }
        )

    def mark_failed(self) -> "ScheduledJob":
        new_retries = self.retry_count + 1
        new_status = JobStatus.FAILED if new_retries >= self.max_retries else JobStatus.PENDING
        return self.model_copy(
            update={"status": new_status, "retry_count": new_retries}
        )

    model_config = {"frozen": True}
