"""
Domain Interfaces (Ports) for Execution.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.execution.domain.models import ExecutionEntity

class ExecutionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: ExecutionEntity) -> ExecutionEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[ExecutionEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[ExecutionEntity]:
        pass
