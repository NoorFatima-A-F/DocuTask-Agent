"""
Application Use Cases & Workflows for Quality.
"""
from typing import List, Optional
from app.platform_verification.modules.quality.domain.models import QualityEntity
from app.platform_verification.modules.quality.domain.interfaces import QualityRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageQualityUseCase:
    def __init__(self, repository: QualityRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[QualityEntity, str]:
        try:
            entity = QualityEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[QualityEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[QualityEntity]:
        return self._repo.list_all(tenant_id)
