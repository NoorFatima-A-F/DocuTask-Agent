"""
Workflow Instance Model.
Represents an active, long-running execution instance of a WorkflowDefinition.
"""

from typing import List
from uuid import UUID
from pydantic import BaseModel, Field
from app.agents.workflow.lifecycle import WorkflowLifecycleState
from app.agents.workflow.metadata import WorkflowIdentity, WorkflowStatistics
from app.agents.workflow.workflow_state import WorkflowState
from app.agents.workflow.workflow_state_machine import WorkflowStateMachine


class WorkflowInstance(BaseModel):
    """An active running or paused instance of a workflow."""
    identity: WorkflowIdentity
    definition_id: UUID
    state: WorkflowLifecycleState = Field(default=WorkflowLifecycleState.CREATED)
    workflow_state: WorkflowState = Field(default_factory=WorkflowState)
    statistics: WorkflowStatistics = Field(default_factory=WorkflowStatistics)
    errors: List[str] = Field(default_factory=list)

    @property
    def instance_id(self) -> UUID:
        return self.identity.instance_id

    def transition_to(self, new_state: WorkflowLifecycleState) -> "WorkflowInstance":
        """Enforces state machine validation on transition."""
        WorkflowStateMachine.validate_transition(self.state, new_state)
        return self.model_copy(update={"state": new_state})
