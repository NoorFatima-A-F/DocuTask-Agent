"""
In-Memory / Async SQLAlchemy Repository for Reporting.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.reporting.domain.models import ReportingEntity
from app.platform_verification.modules.reporting.domain.interfaces import ReportingRepositoryInterface

class InMemoryReportingRepository(ReportingRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, ReportingEntity] = {}

    def save(self, entity: ReportingEntity) -> ReportingEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[ReportingEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[ReportingEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
