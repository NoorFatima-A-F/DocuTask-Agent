"""
Autonomous Runtime State Machine.
Defines the deterministic lifecycle states and valid transitions of the autonomous agent operating system.
"""

from __future__ import annotations

import logging
from enum import Enum
from typing import Dict, Set

logger = logging.getLogger(__name__)


class AutonomousState(str, Enum):
    CREATED = "CREATED"
    INITIALIZING = "INITIALIZING"
    OBSERVING = "OBSERVING"
    REASONING = "REASONING"
    PLANNING = "PLANNING"
    OPTIMIZING = "OPTIMIZING"
    EXECUTING = "EXECUTING"
    REFLECTING = "REFLECTING"
    LEARNING = "LEARNING"
    PAUSED_FOR_HUMAN = "PAUSED_FOR_HUMAN"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# Permitted state transition graph
VALID_TRANSITIONS: Dict[AutonomousState, Set[AutonomousState]] = {
    AutonomousState.CREATED: {AutonomousState.INITIALIZING, AutonomousState.FAILED},
    AutonomousState.INITIALIZING: {AutonomousState.OBSERVING, AutonomousState.FAILED},
    AutonomousState.OBSERVING: {AutonomousState.REASONING, AutonomousState.FAILED},
    AutonomousState.REASONING: {AutonomousState.PLANNING, AutonomousState.FAILED},
    AutonomousState.PLANNING: {AutonomousState.OPTIMIZING, AutonomousState.FAILED},
    AutonomousState.OPTIMIZING: {AutonomousState.EXECUTING, AutonomousState.FAILED},
    AutonomousState.EXECUTING: {
        AutonomousState.REFLECTING,
        AutonomousState.PAUSED_FOR_HUMAN,
        AutonomousState.FAILED,
    },
    AutonomousState.REFLECTING: {
        AutonomousState.LEARNING,
        AutonomousState.PLANNING,  # Self-correction loop
        AutonomousState.PAUSED_FOR_HUMAN,
        AutonomousState.FAILED,
    },
    AutonomousState.LEARNING: {AutonomousState.COMPLETED, AutonomousState.OBSERVING, AutonomousState.FAILED},
    AutonomousState.PAUSED_FOR_HUMAN: {
        AutonomousState.EXECUTING,
        AutonomousState.PLANNING,
        AutonomousState.FAILED,
    },
    AutonomousState.COMPLETED: set(),
    AutonomousState.FAILED: {AutonomousState.INITIALIZING},  # Restart / Recovery
}


class RuntimeStateMachine:
    """Manages state transitions with guard validation."""

    def __init__(self, initial_state: AutonomousState = AutonomousState.CREATED) -> None:
        self._current_state = initial_state
        self._transition_history: list[tuple[AutonomousState, AutonomousState]] = []

    @property
    def current_state(self) -> AutonomousState:
        return self._current_state

    def can_transition_to(self, target_state: AutonomousState) -> bool:
        """Checks if transition is valid from current state."""
        allowed = VALID_TRANSITIONS.get(self._current_state, set())
        return target_state in allowed

    def transition_to(self, target_state: AutonomousState) -> AutonomousState:
        """Executes a validated state transition."""
        if not self.can_transition_to(target_state):
            msg = f"Invalid state transition from {self._current_state.value} to {target_state.value}"
            logger.error(msg)
            raise ValueError(msg)

        prev_state = self._current_state
        self._current_state = target_state
        self._transition_history.append((prev_state, target_state))
        logger.info("Autonomous State: %s -> %s", prev_state.value, target_state.value)
        return self._current_state

    def reset(self) -> None:
        self._current_state = AutonomousState.CREATED
        self._transition_history.clear()

    @property
    def history(self) -> list[tuple[AutonomousState, AutonomousState]]:
        return list(self._transition_history)
