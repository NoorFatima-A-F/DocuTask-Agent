"""
Recovery Cache.
In-memory cache for recent failure classifications and recovery results.
"""

from typing import Dict, Optional
from uuid import UUID
from app.agents.recovery.context import RecoveryResult


class RecoveryCache:
    """In-memory cache for fast lookup of recovery results."""

    def __init__(self):
        self._cache: Dict[UUID, RecoveryResult] = {}

    def get(self, recovery_id: UUID) -> Optional[RecoveryResult]:
        return self._cache.get(recovery_id)

    def set(self, recovery_id: UUID, result: RecoveryResult) -> None:
        self._cache[recovery_id] = result

    def clear(self) -> None:
        self._cache.clear()
