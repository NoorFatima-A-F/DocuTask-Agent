"""
Application Use Cases & Workflows for Reporting.
"""
from typing import List, Optional
from app.platform_verification.modules.reporting.domain.models import ReportingEntity
from app.platform_verification.modules.reporting.domain.interfaces import ReportingRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageReportingUseCase:
    def __init__(self, repository: ReportingRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[ReportingEntity, str]:
        try:
            entity = ReportingEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[ReportingEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[ReportingEntity]:
        return self._repo.list_all(tenant_id)
