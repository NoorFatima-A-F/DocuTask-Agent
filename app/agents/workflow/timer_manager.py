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
    duration_seconds: float = Field(default=0.0)
    delay_seconds: float = Field(default=0.0)
    expires_at_timestamp: float = Field(default=0.0)

    model_config = {"frozen": False}

    def __init__(self, **data):
        if "delay_seconds" in data and "duration_seconds" not in data:
            data["duration_seconds"] = data["delay_seconds"]
        if "duration_seconds" in data and "delay_seconds" not in data:
            data["delay_seconds"] = data["duration_seconds"]
        super().__init__(**data)


class TimerManager:
    """Manages in-memory and durable timers."""

    def __init__(self):
        self._timers: Dict[UUID, WorkflowTimer] = {}

    def register_timer(self, instance_id: UUID, node_id: str, delay_seconds: float = 0.0, **kwargs) -> WorkflowTimer:
        """Registers a new timer with delay_seconds parameter."""
        duration = delay_seconds or kwargs.get("duration_seconds", 0.0)
        return self.set_timer(instance_id, node_id, duration)

    def set_timer(self, instance_id: UUID, node_id: str, duration_seconds: float) -> WorkflowTimer:
        """Registers a new timer."""
        if duration_seconds <= 0:
            raise InvalidTimerConfigurationError(f"Timer duration must be positive. Provided: {duration_seconds}")

        now = datetime.now(timezone.utc).timestamp()
        timer = WorkflowTimer(
            instance_id=instance_id,
            node_id=node_id,
            duration_seconds=duration_seconds,
            delay_seconds=duration_seconds,
            expires_at_timestamp=now + duration_seconds,
        )
        self._timers[timer.timer_id] = timer
        return timer

    def has_expired(self, timer_id: UUID) -> bool:
        """Checks if a timer has completed its scheduled duration."""
        timer = self._timers.get(timer_id)
        if not timer:
            return True
        now = datetime.now(timezone.utc).timestamp()
        return timer.expires_at_timestamp <= now

    def get_expired_timers(self) -> List[WorkflowTimer]:
        """Returns all timers that have completed their duration."""
        now = datetime.now(timezone.utc).timestamp()
        expired = [t for t in self._timers.values() if t.expires_at_timestamp <= now]
        for t in expired:
            del self._timers[t.timer_id]
        return expired
