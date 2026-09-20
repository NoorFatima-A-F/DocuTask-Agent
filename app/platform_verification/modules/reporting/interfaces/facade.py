"""
Public Contract Facade for Reporting.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.reporting.application.use_cases import ManageReportingUseCase
from app.platform_verification.modules.reporting.infrastructure.repositories import InMemoryReportingRepository

class ReportingFacade:
    def __init__(self):
        self._repo = InMemoryReportingRepository()
        self._use_case = ManageReportingUseCase(self._repo)

    @property
    def service(self) -> ManageReportingUseCase:
        return self._use_case

reporting_facade = ReportingFacade()
