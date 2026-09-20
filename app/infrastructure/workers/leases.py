"""Worker Registration and Heartbeat Lease Management."""

from datetime import datetime, timezone, timedelta
import threading
from typing import Dict, List, Optional
from app.infrastructure.workers.models import WorkerLease


class WorkerLeaseManager:
    """Manages worker registration and heartbeat leases."""

    def __init__(self) -> None:
        self._leases: Dict[str, WorkerLease] = {}  # worker_id -> WorkerLease
        self._lock = threading.RLock()

    def issue_lease(
        self,
        worker_id: str,
        cluster_id: str,
        runtime_version: str = "3.1.0",
        ttl_seconds: int = 60,
    ) -> WorkerLease:
        """Issue a fresh lease for a registering worker."""
        with self._lock:
            now = datetime.now(timezone.utc)
            expires = now + timedelta(seconds=ttl_seconds)
            lease = WorkerLease(
                worker_id=worker_id,
                cluster_id=cluster_id,
                runtime_version=runtime_version,
                ttl_seconds=ttl_seconds,
                issued_at=now,
                last_renewed=now,
                expires_at=expires,
                is_valid=True,
            )
            self._leases[worker_id] = lease
            return lease

    def renew_lease(self, worker_id: str, ttl_seconds: Optional[int] = None) -> Optional[WorkerLease]:
        """Renew active lease on heartbeat."""
        with self._lock:
            lease = self._leases.get(worker_id)
            if not lease:
                return None
            now = datetime.now(timezone.utc)
            ttl = ttl_seconds or lease.ttl_seconds
            lease.last_renewed = now
            lease.ttl_seconds = ttl
            lease.expires_at = now + timedelta(seconds=ttl)
            lease.is_valid = True
            return lease

    def is_lease_valid(self, worker_id: str) -> bool:
        """Check if worker lease is active and non-expired."""
        with self._lock:
            lease = self._leases.get(worker_id)
            if not lease or not lease.is_valid:
                return False
            now = datetime.now(timezone.utc)
            elapsed = (now - lease.last_renewed).total_seconds()
            if elapsed > lease.ttl_seconds:
                lease.is_valid = False
                return False
            return True

    def get_lease(self, worker_id: str) -> Optional[WorkerLease]:
        with self._lock:
            return self._leases.get(worker_id)

    def revoke_lease(self, worker_id: str) -> bool:
        with self._lock:
            lease = self._leases.get(worker_id)
            if lease:
                lease.is_valid = False
                return True
            return False

    def find_expired_leases(self) -> List[str]:
        """Return list of worker IDs whose leases have expired."""
        with self._lock:
            expired = []
            for w_id in list(self._leases.keys()):
                if not self.is_lease_valid(w_id):
                    expired.append(w_id)
            return expired
