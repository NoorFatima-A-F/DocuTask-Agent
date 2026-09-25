"""
Workflow Registry.
Catalog of registered workflow definitions, active instances, and historical records.
"""

from typing import Dict, List, Optional
from uuid import UUID
from app.agents.workflow.workflow_definition import WorkflowDefinition
from app.agents.workflow.workflow_instance import WorkflowInstance


class WorkflowRegistry:
    """Thread-safe registry for workflow definitions and live instances."""

    def __init__(self):
        self._definitions: Dict[UUID, WorkflowDefinition] = {}
        self._instances: Dict[UUID, WorkflowInstance] = {}

    def register_definition(self, definition: WorkflowDefinition) -> None:
        self._definitions[definition.definition_id] = definition

    def get_definition(self, definition_id: UUID) -> Optional[WorkflowDefinition]:
        return self._definitions.get(definition_id)

    def register_instance(self, instance: WorkflowInstance) -> None:
        self._instances[instance.instance_id] = instance

    def get_instance(self, instance_id: UUID) -> Optional[WorkflowInstance]:
        return self._instances.get(instance_id)

    def list_active_instances(self) -> List[WorkflowInstance]:
        return [i for i in self._instances.values() if i.state.is_active()]
