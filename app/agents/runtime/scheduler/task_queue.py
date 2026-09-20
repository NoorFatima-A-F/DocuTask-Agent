"""
Task Queue Backend Contract for Enterprise Distributed Scheduler.
Defines distributed lease semantics, retry budgets, dead-letter queueing, and lease heartbeating.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from app.agents.runtime.enterprise.scheduler_state import ScheduledJob, JobStatus


class TaskLease(BaseModel):
    """Represents a time-bounded distributed lease granted to a worker."""
    job_id: UUID
    worker_id: str
    acquired_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime
    renewal_count: int = 0


class TaskQueueBackend(ABC):
    """Abstract interface for distributed task queue backends."""

    @abstractmethod
    async def enqueue(self, job: ScheduledJob) -> None:
        """Enqueues a job into the backend with its priority and scheduled run_at time."""
        pass

    @abstractmethod
    async def dequeue_with_lease(
        self,
        worker_id: str,
        lease_duration_seconds: float = 30.0,
    ) -> Optional[ScheduledJob]:
        """
        Atomically dequeues the highest priority eligible job and acquires a lease for worker_id.
        Returns None if no eligible job is available.
        """
        pass

    @abstractmethod
    async def renew_lease(
        self,
        job_id: UUID,
        worker_id: str,
        extension_seconds: float = 30.0,
    ) -> bool:
        """Extends an active lease for worker_id. Returns False if lease expired or was reclaimed."""
        pass

    @abstractmethod
    async def complete_job(self, job_id: UUID, worker_id: str) -> bool:
        """Marks a leased job as successfully completed and releases the lease."""
        pass

    @abstractmethod
    async def fail_job(self, job_id: UUID, worker_id: str, error_message: str) -> bool:
        """
        Handles job execution failure. If retries remain, re-queues with backoff.
        If retries exhausted, routes to Dead-Letter Queue (DLQ).
        """
        pass

    @abstractmethod
    async def reclaim_expired_leases(self) -> int:
        """
        Scans for leased jobs whose expiration time has passed without completion or renewal.
        Reclaims them for re-assignment. Returns the count of reclaimed jobs.
        """
        pass

    @abstractmethod
    async def get_job(self, job_id: UUID) -> Optional[ScheduledJob]:
        """Fetches job metadata by UUID."""
        pass

    @abstractmethod
    async def get_dlq_jobs(self) -> List[ScheduledJob]:
        """Returns all jobs routed to the Dead-Letter Queue."""
        pass
