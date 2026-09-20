"""
Application Use Cases & Workflows for Evidence.
"""
from typing import List, Optional
from app.platform_verification.modules.evidence.domain.models import EvidenceEntity
from app.platform_verification.modules.evidence.domain.interfaces import EvidenceRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageEvidenceUseCase:
    def __init__(self, repository: EvidenceRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[EvidenceEntity, str]:
        try:
            entity = EvidenceEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[EvidenceEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[EvidenceEntity]:
        return self._repo.list_all(tenant_id)
