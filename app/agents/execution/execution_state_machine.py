"""
Execution State Machine.
Enforces deterministic validated transitions across all 14 execution lifecycle states.
"""

from typing import Dict, Set
from app.agents.execution.exceptions import IllegalStateTransitionException
from app.agents.execution.lifecycle import ExecutionLifecycleState


class ExecutionStateMachine:
    """State machine governing valid transitions for nodes and overall execution sessions."""

    # Explicit allowed transitions matrix for all 14 states
    ALLOWED_TRANSITIONS: Dict[ExecutionLifecycleState, Set[ExecutionLifecycleState]] = {
        ExecutionLifecycleState.CREATED: {
            ExecutionLifecycleState.READY,
            ExecutionLifecycleState.WAITING,
            ExecutionLifecycleState.CANCELLED
        },
        ExecutionLifecycleState.WAITING: {
            ExecutionLifecycleState.READY,
            ExecutionLifecycleState.BLOCKED,
            ExecutionLifecycleState.CANCELLED,
            ExecutionLifecycleState.TIMED_OUT
        },
        ExecutionLifecycleState.READY: {
            ExecutionLifecycleState.SCHEDULED,
            ExecutionLifecycleState.BLOCKED,
            ExecutionLifecycleState.PAUSED,
            ExecutionLifecycleState.CANCELLED
        },
        ExecutionLifecycleState.SCHEDULED: {
            ExecutionLifecycleState.RUNNING,
            ExecutionLifecycleState.PAUSED,
            ExecutionLifecycleState.CANCELLED,
            ExecutionLifecycleState.TIMED_OUT
        },
        ExecutionLifecycleState.RUNNING: {
            ExecutionLifecycleState.COMPLETED,
            ExecutionLifecycleState.FAILED,
            ExecutionLifecycleState.RETRYING,
            ExecutionLifecycleState.ROLLING_BACK,
            ExecutionLifecycleState.PAUSED,
            ExecutionLifecycleState.CANCELLED,
            ExecutionLifecycleState.TIMED_OUT
        },
        ExecutionLifecycleState.BLOCKED: {
            ExecutionLifecycleState.READY,
            ExecutionLifecycleState.WAITING,
            ExecutionLifecycleState.FAILED,
            ExecutionLifecycleState.CANCELLED
        },
        ExecutionLifecycleState.PAUSED: {
            ExecutionLifecycleState.READY,
            ExecutionLifecycleState.SCHEDULED,
            ExecutionLifecycleState.RUNNING,
            ExecutionLifecycleState.CANCELLED
        },
        ExecutionLifecycleState.RETRYING: {
            ExecutionLifecycleState.SCHEDULED,
            ExecutionLifecycleState.RUNNING,
            ExecutionLifecycleState.FAILED,
            ExecutionLifecycleState.CANCELLED
        },
        ExecutionLifecycleState.ROLLING_BACK: {
            ExecutionLifecycleState.ROLLED_BACK,
            ExecutionLifecycleState.FAILED
        },
        ExecutionLifecycleState.ROLLED_BACK: set(),  # Terminal
        ExecutionLifecycleState.COMPLETED: set(),    # Terminal
        ExecutionLifecycleState.FAILED: {
            ExecutionLifecycleState.ROLLING_BACK,
            ExecutionLifecycleState.RETRYING
        },
        ExecutionLifecycleState.CANCELLED: set(),    # Terminal
        ExecutionLifecycleState.TIMED_OUT: {
            ExecutionLifecycleState.ROLLING_BACK,
            ExecutionLifecycleState.FAILED
        }
    }

    @classmethod
    def can_transition(
        cls,
        current_state: ExecutionLifecycleState,
        target_state: ExecutionLifecycleState
    ) -> bool:
        """Checks if transition is valid according to state machine rules."""
        if current_state == target_state:
            return True
        allowed = cls.ALLOWED_TRANSITIONS.get(current_state, set())
        return target_state in allowed

    @classmethod
    def transition(
        cls,
        current_state: ExecutionLifecycleState,
        target_state: ExecutionLifecycleState,
        entity_id: str = "node"
    ) -> ExecutionLifecycleState:
        """Validates and applies transition, raising IllegalStateTransitionException on invalid move."""
        if not cls.can_transition(current_state, target_state):
            raise IllegalStateTransitionException(
                f"Illegal state transition for '{entity_id}' from {current_state.value} to {target_state.value}."
            )
        return target_state
