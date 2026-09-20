"""
Application Use Cases & Workflows for AiExtraction.
"""
from typing import List, Optional
from app.platform_verification.modules.ai_extraction.domain.models import AiExtractionEntity
from app.platform_verification.modules.ai_extraction.domain.interfaces import AiExtractionRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageAiExtractionUseCase:
    def __init__(self, repository: AiExtractionRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[AiExtractionEntity, str]:
        try:
            entity = AiExtractionEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[AiExtractionEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[AiExtractionEntity]:
        return self._repo.list_all(tenant_id)
