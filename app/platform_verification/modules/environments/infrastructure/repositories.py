"""
In-Memory / Async SQLAlchemy Repository for Environments.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.environments.domain.models import EnvironmentsEntity
from app.platform_verification.modules.environments.domain.interfaces import EnvironmentsRepositoryInterface

class InMemoryEnvironmentsRepository(EnvironmentsRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, EnvironmentsEntity] = {}

    def save(self, entity: EnvironmentsEntity) -> EnvironmentsEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[EnvironmentsEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[EnvironmentsEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
