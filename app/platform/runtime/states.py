"""
Platform Runtime 17-State Finite State Machine Definitions.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict
import uuid


class RuntimeState(str, Enum):
    """The 17 formal runtime operating states of the DocuTask Platform Kernel."""
    CREATED = "CREATED"
    CONFIG_LOADING = "CONFIG_LOADING"
    CONFIG_VALIDATED = "CONFIG_VALIDATED"
    SECRETS_READY = "SECRETS_READY"
    DATABASE_READY = "DATABASE_READY"
    CACHE_READY = "CACHE_READY"
    QUEUE_READY = "QUEUE_READY"
    EVENT_BUS_READY = "EVENT_BUS_READY"
    MODULE_LOADING = "MODULE_LOADING"
    PLUGIN_LOADING = "PLUGIN_LOADING"
    SERVICE_READY = "SERVICE_READY"
    HEALTH_CHECKING = "HEALTH_CHECKING"
    READY = "READY"
    RUNNING = "RUNNING"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    TERMINATED = "TERMINATED"
    FAILED = "FAILED"


# Valid state transitions mapping
VALID_STATE_TRANSITIONS = {
    RuntimeState.CREATED: [RuntimeState.CONFIG_LOADING, RuntimeState.FAILED],
    RuntimeState.CONFIG_LOADING: [RuntimeState.CONFIG_VALIDATED, RuntimeState.FAILED],
    RuntimeState.CONFIG_VALIDATED: [RuntimeState.SECRETS_READY, RuntimeState.FAILED],
    RuntimeState.SECRETS_READY: [RuntimeState.DATABASE_READY, RuntimeState.FAILED],
    RuntimeState.DATABASE_READY: [RuntimeState.CACHE_READY, RuntimeState.FAILED],
    RuntimeState.CACHE_READY: [RuntimeState.QUEUE_READY, RuntimeState.FAILED],
    RuntimeState.QUEUE_READY: [RuntimeState.EVENT_BUS_READY, RuntimeState.FAILED],
    RuntimeState.EVENT_BUS_READY: [RuntimeState.MODULE_LOADING, RuntimeState.FAILED],
    RuntimeState.MODULE_LOADING: [RuntimeState.PLUGIN_LOADING, RuntimeState.FAILED],
    RuntimeState.PLUGIN_LOADING: [RuntimeState.SERVICE_READY, RuntimeState.FAILED],
    RuntimeState.SERVICE_READY: [RuntimeState.HEALTH_CHECKING, RuntimeState.FAILED],
    RuntimeState.HEALTH_CHECKING: [RuntimeState.READY, RuntimeState.FAILED],
    RuntimeState.READY: [RuntimeState.RUNNING, RuntimeState.SHUTTING_DOWN, RuntimeState.FAILED],
    RuntimeState.RUNNING: [RuntimeState.SHUTTING_DOWN, RuntimeState.FAILED],
    RuntimeState.SHUTTING_DOWN: [RuntimeState.TERMINATED, RuntimeState.FAILED],
    RuntimeState.FAILED: [RuntimeState.SHUTTING_DOWN, RuntimeState.TERMINATED],
    RuntimeState.TERMINATED: [],
}


@dataclass
class RuntimeStateEvent:
    """Event emitted on runtime state transition."""
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    from_state: RuntimeState = RuntimeState.CREATED
    to_state: RuntimeState = RuntimeState.CREATED
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)
