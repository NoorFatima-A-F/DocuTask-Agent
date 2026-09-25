"""
Public Contract Facade for Chaos.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.chaos.application.use_cases import ManageChaosUseCase
from app.platform_verification.modules.chaos.infrastructure.repositories import InMemoryChaosRepository

class ChaosFacade:
    def __init__(self):
        self._repo = InMemoryChaosRepository()
        self._use_case = ManageChaosUseCase(self._repo)

    @property
    def service(self) -> ManageChaosUseCase:
        return self._use_case

chaos_facade = ChaosFacade()
