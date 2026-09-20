"""
Public Contract Facade for Quality.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.quality.application.use_cases import ManageQualityUseCase
from app.platform_verification.modules.quality.infrastructure.repositories import InMemoryQualityRepository

class QualityFacade:
    def __init__(self):
        self._repo = InMemoryQualityRepository()
        self._use_case = ManageQualityUseCase(self._repo)

    @property
    def service(self) -> ManageQualityUseCase:
        return self._use_case

quality_facade = QualityFacade()
