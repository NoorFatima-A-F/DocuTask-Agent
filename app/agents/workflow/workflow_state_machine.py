"""
Workflow State Machine.
Enforces deterministic and valid transitions across 15 workflow lifecycle states.
"""

from typing import Dict, Set
from app.agents.workflow.exceptions import InvalidWorkflowStateTransitionError
from app.agents.workflow.lifecycle import WorkflowLifecycleState


class WorkflowStateMachine:
    """State machine governing allowable transitions between workflow lifecycle states."""

    ALLOWED_TRANSITIONS: Dict[WorkflowLifecycleState, Set[WorkflowLifecycleState]] = {
        WorkflowLifecycleState.CREATED: {WorkflowLifecycleState.REGISTERED, WorkflowLifecycleState.READY},
        WorkflowLifecycleState.REGISTERED: {WorkflowLifecycleState.READY, WorkflowLifecycleState.ARCHIVED},
        WorkflowLifecycleState.READY: {WorkflowLifecycleState.SCHEDULED, WorkflowLifecycleState.RUNNING, WorkflowLifecycleState.CANCELLED},
        WorkflowLifecycleState.SCHEDULED: {WorkflowLifecycleState.RUNNING, WorkflowLifecycleState.CANCELLED},
        WorkflowLifecycleState.RUNNING: {
            WorkflowLifecycleState.WAITING,
            WorkflowLifecycleState.BLOCKED,
            WorkflowLifecycleState.PAUSED,
            WorkflowLifecycleState.MIGRATING,
            WorkflowLifecycleState.COMPENSATING,
            WorkflowLifecycleState.RECOVERING,
            WorkflowLifecycleState.COMPLETED,
            WorkflowLifecycleState.FAILED,
            WorkflowLifecycleState.CANCELLED
        },
        WorkflowLifecycleState.WAITING: {WorkflowLifecycleState.RUNNING, WorkflowLifecycleState.CANCELLED, WorkflowLifecycleState.FAILED},
        WorkflowLifecycleState.BLOCKED: {WorkflowLifecycleState.RUNNING, WorkflowLifecycleState.FAILED, WorkflowLifecycleState.CANCELLED},
        WorkflowLifecycleState.PAUSED: {WorkflowLifecycleState.RUNNING, WorkflowLifecycleState.CANCELLED},
        WorkflowLifecycleState.MIGRATING: {WorkflowLifecycleState.RUNNING, WorkflowLifecycleState.FAILED},
        WorkflowLifecycleState.COMPENSATING: {WorkflowLifecycleState.FAILED, WorkflowLifecycleState.COMPLETED},
        WorkflowLifecycleState.RECOVERING: {WorkflowLifecycleState.RUNNING, WorkflowLifecycleState.FAILED},
        WorkflowLifecycleState.COMPLETED: {WorkflowLifecycleState.ARCHIVED},
        WorkflowLifecycleState.FAILED: {WorkflowLifecycleState.ARCHIVED},
        WorkflowLifecycleState.CANCELLED: {WorkflowLifecycleState.ARCHIVED},
        WorkflowLifecycleState.ARCHIVED: set(),
    }

    @classmethod
    def validate_transition(
        cls,
        current_state: WorkflowLifecycleState,
        target_state: WorkflowLifecycleState
    ) -> None:
        """Validates that current_state -> target_state transition is permitted."""
        allowed = cls.ALLOWED_TRANSITIONS.get(current_state, set())
        if target_state not in allowed:
            raise InvalidWorkflowStateTransitionError(
                f"Illegal workflow state transition from {current_state.value} to {target_state.value}."
            )
