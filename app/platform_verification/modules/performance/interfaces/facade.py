"""
Public Contract Facade for Performance.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.performance.application.use_cases import ManagePerformanceUseCase
from app.platform_verification.modules.performance.infrastructure.repositories import InMemoryPerformanceRepository

class PerformanceFacade:
    def __init__(self):
        self._repo = InMemoryPerformanceRepository()
        self._use_case = ManagePerformanceUseCase(self._repo)

    @property
    def service(self) -> ManagePerformanceUseCase:
        return self._use_case

performance_facade = PerformanceFacade()
