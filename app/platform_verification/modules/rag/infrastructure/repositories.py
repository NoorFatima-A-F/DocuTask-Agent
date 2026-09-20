"""
In-Memory / Async SQLAlchemy Repository for Rag.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.rag.domain.models import RagEntity
from app.platform_verification.modules.rag.domain.interfaces import RagRepositoryInterface

class InMemoryRagRepository(RagRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, RagEntity] = {}

    def save(self, entity: RagEntity) -> RagEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[RagEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[RagEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
