"""
Public Contract Facade for Execution.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.execution.application.use_cases import ManageExecutionUseCase
from app.platform_verification.modules.execution.infrastructure.repositories import InMemoryExecutionRepository

class ExecutionFacade:
    def __init__(self):
        self._repo = InMemoryExecutionRepository()
        self._use_case = ManageExecutionUseCase(self._repo)

    @property
    def service(self) -> ManageExecutionUseCase:
        return self._use_case

execution_facade = ExecutionFacade()
