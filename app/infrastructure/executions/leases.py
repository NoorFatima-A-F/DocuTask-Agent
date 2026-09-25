"""Execution Lease Management for Single-Owner Task Execution."""

from datetime import datetime, timezone, timedelta
from enum import Enum
import secrets
import threading
from typing import Dict, Optional
from pydantic import BaseModel, Field


class ExecutionLeaseStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    RELEASED = "RELEASED"
    REVOKED = "REVOKED"


class ExecutionLease(BaseModel):
    """Cryptographic single-owner execution lease for a workload assignment."""

    lease_id: str = Field(default_factory=lambda: f"exl_{secrets.token_hex(8)}")
    workload_id: str
    worker_id: str
    attempt: int = 1
    ttl_seconds: int = 120
    status: ExecutionLeaseStatus = ExecutionLeaseStatus.ACTIVE
    issued_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(seconds=120))
    last_renewed: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ExecutionLeaseManager:
    """Enforces that exactly one worker holds the valid execution lease for a workload attempt."""

    def __init__(self) -> None:
        self._leases: Dict[str, ExecutionLease] = {}  # lease_id -> ExecutionLease
        self._workload_to_lease: Dict[str, str] = {}  # workload_id -> active lease_id
        self._lock = threading.RLock()

    def issue_execution_lease(
        self,
        workload_id: str,
        worker_id: str,
        attempt: int = 1,
        ttl_seconds: int = 120,
    ) -> ExecutionLease:
        """Issue an execution lease, revoking any existing active lease for this workload."""
        with self._lock:
            # Revoke previous lease if exists
            prev_lease_id = self._workload_to_lease.get(workload_id)
            if prev_lease_id and prev_lease_id in self._leases:
                self._leases[prev_lease_id].status = ExecutionLeaseStatus.REVOKED

            now = datetime.now(timezone.utc)
            lease = ExecutionLease(
                workload_id=workload_id,
                worker_id=worker_id,
                attempt=attempt,
                ttl_seconds=ttl_seconds,
                status=ExecutionLeaseStatus.ACTIVE,
                issued_at=now,
                last_renewed=now,
                expires_at=now + timedelta(seconds=ttl_seconds),
            )
            self._leases[lease.lease_id] = lease
            self._workload_to_lease[workload_id] = lease.lease_id
            return lease

    def renew_execution_lease(self, lease_id: str, ttl_seconds: Optional[int] = None) -> Optional[ExecutionLease]:
        """Renew active execution lease."""
        with self._lock:
            lease = self._leases.get(lease_id)
            if not lease or lease.status != ExecutionLeaseStatus.ACTIVE:
                return None
            now = datetime.now(timezone.utc)
            ttl = ttl_seconds or lease.ttl_seconds
            lease.last_renewed = now
            lease.ttl_seconds = ttl
            lease.expires_at = now + timedelta(seconds=ttl)
            return lease

    def is_lease_valid(self, lease_id: str) -> bool:
        """Check if lease is ACTIVE and non-expired."""
        with self._lock:
            lease = self._leases.get(lease_id)
            if not lease or lease.status != ExecutionLeaseStatus.ACTIVE:
                return False
            now = datetime.now(timezone.utc)
            if now > lease.expires_at:
                lease.status = ExecutionLeaseStatus.EXPIRED
                return False
            return True

    def release_lease(self, lease_id: str) -> bool:
        """Explicitly release execution lease upon task completion or termination."""
        with self._lock:
            lease = self._leases.get(lease_id)
            if not lease:
                return False
            lease.status = ExecutionLeaseStatus.RELEASED
            if self._workload_to_lease.get(lease.workload_id) == lease_id:
                self._workload_to_lease.pop(lease.workload_id, None)
            return True

    def get_active_lease_for_workload(self, workload_id: str) -> Optional[ExecutionLease]:
        with self._lock:
            lease_id = self._workload_to_lease.get(workload_id)
            if not lease_id:
                return None
            if self.is_lease_valid(lease_id):
                return self._leases.get(lease_id)
            return None
