from typing import Dict, Optional
from ..domain.certification_domain import ComplianceCertificateAggregate

class InMemoryCertificationRepository:
    def __init__(self):
        self._store: Dict[str, ComplianceCertificateAggregate] = {}

    def save(self, agg: ComplianceCertificateAggregate) -> None:
        self._store[agg.id] = agg

    def get(self, c_id: str) -> Optional[ComplianceCertificateAggregate]:
        return self._store.get(c_id)
