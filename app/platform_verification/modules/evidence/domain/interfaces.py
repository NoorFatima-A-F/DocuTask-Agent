"""
Domain Interfaces (Ports) for Evidence.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.evidence.domain.models import EvidenceEntity

class EvidenceRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: EvidenceEntity) -> EvidenceEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[EvidenceEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[EvidenceEntity]:
        pass
