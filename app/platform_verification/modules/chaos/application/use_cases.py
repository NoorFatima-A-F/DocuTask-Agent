"""
Application Use Cases & Workflows for Chaos.
"""
from typing import List, Optional
from app.platform_verification.modules.chaos.domain.models import ChaosEntity
from app.platform_verification.modules.chaos.domain.interfaces import ChaosRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageChaosUseCase:
    def __init__(self, repository: ChaosRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[ChaosEntity, str]:
        try:
            entity = ChaosEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[ChaosEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[ChaosEntity]:
        return self._repo.list_all(tenant_id)
