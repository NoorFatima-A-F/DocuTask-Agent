"""
Public Contract Facade for Environments.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.environments.application.use_cases import ManageEnvironmentsUseCase
from app.platform_verification.modules.environments.infrastructure.repositories import InMemoryEnvironmentsRepository

class EnvironmentsFacade:
    def __init__(self):
        self._repo = InMemoryEnvironmentsRepository()
        self._use_case = ManageEnvironmentsUseCase(self._repo)

    @property
    def service(self) -> ManageEnvironmentsUseCase:
        return self._use_case

environments_facade = EnvironmentsFacade()
