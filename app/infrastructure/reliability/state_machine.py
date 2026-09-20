"""
Reliability Lifecycle State Machine.

Manages strict state transitions, invariant verification, and audit logging
for components, services, and regions across the 7 reliability states.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional, Set, Tuple

from app.infrastructure.reliability.models import (
    ReliabilityState,
    ReliabilityTransitionRecord,
)

logger = logging.getLogger("infrastructure.reliability.state_machine")


class ReliabilityInvalidTransitionError(Exception):
    """Raised when an invalid reliability state transition is attempted."""
    pass


class ReliabilityLifecycleStateMachine:
    """
    State machine enforcing 7-state transitions for reliability lifecycles:
    OPTIMAL -> DEGRADED -> FAILING -> PARTIALLY_FAILED / OUTAGE -> RECOVERING -> RECOVERED -> OPTIMAL.
    """

    VALID_TRANSITIONS: Dict[ReliabilityState, Set[ReliabilityState]] = {
        ReliabilityState.OPTIMAL: {
            ReliabilityState.DEGRADED,
            ReliabilityState.FAILING,
            ReliabilityState.OUTAGE,
        },
        ReliabilityState.DEGRADED: {
            ReliabilityState.OPTIMAL,
            ReliabilityState.FAILING,
            ReliabilityState.PARTIALLY_FAILED,
            ReliabilityState.OUTAGE,
            ReliabilityState.RECOVERING,
        },
        ReliabilityState.FAILING: {
            ReliabilityState.DEGRADED,
            ReliabilityState.PARTIALLY_FAILED,
            ReliabilityState.OUTAGE,
            ReliabilityState.RECOVERING,
        },
        ReliabilityState.PARTIALLY_FAILED: {
            ReliabilityState.OUTAGE,
            ReliabilityState.RECOVERING,
            ReliabilityState.DEGRADED,
        },
        ReliabilityState.OUTAGE: {
            ReliabilityState.RECOVERING,
        },
        ReliabilityState.RECOVERING: {
            ReliabilityState.RECOVERED,
            ReliabilityState.FAILING,
            ReliabilityState.OUTAGE,
            ReliabilityState.PARTIALLY_FAILED,
        },
        ReliabilityState.RECOVERED: {
            ReliabilityState.OPTIMAL,
            ReliabilityState.DEGRADED,
            ReliabilityState.RECOVERING,
        },
    }

    def __init__(self, component_id: str, initial_state: ReliabilityState = ReliabilityState.OPTIMAL) -> None:
        self.component_id = component_id
        self._current_state = initial_state
        self._history: List[ReliabilityTransitionRecord] = []
        self._transition_hooks: List[Callable[[ReliabilityTransitionRecord], None]] = []

    @property
    def current_state(self) -> ReliabilityState:
        return self._current_state

    @property
    def history(self) -> List[ReliabilityTransitionRecord]:
        return list(self._history)

    def register_hook(self, hook: Callable[[ReliabilityTransitionRecord], None]) -> None:
        """Register a callback for successful state transitions."""
        self._transition_hooks.append(hook)

    def can_transition_to(self, target_state: ReliabilityState) -> bool:
        """Check if transition from current state to target state is permissible."""
        if target_state == self._current_state:
            return True
        allowed = self.VALID_TRANSITIONS.get(self._current_state, set())
        return target_state in allowed

    def transition_to(
        self,
        target_state: ReliabilityState,
        reason: str,
        trigger_source: str = "system",
        metadata: Optional[Dict] = None,
    ) -> ReliabilityTransitionRecord:
        """
        Transition the state machine to target_state with validation and auditing.
        """
        if target_state == self._current_state:
            # No-op transition
            record = ReliabilityTransitionRecord(
                component_id=self.component_id,
                from_state=self._current_state,
                to_state=target_state,
                reason=f"No-op transition: already in {target_state}",
                trigger_source=trigger_source,
                metadata=metadata or {},
            )
            return record

        if not self.can_transition_to(target_state):
            err = (
                f"Invalid reliability state transition for '{self.component_id}' "
                f"from {self._current_state.value} to {target_state.value}. "
                f"Allowed transitions: {[s.value for s in self.VALID_TRANSITIONS.get(self._current_state, set())]}"
            )
            logger.error(err)
            raise ReliabilityInvalidTransitionError(err)

        from_state = self._current_state
        self._current_state = target_state

        record = ReliabilityTransitionRecord(
            component_id=self.component_id,
            from_state=from_state,
            to_state=target_state,
            reason=reason,
            trigger_source=trigger_source,
            metadata=metadata or {},
        )
        self._history.append(record)

        for hook in self._transition_hooks:
            try:
                hook(record)
            except Exception as e:
                logger.warning(f"Error executing transition hook for {self.component_id}: {e}")

        logger.info(
            f"Component '{self.component_id}' transitioned from {from_state.value} "
            f"to {target_state.value}. Reason: {reason}"
        )
        return record
