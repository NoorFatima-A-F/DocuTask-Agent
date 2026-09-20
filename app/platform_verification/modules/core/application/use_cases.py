"""
Application Use Cases & Workflows for Core.
"""
from typing import List, Optional
from app.platform_verification.modules.core.domain.models import CoreEntity
from app.platform_verification.modules.core.domain.interfaces import CoreRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageCoreUseCase:
    def __init__(self, repository: CoreRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[CoreEntity, str]:
        try:
            entity = CoreEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[CoreEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[CoreEntity]:
        return self._repo.list_all(tenant_id)
