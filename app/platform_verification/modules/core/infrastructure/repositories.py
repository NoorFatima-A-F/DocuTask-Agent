"""
In-Memory / Async SQLAlchemy Repository for Core.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.core.domain.models import CoreEntity
from app.platform_verification.modules.core.domain.interfaces import CoreRepositoryInterface

class InMemoryCoreRepository(CoreRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, CoreEntity] = {}

    def save(self, entity: CoreEntity) -> CoreEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[CoreEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[CoreEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
