"""
Application Use Cases & Workflows for Environments.
"""
from typing import List, Optional
from app.platform_verification.modules.environments.domain.models import EnvironmentsEntity
from app.platform_verification.modules.environments.domain.interfaces import EnvironmentsRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageEnvironmentsUseCase:
    def __init__(self, repository: EnvironmentsRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[EnvironmentsEntity, str]:
        try:
            entity = EnvironmentsEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[EnvironmentsEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[EnvironmentsEntity]:
        return self._repo.list_all(tenant_id)
