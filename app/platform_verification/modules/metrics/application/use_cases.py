"""
Application Use Cases & Workflows for Metrics.
"""
from typing import List, Optional
from app.platform_verification.modules.metrics.domain.models import MetricsEntity
from app.platform_verification.modules.metrics.domain.interfaces import MetricsRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageMetricsUseCase:
    def __init__(self, repository: MetricsRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[MetricsEntity, str]:
        try:
            entity = MetricsEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[MetricsEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[MetricsEntity]:
        return self._repo.list_all(tenant_id)
