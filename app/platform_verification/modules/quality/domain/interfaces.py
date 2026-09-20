"""
Domain Interfaces (Ports) for Quality.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.quality.domain.models import QualityEntity

class QualityRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: QualityEntity) -> QualityEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[QualityEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[QualityEntity]:
        pass
