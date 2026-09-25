"""
Public Contract Facade for Metrics.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.metrics.application.use_cases import ManageMetricsUseCase
from app.platform_verification.modules.metrics.infrastructure.repositories import InMemoryMetricsRepository

class MetricsFacade:
    def __init__(self):
        self._repo = InMemoryMetricsRepository()
        self._use_case = ManageMetricsUseCase(self._repo)

    @property
    def service(self) -> ManageMetricsUseCase:
        return self._use_case

metrics_facade = MetricsFacade()
