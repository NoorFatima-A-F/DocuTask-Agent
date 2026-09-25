"""
Application Use Cases & Workflows for AgentOrchestration.
"""
from typing import List, Optional
from app.platform_verification.modules.agent_orchestration.domain.models import AgentOrchestrationEntity
from app.platform_verification.modules.agent_orchestration.domain.interfaces import AgentOrchestrationRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManageAgentOrchestrationUseCase:
    def __init__(self, repository: AgentOrchestrationRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[AgentOrchestrationEntity, str]:
        try:
            entity = AgentOrchestrationEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[AgentOrchestrationEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[AgentOrchestrationEntity]:
        return self._repo.list_all(tenant_id)
