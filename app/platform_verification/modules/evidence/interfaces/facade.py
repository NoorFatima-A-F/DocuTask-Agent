"""
Public Contract Facade for Evidence.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.evidence.application.use_cases import ManageEvidenceUseCase
from app.platform_verification.modules.evidence.infrastructure.repositories import InMemoryEvidenceRepository

class EvidenceFacade:
    def __init__(self):
        self._repo = InMemoryEvidenceRepository()
        self._use_case = ManageEvidenceUseCase(self._repo)

    @property
    def service(self) -> ManageEvidenceUseCase:
        return self._use_case

evidence_facade = EvidenceFacade()
