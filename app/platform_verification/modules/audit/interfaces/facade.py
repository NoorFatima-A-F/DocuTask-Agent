"""
Public Contract Facade for Audit.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.audit.application.use_cases import ManageAuditUseCase
from app.platform_verification.modules.audit.infrastructure.repositories import InMemoryAuditRepository

class AuditFacade:
    def __init__(self):
        self._repo = InMemoryAuditRepository()
        self._use_case = ManageAuditUseCase(self._repo)

    @property
    def service(self) -> ManageAuditUseCase:
        return self._use_case

audit_facade = AuditFacade()
