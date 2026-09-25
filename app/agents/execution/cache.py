"""
Execution Cache.
In-memory fast lookup cache for active execution results and statuses.
"""

from typing import Dict, Optional
from uuid import UUID
from app.agents.execution.context import ExecutionResult


class ExecutionCache:
    """Fast cache storing recent execution results."""

    def __init__(self):
        self._cache: Dict[UUID, ExecutionResult] = {}

    def get(self, execution_id: UUID) -> Optional[ExecutionResult]:
        return self._cache.get(execution_id)

    def set(self, execution_id: UUID, result: ExecutionResult) -> None:
        self._cache[execution_id] = result

    def clear(self) -> None:
        self._cache.clear()
