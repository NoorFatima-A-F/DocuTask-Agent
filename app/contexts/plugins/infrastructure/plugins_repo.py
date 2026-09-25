from typing import Dict, List, Optional
from ..domain.plugins_domain import PluginRegistryAggregate

class InMemoryPluginRepository:
    def __init__(self):
        self._store: Dict[str, PluginRegistryAggregate] = {}

    def save(self, agg: PluginRegistryAggregate) -> None:
        self._store[agg.id] = agg

    def get(self, p_id: str) -> Optional[PluginRegistryAggregate]:
        return self._store.get(p_id)

    def list_active(self) -> List[PluginRegistryAggregate]:
        return list(self._store.values())
