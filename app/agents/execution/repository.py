"""
Execution Repository Abstraction.
Persists execution sessions, histories, checkpoints, and telemetry.
"""

from typing import Dict, List, Optional
from uuid import UUID
from app.agents.execution.context import ExecutionResult


class ExecutionRepository:
    """In-memory repository for execution sessions, cloud-database compatible."""

    def __init__(self):
        self._store: Dict[UUID, ExecutionResult] = {}

    async def save(self, result: ExecutionResult) -> None:
        self._store[result.execution_id] = result

    async def get(self, execution_id: UUID) -> Optional[ExecutionResult]:
        return self._store.get(execution_id)

    async def list_all(self) -> List[ExecutionResult]:
        return list(self._store.values())
