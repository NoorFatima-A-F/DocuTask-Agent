"""
Application Use Cases & Workflows for Certification.
"""
from typing import List, Optional
from app.platform_verification.modules.certification.domain.models import CertificationEntity
from app.platform_verification.modules.certification.domain.interfaces import CertificationRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageCertificationUseCase:
    def __init__(self, repository: CertificationRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[CertificationEntity, str]:
        try:
            entity = CertificationEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[CertificationEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[CertificationEntity]:
        return self._repo.list_all(tenant_id)
