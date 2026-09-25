from typing import Dict, Optional
from ..domain.statistics_domain import StatisticalAggregate

class InMemoryStatisticsRepository:
    def __init__(self):
        self._store: Dict[str, StatisticalAggregate] = {}

    def save(self, agg: StatisticalAggregate) -> None:
        self._store[agg.id] = agg

    def get(self, a_id: str) -> Optional[StatisticalAggregate]:
        return self._store.get(a_id)
