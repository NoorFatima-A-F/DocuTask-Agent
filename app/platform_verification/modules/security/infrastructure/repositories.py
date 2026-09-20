"""
In-Memory / Async SQLAlchemy Repository for Security.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.security.domain.models import SecurityEntity
from app.platform_verification.modules.security.domain.interfaces import SecurityRepositoryInterface

class InMemorySecurityRepository(SecurityRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, SecurityEntity] = {}

    def save(self, entity: SecurityEntity) -> SecurityEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[SecurityEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[SecurityEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
