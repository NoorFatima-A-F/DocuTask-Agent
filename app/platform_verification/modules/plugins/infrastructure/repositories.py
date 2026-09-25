"""
In-Memory / Async SQLAlchemy Repository for Plugins.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.plugins.domain.models import PluginsEntity
from app.platform_verification.modules.plugins.domain.interfaces import PluginsRepositoryInterface

class InMemoryPluginsRepository(PluginsRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, PluginsEntity] = {}

    def save(self, entity: PluginsEntity) -> PluginsEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[PluginsEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[PluginsEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
