"""
Public Contract Facade for Certification.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.certification.application.use_cases import ManageCertificationUseCase
from app.platform_verification.modules.certification.infrastructure.repositories import InMemoryCertificationRepository

class CertificationFacade:
    def __init__(self):
        self._repo = InMemoryCertificationRepository()
        self._use_case = ManageCertificationUseCase(self._repo)

    @property
    def service(self) -> ManageCertificationUseCase:
        return self._use_case

certification_facade = CertificationFacade()
