"""
Domain Interfaces (Ports) for Rag.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.rag.domain.models import RagEntity

class RagRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: RagEntity) -> RagEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[RagEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[RagEntity]:
        pass
