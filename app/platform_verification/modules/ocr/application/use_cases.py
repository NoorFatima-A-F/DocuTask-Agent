"""
Application Use Cases & Workflows for Ocr.
"""
from typing import List, Optional
from app.platform_verification.modules.ocr.domain.models import OcrEntity
from app.platform_verification.modules.ocr.domain.interfaces import OcrRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageOcrUseCase:
    def __init__(self, repository: OcrRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[OcrEntity, str]:
        try:
            entity = OcrEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[OcrEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[OcrEntity]:
        return self._repo.list_all(tenant_id)
