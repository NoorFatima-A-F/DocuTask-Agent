"""
Domain Interfaces (Ports) for Datasets.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.datasets.domain.models import DatasetsEntity

class DatasetsRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: DatasetsEntity) -> DatasetsEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[DatasetsEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[DatasetsEntity]:
        pass
