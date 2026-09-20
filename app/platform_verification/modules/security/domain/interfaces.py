"""
Domain Interfaces (Ports) for Security.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.security.domain.models import SecurityEntity

class SecurityRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: SecurityEntity) -> SecurityEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[SecurityEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[SecurityEntity]:
        pass
