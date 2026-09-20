"""
In-Memory / Async SQLAlchemy Repository for Certification.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.certification.domain.models import CertificationEntity
from app.platform_verification.modules.certification.domain.interfaces import CertificationRepositoryInterface

class InMemoryCertificationRepository(CertificationRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, CertificationEntity] = {}

    def save(self, entity: CertificationEntity) -> CertificationEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[CertificationEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[CertificationEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
