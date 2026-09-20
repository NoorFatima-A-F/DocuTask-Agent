"""
Platform Kernel Lifecycle Interfaces and State Enums.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
import uuid


class LifecyclePhase(str, Enum):
    """High-level phases in the platform lifecycle."""
    BOOTSTRAP = "BOOTSTRAP"
    INITIALIZATION = "INITIALIZATION"
    STARTUP = "STARTUP"
    RUNNING = "RUNNING"
    DEGRADED = "DEGRADED"
    DRAINING = "DRAINING"
    SHUTDOWN = "SHUTDOWN"
    TERMINATED = "TERMINATED"


class LifecycleState(str, Enum):
    """Granular states of a managed platform component or subsystem."""
    UNINITIALIZED = "UNINITIALIZED"
    INITIALIZING = "INITIALIZING"
    INITIALIZED = "INITIALIZED"
    STARTING = "STARTING"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class LifecycleTransition:
    """Record of a state transition in a component or the runtime."""
    transition_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    component_id: str = "runtime"
    from_state: str = "UNKNOWN"
    to_state: str = "UNKNOWN"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    details: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error_message: Optional[str] = None


class ILifecycle(ABC):
    """Universal interface for components supporting managed lifecycle transitions."""

    @property
    @abstractmethod
    def state(self) -> LifecycleState:
        """Current lifecycle state."""
        pass

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize resources, prepare connections, register dependencies."""
        pass

    @abstractmethod
    async def start(self) -> None:
        """Begin active operations, background workers, event listeners."""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Gracefully stop operations and drain in-flight requests."""
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        """Release all allocated resources, close pools, finalize state."""
        pass
