"""
In-Memory / Async SQLAlchemy Repository for Chaos.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.chaos.domain.models import ChaosEntity
from app.platform_verification.modules.chaos.domain.interfaces import ChaosRepositoryInterface

class InMemoryChaosRepository(ChaosRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, ChaosEntity] = {}

    def save(self, entity: ChaosEntity) -> ChaosEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[ChaosEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[ChaosEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
