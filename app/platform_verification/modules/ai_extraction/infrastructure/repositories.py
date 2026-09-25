"""
In-Memory / Async SQLAlchemy Repository for AiExtraction.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.ai_extraction.domain.models import AiExtractionEntity
from app.platform_verification.modules.ai_extraction.domain.interfaces import AiExtractionRepositoryInterface

class InMemoryAiExtractionRepository(AiExtractionRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, AiExtractionEntity] = {}

    def save(self, entity: AiExtractionEntity) -> AiExtractionEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[AiExtractionEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[AiExtractionEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
