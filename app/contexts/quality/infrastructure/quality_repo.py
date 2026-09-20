from typing import Dict, Optional
from ..domain.quality_domain import QualityGateAggregate

class InMemoryQualityGateRepository:
    def __init__(self):
        self._store: Dict[str, QualityGateAggregate] = {}

    def save(self, agg: QualityGateAggregate) -> None:
        self._store[agg.id] = agg

    def get(self, g_id: str) -> Optional[QualityGateAggregate]:
        return self._store.get(g_id)
