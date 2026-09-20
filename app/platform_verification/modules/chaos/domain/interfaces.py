"""
Domain Interfaces (Ports) for Chaos.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.chaos.domain.models import ChaosEntity

class ChaosRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: ChaosEntity) -> ChaosEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[ChaosEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[ChaosEntity]:
        pass
