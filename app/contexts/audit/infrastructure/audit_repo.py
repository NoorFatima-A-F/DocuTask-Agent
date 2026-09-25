from typing import List, Optional
from ..domain.audit_domain import AuditRecordAggregate

class InMemoryAuditRepository:
    def __init__(self):
        self._chain: List[AuditRecordAggregate] = []

    def save(self, agg: AuditRecordAggregate) -> None:
        self._chain.append(agg)

    def get_latest(self) -> Optional[AuditRecordAggregate]:
        return self._chain[-1] if self._chain else None

    def list_all(self) -> List[AuditRecordAggregate]:
        return list(self._chain)
