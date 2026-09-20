"""
Public Contract Facade for Core.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.core.application.use_cases import ManageCoreUseCase
from app.platform_verification.modules.core.infrastructure.repositories import InMemoryCoreRepository

class CoreFacade:
    def __init__(self):
        self._repo = InMemoryCoreRepository()
        self._use_case = ManageCoreUseCase(self._repo)

    @property
    def service(self) -> ManageCoreUseCase:
        return self._use_case

core_facade = CoreFacade()
