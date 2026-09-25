"""
Runtime Lifecycle State Machine.
Defines the 9 canonical lifecycle states of the platform kernel and enforces deterministic transitions.
"""

from enum import Enum
from typing import Dict, Set
from app.agents.runtime.exceptions import InvalidRuntimeStateTransitionError


class RuntimeLifecycleState(str, Enum):
    """Canonical lifecycle states of the Platform Runtime Kernel."""
    OFFLINE = "OFFLINE"
    BOOTING = "BOOTING"
    INITIALIZING = "INITIALIZING"
    READY = "READY"
    RUNNING = "RUNNING"
    DEGRADED = "DEGRADED"
    DRAINING = "DRAINING"
    STOPPING = "STOPPING"
    TERMINATED = "TERMINATED"


class RuntimeLifecycleStateMachine:
    """Validates state transitions of the platform runtime kernel."""

    VALID_TRANSITIONS: Dict[RuntimeLifecycleState, Set[RuntimeLifecycleState]] = {
        RuntimeLifecycleState.OFFLINE: {
            RuntimeLifecycleState.BOOTING,
        },
        RuntimeLifecycleState.BOOTING: {
            RuntimeLifecycleState.INITIALIZING,
            RuntimeLifecycleState.STOPPING,
            RuntimeLifecycleState.TERMINATED,
        },
        RuntimeLifecycleState.INITIALIZING: {
            RuntimeLifecycleState.READY,
            RuntimeLifecycleState.STOPPING,
            RuntimeLifecycleState.TERMINATED,
        },
        RuntimeLifecycleState.READY: {
            RuntimeLifecycleState.RUNNING,
            RuntimeLifecycleState.DRAINING,
            RuntimeLifecycleState.STOPPING,
        },
        RuntimeLifecycleState.RUNNING: {
            RuntimeLifecycleState.DEGRADED,
            RuntimeLifecycleState.DRAINING,
            RuntimeLifecycleState.STOPPING,
        },
        RuntimeLifecycleState.DEGRADED: {
            RuntimeLifecycleState.RUNNING,  # Recovered
            RuntimeLifecycleState.DRAINING,
            RuntimeLifecycleState.STOPPING,
        },
        RuntimeLifecycleState.DRAINING: {
            RuntimeLifecycleState.STOPPING,
            RuntimeLifecycleState.TERMINATED,
        },
        RuntimeLifecycleState.STOPPING: {
            RuntimeLifecycleState.TERMINATED,
        },
        RuntimeLifecycleState.TERMINATED: {
            RuntimeLifecycleState.BOOTING,  # Re-boot allowed
        },
    }

    @classmethod
    def can_transition(cls, from_state: RuntimeLifecycleState, to_state: RuntimeLifecycleState) -> bool:
        """Returns True if transition from from_state to to_state is valid."""
        return to_state in cls.VALID_TRANSITIONS.get(from_state, set())

    @classmethod
    def validate_transition(cls, from_state: RuntimeLifecycleState, to_state: RuntimeLifecycleState) -> None:
        """Enforces transition rule or raises InvalidRuntimeStateTransitionError."""
        if not cls.can_transition(from_state, to_state):
            raise InvalidRuntimeStateTransitionError(
                f"Invalid runtime kernel transition from '{from_state.value}' to '{to_state.value}'."
            )
