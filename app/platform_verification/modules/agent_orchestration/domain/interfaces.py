"""
Domain Interfaces (Ports) for AgentOrchestration.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.agent_orchestration.domain.models import AgentOrchestrationEntity

class AgentOrchestrationRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: AgentOrchestrationEntity) -> AgentOrchestrationEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[AgentOrchestrationEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[AgentOrchestrationEntity]:
        pass
