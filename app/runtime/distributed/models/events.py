"""
Phase 13.18: Distributed Event Mesh & Event Stream
High-throughput asynchronous distributed domain events.
"""

from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Callable, Any, Optional, Union
from pydantic import BaseModel, Field
import uuid


class DistributedEventType(str, Enum):
    WORKER_REGISTERED = "WORKER_REGISTERED"
    WORKER_HEARTBEAT = "WORKER_HEARTBEAT"
    WORKER_DRAINED = "WORKER_DRAINED"
    WORKER_CRASHED = "WORKER_CRASHED"
    JOB_ENQUEUED = "JOB_ENQUEUED"
    JOB_SCHEDULED = "JOB_SCHEDULED"
    JOB_DISPATCHED = "JOB_DISPATCHED"
    JOB_COMPLETED = "JOB_COMPLETED"
    JOB_FAILED = "JOB_FAILED"
    WORKFLOW_STARTED = "WORKFLOW_STARTED"
    WORKFLOW_CHECKPOINTED = "WORKFLOW_CHECKPOINTED"
    WORKFLOW_PAUSED = "WORKFLOW_PAUSED"
    WORKFLOW_RESUMED = "WORKFLOW_RESUMED"
    WORKFLOW_MIGRATED = "WORKFLOW_MIGRATED"
    LOCK_ACQUIRED = "LOCK_ACQUIRED"
    LOCK_RELEASED = "LOCK_RELEASED"
    AUTOSCALE_TRIGGERED = "AUTOSCALE_TRIGGERED"
    FAILOVER_EXECUTED = "FAILOVER_EXECUTED"
    DR_SNAPSHOT_CREATED = "DR_SNAPSHOT_CREATED"


class DistributedEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"dev_{uuid.uuid4().hex[:10]}")
    event_type: DistributedEventType
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_node: Optional[str] = "fabric_master"
    workflow_id: Optional[str] = None
    job_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)


class DistributedEventBus:
    """In-memory event mesh with subscriber routing and replay buffers."""

    def __init__(self, max_history: int = 5000):
        self._subscribers: Dict[str, List[Callable[[DistributedEvent], Any]]] = {}
        self._history: List[DistributedEvent] = []
        self._max_history = max_history

    def subscribe(self, event_type: Union[DistributedEventType, str], callback: Callable[[DistributedEvent], Any]):
        key = event_type.value if isinstance(event_type, DistributedEventType) else event_type
        if key not in self._subscribers:
            self._subscribers[key] = []
        self._subscribers[key].append(callback)

    async def publish(self, event: DistributedEvent):
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history.pop(0)

        key = event.event_type.value
        handlers = self._subscribers.get(key, []) + self._subscribers.get("*", [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception:
                pass

    def get_history(self, limit: int = 100, event_type: Optional[DistributedEventType] = None) -> List[DistributedEvent]:
        if event_type:
            filtered = [e for e in self._history if e.event_type == event_type]
            return filtered[-limit:]
        return self._history[-limit:]
