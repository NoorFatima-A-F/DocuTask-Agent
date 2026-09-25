"""
Domain Interfaces (Ports) for Plugins.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.platform_verification.modules.plugins.domain.models import PluginsEntity

class PluginsRepositoryInterface(ABC):
    @abstractmethod
    def save(self, entity: PluginsEntity) -> PluginsEntity:
        pass

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[PluginsEntity]:
        pass

    @abstractmethod
    def list_all(self, tenant_id: str) -> List[PluginsEntity]:
        pass
