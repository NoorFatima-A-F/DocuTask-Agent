"""
In-Memory / Async SQLAlchemy Repository for Execution.
"""
from typing import Dict, List, Optional
from app.platform_verification.modules.execution.domain.models import ExecutionEntity
from app.platform_verification.modules.execution.domain.interfaces import ExecutionRepositoryInterface

class InMemoryExecutionRepository(ExecutionRepositoryInterface):
    def __init__(self):
        self._storage: Dict[str, ExecutionEntity] = {}

    def save(self, entity: ExecutionEntity) -> ExecutionEntity:
        self._storage[entity.id] = entity
        return entity

    def get_by_id(self, entity_id: str) -> Optional[ExecutionEntity]:
        return self._storage.get(entity_id)

    def list_all(self, tenant_id: str = "default-tenant") -> List[ExecutionEntity]:
        return [e for e in self._storage.values() if e.tenant_id == tenant_id]
