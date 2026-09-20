"""
Public Contract Facade for Ocr.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.ocr.application.use_cases import ManageOcrUseCase
from app.platform_verification.modules.ocr.infrastructure.repositories import InMemoryOcrRepository

class OcrFacade:
    def __init__(self):
        self._repo = InMemoryOcrRepository()
        self._use_case = ManageOcrUseCase(self._repo)

    @property
    def service(self) -> ManageOcrUseCase:
        return self._use_case

ocr_facade = OcrFacade()
