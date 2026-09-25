"""
Public Contract Facade for Rag.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.rag.application.use_cases import ManageRagUseCase
from app.platform_verification.modules.rag.infrastructure.repositories import InMemoryRagRepository

class RagFacade:
    def __init__(self):
        self._repo = InMemoryRagRepository()
        self._use_case = ManageRagUseCase(self._repo)

    @property
    def service(self) -> ManageRagUseCase:
        return self._use_case

rag_facade = RagFacade()
