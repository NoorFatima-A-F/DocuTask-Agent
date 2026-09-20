"""
In-Memory / Async SQLAlchemy Repository for Ocr.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.ocr.domain.models import OcrEntity
from app.platform_verification.modules.ocr.domain.interfaces import OcrRepositoryInterface

class InMemoryOcrRepository(OcrRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, OcrEntity] = {}

    def save(self, entity: OcrEntity) -> OcrEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[OcrEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[OcrEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
