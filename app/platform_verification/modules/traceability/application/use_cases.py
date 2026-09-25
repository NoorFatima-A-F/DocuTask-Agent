"""
Application Use Cases & Workflows for Traceability.
"""
from typing import List, Optional
from app.platform_verification.modules.traceability.domain.models import TraceabilityEntity
from app.platform_verification.modules.traceability.domain.interfaces import TraceabilityRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageTraceabilityUseCase:
    def __init__(self, repository: TraceabilityRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[TraceabilityEntity, str]:
        try:
            entity = TraceabilityEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[TraceabilityEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[TraceabilityEntity]:
        return self._repo.list_all(tenant_id)
