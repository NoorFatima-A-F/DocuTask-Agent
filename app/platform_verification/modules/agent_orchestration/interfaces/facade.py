"""
Public Contract Facade for AgentOrchestration.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.agent_orchestration.application.use_cases import ManageAgentOrchestrationUseCase
from app.platform_verification.modules.agent_orchestration.infrastructure.repositories import InMemoryAgentOrchestrationRepository

class AgentOrchestrationFacade:
    def __init__(self):
        self._repo = InMemoryAgentOrchestrationRepository()
        self._use_case = ManageAgentOrchestrationUseCase(self._repo)

    @property
    def service(self) -> ManageAgentOrchestrationUseCase:
        return self._use_case

agent_orchestration_facade = AgentOrchestrationFacade()
