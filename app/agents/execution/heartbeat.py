"""
Heartbeat and Liveness Monitor.
Tracks worker and execution session heartbeats to detect hung or stalled processes.
"""

from datetime import datetime, timezone
from typing import Dict
from pydantic import BaseModel, Field


class HeartbeatRecord(BaseModel):
    """Heartbeat timestamp for an active entity."""
    entity_id: str
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_config = {"frozen": True}


class HeartbeatMonitor:
    """Monitors worker heartbeats and detects dead or unresponsive workers."""

    def __init__(self, heartbeat_timeout_seconds: float = 60.0):
        self.timeout_seconds = heartbeat_timeout_seconds
        self._heartbeats: Dict[str, datetime] = {}

    def record_heartbeat(self, entity_id: str) -> None:
        self._heartbeats[entity_id] = datetime.now(timezone.utc)

    def is_alive(self, entity_id: str) -> bool:
        last = self._heartbeats.get(entity_id)
        if not last:
            return True  # Assuming alive if freshly registered
        elapsed = (datetime.now(timezone.utc) - last).total_seconds()
        return elapsed <= self.timeout_seconds
