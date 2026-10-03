"""
Domain Interfaces (Ports) for Core.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.core.domain.models import CoreEntity

class CoreRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: CoreEntity) -> CoreEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[CoreEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[CoreEntity]:
        pass
