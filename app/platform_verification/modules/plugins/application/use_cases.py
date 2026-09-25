"""
Application Use Cases & Workflows for Plugins.
"""
from typing import List, Optional
from app.platform_verification.modules.plugins.domain.models import PluginsEntity
from app.platform_verification.modules.plugins.domain.interfaces import PluginsRepositoryInterface
from app.platform_verification.shared_kernel.result import Result, Success, Failure

class ManagePluginsUseCase:
    def __init__(self, repository: PluginsRepositoryInterface):
        self._repo = repository

    def create(self, name: str, tenant_id: str = "default-tenant", **metadata) -> Result[PluginsEntity, str]:
        try:
            entity = PluginsEntity(name=name, tenant_id=tenant_id, metadata=metadata)
            saved = self._repo.save(entity)
            return Success(saved)
        except Exception as e:
            return Failure(str(e))

    def get(self, entity_id: str) -> Optional[PluginsEntity]:
        return self._repo.get_by_id(entity_id)

    def list(self, tenant_id: str = "default-tenant") -> List[PluginsEntity]:
        return self._repo.list_all(tenant_id)
