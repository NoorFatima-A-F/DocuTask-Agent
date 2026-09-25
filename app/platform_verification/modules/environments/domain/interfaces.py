"""
Domain Interfaces (Ports) for Environments.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.environments.domain.models import EnvironmentsEntity

class EnvironmentsRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: EnvironmentsEntity) -> EnvironmentsEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[EnvironmentsEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[EnvironmentsEntity]:
        pass
