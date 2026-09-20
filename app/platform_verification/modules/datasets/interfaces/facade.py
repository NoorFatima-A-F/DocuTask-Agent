"""
Public Contract Facade for Datasets.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.datasets.application.use_cases import ManageDatasetsUseCase
from app.platform_verification.modules.datasets.infrastructure.repositories import InMemoryDatasetsRepository

class DatasetsFacade:
    def __init__(self):
        self._repo = InMemoryDatasetsRepository()
        self._use_case = ManageDatasetsUseCase(self._repo)

    @property
    def service(self) -> ManageDatasetsUseCase:
        return self._use_case

datasets_facade = DatasetsFacade()
