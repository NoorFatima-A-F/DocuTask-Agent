"""
Worker Lease Manager.
Manages time-bounded worker leases to prevent hanging task allocations.
"""

from datetime import datetime, timezone
from typing import Dict, Optional
from pydantic import BaseModel, Field


class WorkerLease(BaseModel):
    """Exclusive lease granted to an execution node on a worker."""
    lease_id: str
    worker_id: str
    node_id: str
    granted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    duration_seconds: float = Field(default=300.0, gt=0.0)
    model_config = {"frozen": True}


class WorkerLeaseManager:
    """Manages active leases and detects expired allocations."""

    def __init__(self):
        self._leases: Dict[str, WorkerLease] = {}

    def grant_lease(self, lease_id: str, worker_id: str, node_id: str, duration_seconds: float = 300.0) -> WorkerLease:
        lease = WorkerLease(
            lease_id=lease_id,
            worker_id=worker_id,
            node_id=node_id,
            duration_seconds=duration_seconds
        )
        self._leases[lease_id] = lease
        return lease

    def release_lease(self, lease_id: str) -> None:
        self._leases.pop(lease_id, None)

    def get_lease(self, lease_id: str) -> Optional[WorkerLease]:
        return self._leases.get(lease_id)
