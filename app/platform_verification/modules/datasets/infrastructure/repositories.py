"""
In-Memory / Async SQLAlchemy Repository for Datasets.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.datasets.domain.models import DatasetsEntity
from app.platform_verification.modules.datasets.domain.interfaces import DatasetsRepositoryInterface

class InMemoryDatasetsRepository(DatasetsRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, DatasetsEntity] = {}

    def save(self, entity: DatasetsEntity) -> DatasetsEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[DatasetsEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[DatasetsEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
