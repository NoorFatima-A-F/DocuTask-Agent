"""
Workflow History.
Append-only event audit log recording all node completions, state transitions, and signals for deterministic replay.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class WorkflowHistoryEvent(BaseModel):
    """An individual historical event in the workflow execution timeline."""
    event_id: UUID = Field(default_factory=uuid4)
    instance_id: UUID
    event_type: str  # NODE_STARTED, NODE_COMPLETED, SIGNAL_RECEIVED, STATE_TRANSITION
    node_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}


class WorkflowHistory(BaseModel):
    """Sequence of historical execution events for an instance."""
    instance_id: UUID
    events: List[WorkflowHistoryEvent] = Field(default_factory=list)

    def append_event(self, event_type: str, node_id: Optional[str] = None, payload: Dict[str, Any] = None) -> "WorkflowHistory":
        event = WorkflowHistoryEvent(
            instance_id=self.instance_id,
            event_type=event_type,
            node_id=node_id,
            payload=payload or {}
        )
        return self.model_copy(update={"events": [*self.events, event]})
