"""
Recovery Repository Abstraction.
Persists recovery sessions, incidents, failure records, and dead-letter entities.
"""

from typing import Dict, List, Optional
from uuid import UUID
from app.agents.recovery.context import RecoveryResult


class RecoveryRepository:
    """In-memory repository for recovery sessions, cloud-database compatible."""

    def __init__(self):
        self._store: Dict[UUID, RecoveryResult] = {}

    async def save(self, result: RecoveryResult) -> None:
        self._store[result.recovery_id] = result

    async def get(self, recovery_id: UUID) -> Optional[RecoveryResult]:
        return self._store.get(recovery_id)

    async def list_all(self) -> List[RecoveryResult]:
        return list(self._store.values())
