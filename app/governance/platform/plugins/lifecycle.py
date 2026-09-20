"""Plugin Lifecycle State Machine for Governance Extensions."""

from enum import Enum
from typing import Dict, Set


class PluginState(str, Enum):
    REGISTERED = "REGISTERED"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    REMOVED = "REMOVED"


class PluginLifecycleStateMachine:
    """Enforces valid lifecycle transitions for governance plugins."""

    ALLOWED_TRANSITIONS: Dict[PluginState, Set[PluginState]] = {
        PluginState.REGISTERED: {PluginState.VALIDATED, PluginState.REMOVED},
        PluginState.VALIDATED: {PluginState.APPROVED, PluginState.DISABLED, PluginState.REMOVED},
        PluginState.APPROVED: {PluginState.ACTIVE, PluginState.DISABLED, PluginState.REMOVED},
        PluginState.ACTIVE: {PluginState.DISABLED, PluginState.REMOVED},
        PluginState.DISABLED: {PluginState.ACTIVE, PluginState.APPROVED, PluginState.REMOVED},
        PluginState.REMOVED: set(),
    }

    @classmethod
    def can_transition(cls, from_state: PluginState, to_state: PluginState) -> bool:
        """Check if transition between plugin states is permitted."""
        return to_state in cls.ALLOWED_TRANSITIONS.get(from_state, set())

    @classmethod
    def transition(cls, current_state: PluginState, target_state: PluginState) -> PluginState:
        """Execute state transition or raise error."""
        if not cls.can_transition(current_state, target_state):
            raise ValueError(
                f"Invalid plugin lifecycle transition from {current_state.value} to {target_state.value}."
            )
        return target_state
