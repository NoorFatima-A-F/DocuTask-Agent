from typing import Dict, Optional
from ..domain.environments_domain import EnvironmentAggregate

class InMemoryEnvironmentRepository:
    def __init__(self):
        self._store: Dict[str, EnvironmentAggregate] = {}

    def save(self, agg: EnvironmentAggregate) -> None:
        self._store[agg.id] = agg

    def get(self, env_id: str) -> Optional[EnvironmentAggregate]:
        return self._store.get(env_id)
