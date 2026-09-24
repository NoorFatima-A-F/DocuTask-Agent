"""
Workflow Timer Manager.
Coordinates durable workflow sleep intervals, timeouts, and scheduled wake-ups.
"""

from datetime import datetime, timezone
from typing import Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.workflow.exceptions import InvalidTimerConfigurationError


class WorkflowTimer(BaseModel):
    """A durable timer set by a workflow."""
    timer_id: UUID = Field(default_factory=uuid4)
    instance_id: UUID
    node_id: str
    duration_seconds: float
    expires_at_timestamp: float

    model_config = {"frozen": True}


class TimerManager:
    """Manages in-memory and durable timers."""

    def __init__(self):
        self._timers: Dict[UUID, WorkflowTimer] = {}

    def set_timer(self, instance_id: UUID, node_id: str, duration_seconds: float) -> WorkflowTimer:
        """Registers a new timer."""
        if duration_seconds <= 0:
            raise InvalidTimerConfigurationError(f"Timer duration must be positive. Provided: {duration_seconds}")

        now = datetime.now(timezone.utc).timestamp()
        timer = WorkflowTimer(
            instance_id=instance_id,
            node_id=node_id,
            duration_seconds=duration_seconds,
            expires_at_timestamp=now + duration_seconds
        )
        self._timers[timer.timer_id] = timer
        return timer

    def get_expired_timers(self) -> List[WorkflowTimer]:
        """Returns all timers that have completed their duration."""
        now = datetime.now(timezone.utc).timestamp()
        expired = [t for t in self._timers.values() if t.expires_at_timestamp <= now]
        for t in expired:
            del self._timers[t.timer_id]
        return expired
