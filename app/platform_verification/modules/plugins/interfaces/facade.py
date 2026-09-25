"""
Public Contract Facade for Plugins.
Restricts internal package details from leaking across module boundaries.
"""
from app.platform_verification.modules.plugins.application.use_cases import ManagePluginsUseCase
from app.platform_verification.modules.plugins.infrastructure.repositories import InMemoryPluginsRepository

class PluginsFacade:
    def __init__(self):
        self._repo = InMemoryPluginsRepository()
        self._use_case = ManagePluginsUseCase(self._repo)

    @property
    def service(self) -> ManagePluginsUseCase:
        return self._use_case

plugins_facade = PluginsFacade()
