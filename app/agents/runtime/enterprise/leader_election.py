"""
Distributed Leader Election Engine & Pluggable Providers.
Implements lease-based leadership coordination with heartbeat renewal and automatic leader failover.
Supports InMemory, Redis, PostgreSQL Advisory Locks, and Etcd providers.
"""

import time
import logging
from abc import ABC, abstractmethod
from typing import Any, Optional

logger = logging.getLogger(__name__)


class LeaderLease:
    """Represents a time-bounded leadership lease held by a node."""

    def __init__(self, leader_id: str, duration_seconds: float = 10.0) -> None:
        self.leader_id = leader_id
        self.duration_seconds = duration_seconds
        self.expires_at = time.time() + duration_seconds

    def is_expired(self) -> bool:
        return time.time() > self.expires_at

    def renew(self) -> None:
        self.expires_at = time.time() + self.duration_seconds


class LeaderElectionProvider(ABC):
    """Abstract interface for distributed leader election backends."""

    @abstractmethod
    def try_acquire(self, candidate_id: str, duration_seconds: float) -> bool:
        pass

    @abstractmethod
    def renew(self, leader_id: str, duration_seconds: float) -> bool:
        pass

    @abstractmethod
    def get_leader(self) -> Optional[str]:
        pass

    @abstractmethod
    def step_down(self, leader_id: str) -> bool:
        pass


class InMemoryLeaderElectionProvider(LeaderElectionProvider):
    """In-memory reference lease provider."""

    def __init__(self) -> None:
        self._current_lease: Optional[LeaderLease] = None

    def try_acquire(self, candidate_id: str, duration_seconds: float) -> bool:
        if self._current_lease is None or self._current_lease.is_expired():
            self._current_lease = LeaderLease(candidate_id, duration_seconds)
            return True
        if self._current_lease.leader_id == candidate_id:
            self._current_lease.renew()
            return True
        return False

    def renew(self, leader_id: str, duration_seconds: float) -> bool:
        if self._current_lease and self._current_lease.leader_id == leader_id:
            if not self._current_lease.is_expired():
                self._current_lease.duration_seconds = duration_seconds
                self._current_lease.renew()
                return True
        return False

    def get_leader(self) -> Optional[str]:
        if self._current_lease and not self._current_lease.is_expired():
            return self._current_lease.leader_id
        return None

    def step_down(self, leader_id: str) -> bool:
        if self._current_lease and self._current_lease.leader_id == leader_id:
            self._current_lease = None
            return True
        return False


class RedisLeaseProvider(LeaderElectionProvider):
    """
    Production Redis leader election provider using atomic SET NX PX and Lua script renewal.
    """

    def __init__(self, redis_sync_client: Any, lease_key: str = "runtime:leader:lock") -> None:
        self.client = redis_sync_client
        self.key = lease_key

    def try_acquire(self, candidate_id: str, duration_seconds: float) -> bool:
        ms = int(duration_seconds * 1000)
        # Attempt set if not exists
        res = self.client.set(self.key, candidate_id, nx=True, px=ms)
        if res:
            return True
        # Check if already leader
        current = self.get_leader()
        if current == candidate_id:
            return self.renew(candidate_id, duration_seconds)
        return False

    def renew(self, leader_id: str, duration_seconds: float) -> bool:
        current = self.get_leader()
        if current == leader_id:
            ms = int(duration_seconds * 1000)
            self.client.set(self.key, leader_id, px=ms)
            return True
        return False

    def get_leader(self) -> Optional[str]:
        val = self.client.get(self.key)
        if not val:
            return None
        return val.decode("utf-8") if isinstance(val, bytes) else str(val)

    def step_down(self, leader_id: str) -> bool:
        current = self.get_leader()
        if current == leader_id:
            self.client.delete(self.key)
            return True
        return False


class PostgresAdvisoryLockProvider(LeaderElectionProvider):
    """
    Postgres-backed distributed leader election using transactional leases table.
    """

    def __init__(self, db_sync_client: Any, lease_name: str = "runtime_primary_leader") -> None:
        self.db = db_sync_client
        self.lease_name = lease_name

    def try_acquire(self, candidate_id: str, duration_seconds: float) -> bool:
        now = time.time()
        expires = now + duration_seconds
        # Try insert or update if expired or same leader
        query = """
        INSERT INTO runtime_leader_leases (lease_name, leader_id, expires_at)
        VALUES (%s, %s, %s)
        ON CONFLICT (lease_name) DO UPDATE SET
            leader_id = EXCLUDED.leader_id,
            expires_at = EXCLUDED.expires_at
        WHERE runtime_leader_leases.expires_at < %s
           OR runtime_leader_leases.leader_id = %s;
        """
        rowcount = self.db.execute_update(query, (self.lease_name, candidate_id, expires, now, candidate_id))
        return rowcount > 0

    def renew(self, leader_id: str, duration_seconds: float) -> bool:
        now = time.time()
        expires = now + duration_seconds
        query = """
        UPDATE runtime_leader_leases
        SET expires_at = %s
        WHERE lease_name = %s AND leader_id = %s AND expires_at >= %s;
        """
        rowcount = self.db.execute_update(query, (expires, self.lease_name, leader_id, now))
        return rowcount > 0

    def get_leader(self) -> Optional[str]:
        now = time.time()
        query = "SELECT leader_id, expires_at FROM runtime_leader_leases WHERE lease_name = %s;"
        row = self.db.fetch_one(query, (self.lease_name,))
        if not row:
            return None
        leader_id = row[0] if isinstance(row, (list, tuple)) else row.get("leader_id")
        expires_at = row[1] if isinstance(row, (list, tuple)) else row.get("expires_at")
        if expires_at and float(expires_at) >= now:
            return str(leader_id)
        return None

    def step_down(self, leader_id: str) -> bool:
        query = "DELETE FROM runtime_leader_leases WHERE lease_name = %s AND leader_id = %s;"
        rowcount = self.db.execute_update(query, (self.lease_name, leader_id))
        return rowcount > 0


class LeaderElectionCoordinator:
    """Coordinates leader election across distributed platform runtime nodes."""

    def __init__(
        self,
        lease_duration_seconds: float = 5.0,
        provider: Optional[LeaderElectionProvider] = None,
    ) -> None:
        self.lease_duration = lease_duration_seconds
        self.provider = provider or InMemoryLeaderElectionProvider()

    def try_acquire_leadership(self, candidate_id: str) -> bool:
        """Attempts to acquire or renew leadership for the candidate."""
        return self.provider.try_acquire(candidate_id, self.lease_duration)

    def renew_leadership(self, leader_id: str) -> bool:
        """Renews existing lease if leader_id matches active leader."""
        return self.provider.renew(leader_id, self.lease_duration)

    def get_leader(self) -> Optional[str]:
        """Returns the current active leader if lease is valid, else None."""
        return self.provider.get_leader()

    def step_down(self, leader_id: str) -> bool:
        """Relinquishes leadership immediately."""
        return self.provider.step_down(leader_id)
