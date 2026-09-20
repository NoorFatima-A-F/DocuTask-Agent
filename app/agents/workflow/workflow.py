"""
Workflow Aggregate Root.
Domain aggregate modeling a workflow definition, current state, active checkpoints, and lifecycle state.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field
from app.agents.workflow.lifecycle import WorkflowLifecycleState
from app.agents.workflow.metadata import WorkflowIdentity, WorkflowStatistics
from app.agents.workflow.workflow_definition import WorkflowDefinition
from app.agents.workflow.workflow_instance import WorkflowInstance


class Workflow(BaseModel):
    """
    Workflow Aggregate Root.
    Encapsulates definition, runtime instance, and execution metadata.
    """
    definition: WorkflowDefinition
    instance: WorkflowInstance
    statistics: WorkflowStatistics = Field(default_factory=WorkflowStatistics)

    @property
    def workflow_id(self) -> UUID:
        return self.definition.definition_id

    @property
    def instance_id(self) -> UUID:
        return self.instance.instance_id

    @property
    def state(self) -> WorkflowLifecycleState:
        return self.instance.state

    def update_instance(self, instance: WorkflowInstance) -> "Workflow":
        return self.model_copy(update={"instance": instance})
