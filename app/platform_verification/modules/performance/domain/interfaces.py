"""
Domain Interfaces (Ports) for Performance.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.performance.domain.models import PerformanceEntity

class PerformanceRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: PerformanceEntity) -> PerformanceEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[PerformanceEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[PerformanceEntity]:
        pass
