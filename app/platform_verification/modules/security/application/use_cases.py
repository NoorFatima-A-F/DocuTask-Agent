"""
Application Use Cases & Workflows for Security.
"""
from typing import List, Optional
from app.platform_verification.modules.security.domain.models import SecurityEntity
from app.platform_verification.modules.security.domain.interfaces import SecurityRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageSecurityUseCase:
    def __init__(self, repository: SecurityRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[SecurityEntity, str]:
        try:
            entity = SecurityEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[SecurityEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[SecurityEntity]:
        return self._repo.list_all(tenant_id)
