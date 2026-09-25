"""
Application Use Cases & Workflows for Rag.
"""
from typing import List, Optional
from app.platform_verification.modules.rag.domain.models import RagEntity
from app.platform_verification.modules.rag.domain.interfaces import RagRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageRagUseCase:
    def __init__(self, repository: RagRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[RagEntity, str]:
        try:
            entity = RagEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[RagEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[RagEntity]:
        return self._repo.list_all(tenant_id)
