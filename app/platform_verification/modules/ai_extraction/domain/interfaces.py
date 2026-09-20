"""
Domain Interfaces (Ports) for AiExtraction.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.ai_extraction.domain.models import AiExtractionEntity

class AiExtractionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: AiExtractionEntity) -> AiExtractionEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[AiExtractionEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[AiExtractionEntity]:
        pass
