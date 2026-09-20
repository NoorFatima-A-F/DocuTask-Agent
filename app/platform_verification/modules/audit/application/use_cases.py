"""
Application Use Cases & Workflows for Audit.
"""
from typing import List, Optional
from app.platform_verification.modules.audit.domain.models import AuditEntity
from app.platform_verification.modules.audit.domain.interfaces import AuditRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageAuditUseCase:
    def __init__(self, repository: AuditRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[AuditEntity, str]:
        try:
            entity = AuditEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[AuditEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[AuditEntity]:
        return self._repo.list_all(tenant_id)
