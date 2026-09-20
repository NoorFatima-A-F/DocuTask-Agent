"""
Public Contract Facade for AiExtraction.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.ai_extraction.application.use_cases import ManageAiExtractionUseCase
from app.platform_verification.modules.ai_extraction.infrastructure.repositories import InMemoryAiExtractionRepository

class AiExtractionFacade:
    def __init__(self):
        self._repo = InMemoryAiExtractionRepository()
        self._use_case = ManageAiExtractionUseCase(self._repo)

    @property
    def service(self) -> ManageAiExtractionUseCase:
        return self._use_case

ai_extraction_facade = AiExtractionFacade()
