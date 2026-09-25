from typing import Dict, Optional
from ..domain.datasets_domain import DatasetAggregate

class InMemoryDatasetRepository:
    def __init__(self):
        self._store: Dict[str, DatasetAggregate] = {}

    def save(self, agg: DatasetAggregate) -> None:
        self._store[agg.id] = agg

    def get(self, ds_id: str) -> Optional[DatasetAggregate]:
        return self._store.get(ds_id)
