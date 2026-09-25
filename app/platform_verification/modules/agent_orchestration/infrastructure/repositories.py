"""
In-Memory / Async SQLAlchemy Repository for AgentOrchestration.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.agent_orchestration.domain.models import AgentOrchestrationEntity
from app.platform_verification.modules.agent_orchestration.domain.interfaces import AgentOrchestrationRepositoryInterface

class InMemoryAgentOrchestrationRepository(AgentOrchestrationRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, AgentOrchestrationEntity] = {}

    def save(self, entity: AgentOrchestrationEntity) -> AgentOrchestrationEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[AgentOrchestrationEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[AgentOrchestrationEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
