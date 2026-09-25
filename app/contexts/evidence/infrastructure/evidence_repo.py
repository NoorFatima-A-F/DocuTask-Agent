from typing import Dict, Optional
from ..domain.evidence_domain import EvidenceAggregate

class InMemoryEvidenceRepository:
    def __init__(self):
        self._store: Dict[str, EvidenceAggregate] = {}

    def save(self, agg: EvidenceAggregate) -> None:
        self._store[agg.id] = agg

    def get(self, ev_id: str) -> Optional[EvidenceAggregate]:
        return self._store.get(ev_id)
