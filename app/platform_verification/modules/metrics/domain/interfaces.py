"""
Domain Interfaces (Ports) for Metrics.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.metrics.domain.models import MetricsEntity

class MetricsRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: MetricsEntity) -> MetricsEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[MetricsEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[MetricsEntity]:
        pass
