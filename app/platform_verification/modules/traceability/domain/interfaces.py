"""
Domain Interfaces (Ports) for Traceability.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.traceability.domain.models import TraceabilityEntity

class TraceabilityRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: TraceabilityEntity) -> TraceabilityEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[TraceabilityEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[TraceabilityEntity]:
        pass
