"""
In-Memory / Async SQLAlchemy Repository for Metrics.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.metrics.domain.models import MetricsEntity
from app.platform_verification.modules.metrics.domain.interfaces import MetricsRepositoryInterface

class InMemoryMetricsRepository(MetricsRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, MetricsEntity] = {}

    def save(self, entity: MetricsEntity) -> MetricsEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[MetricsEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[MetricsEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
