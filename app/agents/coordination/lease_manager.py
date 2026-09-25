"""
Lease Manager.
Manages distributed time-bound task and resource leases to prevent split-brain and duplicate execution.
"""

from datetime import datetime, timezone
from typing import Dict
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.coordination.exceptions import StaleLeaseError


class TaskLease(BaseModel):
    """Time-bounded lease granting exclusive execution rights for a task."""
    lease_id: UUID = Field(default_factory=uuid4)
    task_id: str
    holder_agent_id: UUID
    granted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at_timestamp: float

    def is_expired(self) -> bool:
        return datetime.now(timezone.utc).timestamp() > self.expires_at_timestamp


class LeaseManager:
    """Acquires, renews, and releases distributed task leases."""

    def __init__(self, default_lease_ttl_seconds: float = 60.0):
        self.default_ttl = default_lease_ttl_seconds
        self._leases: Dict[str, TaskLease] = {}

    def acquire_lease(self, task_id: str, agent_id: UUID) -> TaskLease:
        """Acquires a lease on a task if free or expired."""
        existing = self._leases.get(task_id)
        now = datetime.now(timezone.utc).timestamp()

        if existing and not existing.is_expired() and existing.holder_agent_id != agent_id:
            raise StaleLeaseError(
                f"Task '{task_id}' is actively leased to agent {existing.holder_agent_id}.",
                existing.holder_agent_id
            )

        lease = TaskLease(
            task_id=task_id,
            holder_agent_id=agent_id,
            expires_at_timestamp=now + self.default_ttl
        )
        self._leases[task_id] = lease
        return lease

    def validate_lease(self, task_id: str, agent_id: UUID) -> None:
        """Verifies agent currently holds a valid, non-expired lease on task."""
        lease = self._leases.get(task_id)
        if not lease or lease.holder_agent_id != agent_id or lease.is_expired():
            raise StaleLeaseError(f"Agent {agent_id} does not hold a valid lease for task '{task_id}'.", agent_id)

    def release_lease(self, task_id: str, agent_id: UUID) -> None:
        """Releases lease if held by agent."""
        lease = self._leases.get(task_id)
        if lease and lease.holder_agent_id == agent_id:
            del self._leases[task_id]
