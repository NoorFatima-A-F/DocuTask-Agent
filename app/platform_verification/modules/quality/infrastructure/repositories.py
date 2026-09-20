"""
In-Memory / Async SQLAlchemy Repository for Quality.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.quality.domain.models import QualityEntity
from app.platform_verification.modules.quality.domain.interfaces import QualityRepositoryInterface

class InMemoryQualityRepository(QualityRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, QualityEntity] = {}

    def save(self, entity: QualityEntity) -> QualityEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[QualityEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[QualityEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
