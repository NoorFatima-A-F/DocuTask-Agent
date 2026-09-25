from typing import Dict, Optional
from ..domain.execution_domain import ExecutionAggregate

class InMemoryExecutionRepository:
    def __init__(self):
        self._store: Dict[str, ExecutionAggregate] = {}

    def save(self, agg: ExecutionAggregate) -> None:
        self._store[agg.id] = agg

    def get(self, exec_id: str) -> Optional[ExecutionAggregate]:
        return self._store.get(exec_id)
