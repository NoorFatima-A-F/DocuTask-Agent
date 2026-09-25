from typing import Dict, List
from ..domain.metrics_domain import MetricAggregate

class InMemoryMetricsRepository:
    def __init__(self):
        self._store: Dict[str, MetricAggregate] = {}

    def save(self, agg: MetricAggregate) -> None:
        self._store[agg.id] = agg

    def get_by_run(self, run_id: str) -> List[MetricAggregate]:
        return [m for m in self._store.values() if m.run_id == run_id]
