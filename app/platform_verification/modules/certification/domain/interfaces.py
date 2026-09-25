"""
Domain Interfaces (Ports) for Certification.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.certification.domain.models import CertificationEntity

class CertificationRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: CertificationEntity) -> CertificationEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[CertificationEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[CertificationEntity]:
        pass
