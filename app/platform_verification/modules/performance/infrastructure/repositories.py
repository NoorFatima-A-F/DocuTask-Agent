"""
In-Memory / Async SQLAlchemy Repository for Performance.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.performance.domain.models import PerformanceEntity
from app.platform_verification.modules.performance.domain.interfaces import PerformanceRepositoryInterface

class InMemoryPerformanceRepository(PerformanceRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, PerformanceEntity] = {}

    def save(self, entity: PerformanceEntity) -> PerformanceEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[PerformanceEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[PerformanceEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
