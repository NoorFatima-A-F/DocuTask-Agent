"""
Agent State Machine & Transitions.
Provides production-grade state machine enforcing valid agent state transitions.
States: Created, Initialized, Planning, Executing, Observing, Reflecting, Waiting, Retrying, Completed, Failed, Cancelled.
"""

from enum import Enum
from typing import Dict, List, Set
from app.agents.exceptions import InvalidStateTransitionException


class AgentState(Enum):
    """Production Agent States."""
    CREATED = "CREATED"
    INITIALIZED = "INITIALIZED"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    OBSERVING = "OBSERVING"
    REFLECTING = "REFLECTING"
    WAITING = "WAITING"
    RETRYING = "RETRYING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class AgentStateMachine:
    """
    Validated Agent State Machine.
    Enforces deterministic state transitions and prevents invalid state mutations.
    """

    # Strictly allowed state transitions
    _ALLOWED_TRANSITIONS: Dict[AgentState, Set[AgentState]] = {
        AgentState.CREATED: {AgentState.INITIALIZED, AgentState.CANCELLED},
        AgentState.INITIALIZED: {AgentState.PLANNING, AgentState.CANCELLED, AgentState.FAILED},
        AgentState.PLANNING: {AgentState.EXECUTING, AgentState.FAILED, AgentState.CANCELLED},
        AgentState.EXECUTING: {AgentState.OBSERVING, AgentState.WAITING, AgentState.RETRYING, AgentState.FAILED, AgentState.CANCELLED},
        AgentState.OBSERVING: {AgentState.REFLECTING, AgentState.FAILED, AgentState.CANCELLED},
        AgentState.REFLECTING: {AgentState.COMPLETED, AgentState.PLANNING, AgentState.EXECUTING, AgentState.RETRYING, AgentState.FAILED, AgentState.CANCELLED},
        AgentState.WAITING: {AgentState.EXECUTING, AgentState.CANCELLED, AgentState.FAILED},
        AgentState.RETRYING: {AgentState.PLANNING, AgentState.EXECUTING, AgentState.FAILED, AgentState.CANCELLED},
        AgentState.COMPLETED: set(),
        AgentState.FAILED: set(),
        AgentState.CANCELLED: set(),
    }

    def __init__(self, initial_state: AgentState = AgentState.CREATED):
        self._current_state = initial_state
        self._history: List[AgentState] = [initial_state]

    @property
    def current_state(self) -> AgentState:
        """Returns the current state of the agent state machine."""
        return self._current_state

    @property
    def history(self) -> List[AgentState]:
        """Returns the state transition history log."""
        return list(self._history)

    def is_terminal(self) -> bool:
        """Checks if current state is a terminal state (Completed, Failed, Cancelled)."""
        return self._current_state in {AgentState.COMPLETED, AgentState.FAILED, AgentState.CANCELLED}

    def can_transition_to(self, target_state: AgentState) -> bool:
        """Returns True if transition from current state to target state is valid."""
        allowed = self._ALLOWED_TRANSITIONS.get(self._current_state, set())
        return target_state in allowed

    def transition_to(self, target_state: AgentState) -> None:
        """
        Transitions the state machine to target state.
        Raises InvalidStateTransitionException if transition is invalid.
        """
        if not self.can_transition_to(target_state):
            raise InvalidStateTransitionException(
                f"Invalid agent state transition: Cannot transition from {self._current_state.value} to {target_state.value}."
            )
        self._current_state = target_state
        self._history.append(target_state)
