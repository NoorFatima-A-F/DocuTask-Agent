"""
Domain Interfaces (Ports) for Audit.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.audit.domain.models import AuditEntity

class AuditRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: AuditEntity) -> AuditEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[AuditEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[AuditEntity]:
        pass
