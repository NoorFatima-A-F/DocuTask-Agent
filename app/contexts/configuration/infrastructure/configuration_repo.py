from typing import Dict, Optional
from ..domain.configuration_domain import ConfigurationAggregate

class InMemoryConfigurationRepository:
    def __init__(self):
        self._store: Dict[str, ConfigurationAggregate] = {}

    def save(self, agg: ConfigurationAggregate) -> None:
        self._store[agg.id] = agg

    def get(self, config_id: str) -> Optional[ConfigurationAggregate]:
        return self._store.get(config_id)
