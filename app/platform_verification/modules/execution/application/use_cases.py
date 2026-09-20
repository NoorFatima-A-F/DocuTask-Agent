"""
Application Use Cases & Workflows for Execution.
"""
from typing import List, Optional
from app.platform_verification.modules.execution.domain.models import ExecutionEntity
from app.platform_verification.modules.execution.domain.interfaces import ExecutionRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageExecutionUseCase:
    def __init__(self, repository: ExecutionRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[ExecutionEntity, str]:
        try:
            entity = ExecutionEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[ExecutionEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[ExecutionEntity]:
        return self._repo.list_all(tenant_id)
