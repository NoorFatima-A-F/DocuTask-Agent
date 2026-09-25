"""
Application Use Cases & Workflows for Performance.
"""
from typing import List, Optional
from app.platform_verification.modules.performance.domain.models import PerformanceEntity
from app.platform_verification.modules.performance.domain.interfaces import PerformanceRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManagePerformanceUseCase:
    def __init__(self, repository: PerformanceRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[PerformanceEntity, str]:
        try:
            entity = PerformanceEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[PerformanceEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[PerformanceEntity]:
        return self._repo.list_all(tenant_id)
