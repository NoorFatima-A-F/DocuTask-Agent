"""
Phase 13.18: Distributed Lock Manager (DLM)
Lease-based distributed locks with fencing tokens to prevent race conditions and duplicate execution.
"""

from __future__ import annotations
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional
from app.runtime.distributed.models.schemas import LockLease


class DistributedLockManager:
    """Manages distributed leases with auto-expiration and monotonically increasing fencing tokens."""

    def __init__(self):
        self._locks: Dict[str, LockLease] = {}
        self._fencing_counters: Dict[str, int] = {}

    def acquire_lock(self, lock_key: str, holder_id: str, lease_duration_sec: int = 15) -> Optional[LockLease]:
        now = datetime.now(timezone.utc)
        existing = self._locks.get(lock_key)

        # Check if existing lock is valid or expired
        if existing:
            try:
                exp = datetime.fromisoformat(existing.expires_at)
                if exp > now and existing.holder_id != holder_id:
                    # Lock held by someone else and not expired
                    return None
            except Exception:
                pass

        # Increment fencing token
        token = self._fencing_counters.get(lock_key, 0) + 1
        self._fencing_counters[lock_key] = token

        expires_at = (now + timedelta(seconds=lease_duration_sec)).isoformat()
        lease = LockLease(
            lock_key=lock_key,
            holder_id=holder_id,
            fencing_token=token,
            expires_at=expires_at,
            lease_duration_sec=lease_duration_sec,
        )
        self._locks[lock_key] = lease
        return lease

    def release_lock(self, lock_key: str, holder_id: str) -> bool:
        existing = self._locks.get(lock_key)
        if not existing:
            return True
        if existing.holder_id == holder_id:
            self._locks.pop(lock_key, None)
            return True
        return False

    def is_locked(self, lock_key: str) -> bool:
        existing = self._locks.get(lock_key)
        if not existing:
            return False
        try:
            exp = datetime.fromisoformat(existing.expires_at)
            return exp > datetime.now(timezone.utc)
        except Exception:
            return False
