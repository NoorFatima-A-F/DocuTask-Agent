"""
Domain Interfaces (Ports) for Reporting.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.reporting.domain.models import ReportingEntity

class ReportingRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: ReportingEntity) -> ReportingEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[ReportingEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[ReportingEntity]:
        pass
