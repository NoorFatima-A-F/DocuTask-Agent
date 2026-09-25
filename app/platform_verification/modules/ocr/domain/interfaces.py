"""
Domain Interfaces (Ports) for Ocr.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.ocr.domain.models import OcrEntity

class OcrRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: OcrEntity) -> OcrEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[OcrEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[OcrEntity]:
        pass
