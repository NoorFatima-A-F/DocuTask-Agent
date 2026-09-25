"""
In-Memory / Async SQLAlchemy Repository for Traceability.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.traceability.domain.models import TraceabilityEntity
from app.platform_verification.modules.traceability.domain.interfaces import TraceabilityRepositoryInterface

class InMemoryTraceabilityRepository(TraceabilityRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, TraceabilityEntity] = {}

    def save(self, entity: TraceabilityEntity) -> TraceabilityEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[TraceabilityEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[TraceabilityEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
