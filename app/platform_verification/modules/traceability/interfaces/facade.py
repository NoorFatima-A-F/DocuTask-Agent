"""
Public Contract Facade for Traceability.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.traceability.application.use_cases import ManageTraceabilityUseCase
from app.platform_verification.modules.traceability.infrastructure.repositories import InMemoryTraceabilityRepository

class TraceabilityFacade:
    def __init__(self):
        self._repo = InMemoryTraceabilityRepository()
        self._use_case = ManageTraceabilityUseCase(self._repo)

    @property
    def service(self) -> ManageTraceabilityUseCase:
        return self._use_case

traceability_facade = TraceabilityFacade()
