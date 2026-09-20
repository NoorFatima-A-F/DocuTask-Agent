"""
Workflow Replay Engine.
Deterministically reconstructs workflow instance state and progression from historical event logs.
"""

import logging
from typing import Any, Dict, Optional
from uuid import UUID
from app.agents.workflow.interfaces import IWorkflowReplayEngine
from app.agents.workflow.lifecycle import WorkflowLifecycleState
from app.agents.workflow.workflow_history import WorkflowHistory, WorkflowHistoryEvent
from app.agents.workflow.workflow_state import WorkflowState

logger = logging.getLogger(__name__)


class WorkflowReplayResult:
    """Result of replaying workflow history."""

    def __init__(
        self,
        instance_id: UUID,
        final_state: WorkflowState,
        last_lifecycle_state: WorkflowLifecycleState,
        events_replayed: int,
    ) -> None:
        self.instance_id = instance_id
        self.final_state = final_state
        self.last_lifecycle_state = last_lifecycle_state
        self.events_replayed = events_replayed


class WorkflowReplayEngine(IWorkflowReplayEngine):
    """Reconstructs state deterministically from append-only history."""

    async def replay(self, history: WorkflowHistory) -> WorkflowReplayResult:
        """Replays all events in sequence to rebuild the workflow state."""
        state = WorkflowState()
        lifecycle_state = WorkflowLifecycleState.CREATED

        for event in history.events:
            logger.debug(
                f"Replaying event {event.event_id} ({event.event_type}) for instance {event.instance_id}"
            )
            if event.event_type == "NODE_COMPLETED":
                if event.node_id:
                    state = state.mark_node_completed(event.node_id, event.payload)
            elif event.event_type == "VARIABLE_SET":
                for k, v in event.payload.items():
                    state = state.set_variable(k, v)
            elif event.event_type == "STATE_TRANSITION":
                target_state = event.payload.get("target_state")
                if target_state:
                    lifecycle_state = WorkflowLifecycleState(target_state)

        return WorkflowReplayResult(
            instance_id=history.instance_id,
            final_state=state,
            last_lifecycle_state=lifecycle_state,
            events_replayed=len(history.events),
        )
