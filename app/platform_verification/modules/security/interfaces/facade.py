"""
Public Contract Facade for Security.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.security.application.use_cases import ManageSecurityUseCase
from app.platform_verification.modules.security.infrastructure.repositories import InMemorySecurityRepository

class SecurityFacade:
    def __init__(self):
        self._repo = InMemorySecurityRepository()
        self._use_case = ManageSecurityUseCase(self._repo)

    @property
    def service(self) -> ManageSecurityUseCase:
        return self._use_case

security_facade = SecurityFacade()
