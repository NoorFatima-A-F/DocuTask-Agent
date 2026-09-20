"""
Workflow Repository.
Provides storage abstraction and in-memory implementation for definitions and active/persisted workflow instances.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from uuid import UUID
from app.agents.workflow.workflow_definition import WorkflowDefinition
from app.agents.workflow.workflow_instance import WorkflowInstance


class IWorkflowRepository(ABC):
    """Abstract repository for workflow definitions and instances."""

    @abstractmethod
    async def save_definition(self, definition: WorkflowDefinition) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_definition(self, definition_id: UUID) -> Optional[WorkflowDefinition]:
        raise NotImplementedError

    @abstractmethod
    async def list_definitions(self) -> List[WorkflowDefinition]:
        raise NotImplementedError

    @abstractmethod
    async def save_instance(self, instance: WorkflowInstance) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_instance(self, instance_id: UUID) -> Optional[WorkflowInstance]:
        raise NotImplementedError

    @abstractmethod
    async def list_instances(self) -> List[WorkflowInstance]:
        raise NotImplementedError

    @abstractmethod
    async def delete_instance(self, instance_id: UUID) -> bool:
        raise NotImplementedError


class InMemoryWorkflowRepository(IWorkflowRepository):
    """Thread-safe in-memory repository for workflow definitions and execution instances."""

    def __init__(self) -> None:
        self._definitions: Dict[UUID, WorkflowDefinition] = {}
        self._instances: Dict[UUID, WorkflowInstance] = {}

    async def save_definition(self, definition: WorkflowDefinition) -> None:
        self._definitions[definition.definition_id] = definition

    async def get_definition(self, definition_id: UUID) -> Optional[WorkflowDefinition]:
        return self._definitions.get(definition_id)

    async def list_definitions(self) -> List[WorkflowDefinition]:
        return list(self._definitions.values())

    async def save_instance(self, instance: WorkflowInstance) -> None:
        self._instances[instance.instance_id] = instance

    async def get_instance(self, instance_id: UUID) -> Optional[WorkflowInstance]:
        return self._instances.get(instance_id)

    async def list_instances(self) -> List[WorkflowInstance]:
        return list(self._instances.values())

    async def delete_instance(self, instance_id: UUID) -> bool:
        return bool(self._instances.pop(instance_id, None))
