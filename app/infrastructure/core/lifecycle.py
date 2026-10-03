"""Infrastructure and Resource Lifecycle State Machines."""

from enum import Enum
from typing import Dict, Set
from .exceptions import InvalidStateTransitionError


class RuntimeState(str, Enum):
    CREATED = "CREATED"
    INITIALIZING = "INITIALIZING"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    DEGRADED = "DEGRADED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"
    RECOVERING = "RECOVERING"


class ResourceState(str, Enum):
    REQUESTED = "REQUESTED"
    ALLOCATING = "ALLOCATING"
    READY = "READY"
    ACTIVE = "ACTIVE"
    DRAINING = "DRAINING"
    RELEASED = "RELEASED"
    FAILED = "FAILED"


class RuntimeLifecycleStateMachine:
    """Enforces valid state transitions for services and runtime processes."""

    ALLOWED_TRANSITIONS: Dict[RuntimeState, Set[RuntimeState]] = {
        RuntimeState.CREATED: {RuntimeState.INITIALIZING, RuntimeState.FAILED},
        RuntimeState.INITIALIZING: {RuntimeState.STARTING, RuntimeState.FAILED, RuntimeState.STOPPED},
        RuntimeState.STARTING: {RuntimeState.RUNNING, RuntimeState.FAILED, RuntimeState.DEGRADED},
        RuntimeState.RUNNING: {RuntimeState.DEGRADED, RuntimeState.STOPPING, RuntimeState.FAILED, RuntimeState.RECOVERING},
        RuntimeState.DEGRADED: {RuntimeState.RUNNING, RuntimeState.RECOVERING, RuntimeState.STOPPING, RuntimeState.FAILED},
        RuntimeState.STOPPING: {RuntimeState.STOPPED, RuntimeState.FAILED},
        RuntimeState.STOPPED: {RuntimeState.INITIALIZING, RuntimeState.STARTING, RuntimeState.CREATED},
        RuntimeState.FAILED: {RuntimeState.RECOVERING, RuntimeState.STOPPED, RuntimeState.CREATED},
        RuntimeState.RECOVERING: {RuntimeState.RUNNING, RuntimeState.DEGRADED, RuntimeState.FAILED, RuntimeState.STOPPED},
    }

    @classmethod
    def can_transition(cls, from_state: RuntimeState, to_state: RuntimeState) -> bool:
        return to_state in cls.ALLOWED_TRANSITIONS.get(from_state, set())

    @classmethod
    def transition(cls, current_state: RuntimeState, target_state: RuntimeState) -> RuntimeState:
        if not cls.can_transition(current_state, target_state):
            raise InvalidStateTransitionError(
                f"Invalid runtime transition from {current_state.value} to {target_state.value}."
            )
        return target_state


class ResourceLifecycleStateMachine:
    """Enforces valid state transitions for allocated infrastructure resources."""

    ALLOWED_TRANSITIONS: Dict[ResourceState, Set[ResourceState]] = {
        ResourceState.REQUESTED: {ResourceState.ALLOCATING, ResourceState.FAILED},
        ResourceState.ALLOCATING: {ResourceState.READY, ResourceState.FAILED},
        ResourceState.READY: {ResourceState.ACTIVE, ResourceState.DRAINING, ResourceState.RELEASED, ResourceState.FAILED},
        ResourceState.ACTIVE: {ResourceState.DRAINING, ResourceState.FAILED, ResourceState.READY},
        ResourceState.DRAINING: {ResourceState.RELEASED, ResourceState.FAILED, ResourceState.ACTIVE},
        ResourceState.RELEASED: set(),
        ResourceState.FAILED: {ResourceState.ALLOCATING, ResourceState.RELEASED},
    }

    @classmethod
    def can_transition(cls, from_state: ResourceState, to_state: ResourceState) -> bool:
        return to_state in cls.ALLOWED_TRANSITIONS.get(from_state, set())

    @classmethod
    def transition(cls, current_state: ResourceState, target_state: ResourceState) -> ResourceState:
        if not cls.can_transition(current_state, target_state):
            raise InvalidStateTransitionError(
                f"Invalid resource transition from {current_state.value} to {target_state.value}."
            )
        return target_state
