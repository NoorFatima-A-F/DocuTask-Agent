"""
In-Memory / Async SQLAlchemy Repository for Evidence.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.evidence.domain.models import EvidenceEntity
from app.platform_verification.modules.evidence.domain.interfaces import EvidenceRepositoryInterface

class InMemoryEvidenceRepository(EvidenceRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, EvidenceEntity] = {}

    def save(self, entity: EvidenceEntity) -> EvidenceEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[EvidenceEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[EvidenceEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
