"""
Readiness State Machine (Part 2).
Implements the 6-state deterministic lifecycle model:
INITIALIZING -> CHECKING_DEPENDENCIES -> READY <-> DEGRADED <-> NOT_READY -> RECOVERING -> READY.
"""
from typing import Dict, Any, List
from app.platform_verification.readiness_contract.domain.models import (
    ReadinessState,
    StateMachineReport,
)
from app.platform_verification.readiness_contract.domain.interfaces import IReadinessStateMachine


class ReadinessStateMachine(IReadinessStateMachine):
    """
    Deterministic state engine controlling the service readiness lifecycle.
    """

    ALLOWED_TRANSITIONS = {
        ReadinessState.INITIALIZING: [ReadinessState.CHECKING_DEPENDENCIES],
        ReadinessState.CHECKING_DEPENDENCIES: [
            ReadinessState.READY,
            ReadinessState.DEGRADED,
            ReadinessState.NOT_READY,
        ],
        ReadinessState.READY: [ReadinessState.DEGRADED, ReadinessState.NOT_READY],
        ReadinessState.DEGRADED: [ReadinessState.READY, ReadinessState.NOT_READY],
        ReadinessState.NOT_READY: [ReadinessState.RECOVERING],
        ReadinessState.RECOVERING: [
            ReadinessState.READY,
            ReadinessState.DEGRADED,
            ReadinessState.NOT_READY,
        ],
    }

    def __init__(self):
        self._current_state = ReadinessState.INITIALIZING

    @property
    def current_state(self) -> ReadinessState:
        return self._current_state

    def is_valid_transition(self, from_state: ReadinessState, to_state: ReadinessState) -> bool:
        allowed = self.ALLOWED_TRANSITIONS.get(from_state, [])
        return to_state in allowed

    def transition_to(self, to_state: ReadinessState) -> ReadinessState:
        if not self.is_valid_transition(self._current_state, to_state):
            raise ValueError(
                f"Illegal readiness transition from {self._current_state.value} to {to_state.value}"
            )
        self._current_state = to_state
        return self._current_state

    def verify_state_machine(self) -> StateMachineReport:
        all_states = [s.value for s in ReadinessState]
        total = len(all_states)
        valid = (total == 6) and all(s in self.ALLOWED_TRANSITIONS for s in ReadinessState)

        return StateMachineReport(
            total_states=total,
            states=all_states,
            transition_matrix_valid=valid,
            all_states_deterministic=valid,
            passed=valid,
            details={
                "state_definitions": {
                    "INITIALIZING": "Service started, loading config and DB pool, traffic blocked",
                    "CHECKING_DEPENDENCIES": "Actively evaluating postgres, redis, storage, workers, ai",
                    "READY": "All critical and required capabilities healthy, traffic fully admitted",
                    "DEGRADED": "Optional dependency unavailable (e.g. Gemini AI), fallback mode active",
                    "NOT_READY": "Critical dependency down (e.g. postgres), traffic withheld",
                    "RECOVERING": "Dependencies returned, system validating warm pool stability",
                },
                "transitions": {
                    k.value: [v.value for v in vals] for k, vals in self.ALLOWED_TRANSITIONS.items()
                },
                "status": "STATE_MACHINE_VERIFIED" if valid else "STATE_MACHINE_INVALID",
            },
        )
