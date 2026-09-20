"""
In-Memory / Async SQLAlchemy Repository for Audit.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.audit.domain.models import AuditEntity
from app.platform_verification.modules.audit.domain.interfaces import AuditRepositoryInterface

class InMemoryAuditRepository(AuditRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, AuditEntity] = {}

    def save(self, entity: AuditEntity) -> AuditEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[AuditEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[AuditEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
