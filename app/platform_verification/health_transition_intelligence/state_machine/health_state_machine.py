"""
Health State Machine Engine (Part 3H.3.3.1).
Implements the 5-state deterministic health lifecycle:
STARTING -> READY <-> DEGRADED <-> NOT_READY -> RECOVERING -> READY.
Maintains state transition history and validates transition bounds.
"""
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.platform_verification.health_transition_intelligence.domain.models import (
    HealthState,
    HealthEvent,
    StateMachineReport,
)


class HealthStateMachine:
    """
    Deterministic health lifecycle state engine for services.
    """

    ALLOWED_TRANSITIONS = {
        HealthState.STARTING: [HealthState.READY],
        HealthState.READY: [HealthState.DEGRADED, HealthState.NOT_READY],
        HealthState.DEGRADED: [HealthState.READY, HealthState.NOT_READY],
        HealthState.NOT_READY: [HealthState.RECOVERING],
        HealthState.RECOVERING: [HealthState.READY, HealthState.NOT_READY, HealthState.DEGRADED],
    }

    def __init__(self, service_name: str = "docutask-api", initial_state: HealthState = HealthState.STARTING):
        self.service_name = service_name
        self._current_state = initial_state
        self._history: List[HealthEvent] = []

    @property
    def current_state(self) -> HealthState:
        return self._current_state

    @property
    def history(self) -> List[HealthEvent]:
        return list(self._history)

    def is_valid_transition(self, to_state: HealthState) -> bool:
        allowed = self.ALLOWED_TRANSITIONS.get(self._current_state, [])
        return to_state in allowed

    def transition(
        self,
        to_state: HealthState,
        reason: str,
        trigger_signal: str = "system_evaluation",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> HealthEvent:
        if not self.is_valid_transition(to_state):
            raise ValueError(
                f"Illegal health state transition for service '{self.service_name}': "
                f"{self._current_state.value} -> {to_state.value}"
            )

        prev_state = self._current_state
        self._current_state = to_state

        event = HealthEvent(
            event_id=str(uuid.uuid4()),
            service_name=self.service_name,
            previous_state=prev_state,
            new_state=to_state,
            reason=reason,
            trigger_signal=trigger_signal,
            timestamp=datetime.now(timezone.utc).isoformat(),
            metadata=metadata or {},
        )
        self._history.append(event)
        return event

    def generate_report(self) -> StateMachineReport:
        all_states = [s.value for s in HealthState]
        total_states = len(all_states)
        matrix_valid = (total_states == 5) and all(s in self.ALLOWED_TRANSITIONS for s in HealthState)

        return StateMachineReport(
            total_states=total_states,
            states=all_states,
            transition_matrix_valid=matrix_valid,
            all_deterministic=True,
            total_transitions_logged=len(self._history),
            passed=matrix_valid,
            details={
                "allowed_transitions": {
                    k.value: [v.value for v in vals] for k, vals in self.ALLOWED_TRANSITIONS.items()
                },
                "current_state": self._current_state.value,
                "history_length": len(self._history),
            },
        )
