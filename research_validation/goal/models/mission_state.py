"""
Mission State & Finite State Machine (FSM) Model
================================================
Defines the 14 formal states of the mission lifecycle and transition validation rules.
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set

from research_validation.goal.exceptions import InvalidStateTransitionError


class MissionState(str, Enum):
    CREATED = "CREATED"
    VALIDATING = "VALIDATING"
    VALIDATED = "VALIDATED"
    ANALYZING_CAPABILITIES = "ANALYZING_CAPABILITIES"
    ANALYZING_DEPENDENCIES = "ANALYZING_DEPENDENCIES"
    ANALYZING_RISK = "ANALYZING_RISK"
    ESTIMATING_BUDGET = "ESTIMATING_BUDGET"
    GENERATING_SUCCESS_CRITERIA = "GENERATING_SUCCESS_CRITERIA"
    READY_FOR_OBSERVATION = "READY_FOR_OBSERVATION"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ABORTED = "ABORTED"
    ARCHIVED = "ARCHIVED"


# Permitted state transition map
PERMITTED_TRANSITIONS: Dict[MissionState, Set[MissionState]] = {
    MissionState.CREATED: {MissionState.VALIDATING, MissionState.ABORTED},
    MissionState.VALIDATING: {MissionState.VALIDATED, MissionState.FAILED, MissionState.ABORTED},
    MissionState.VALIDATED: {MissionState.ANALYZING_CAPABILITIES, MissionState.ABORTED},
    MissionState.ANALYZING_CAPABILITIES: {MissionState.ANALYZING_DEPENDENCIES, MissionState.FAILED, MissionState.ABORTED},
    MissionState.ANALYZING_DEPENDENCIES: {MissionState.ANALYZING_RISK, MissionState.FAILED, MissionState.ABORTED},
    MissionState.ANALYZING_RISK: {MissionState.ESTIMATING_BUDGET, MissionState.FAILED, MissionState.ABORTED},
    MissionState.ESTIMATING_BUDGET: {MissionState.GENERATING_SUCCESS_CRITERIA, MissionState.FAILED, MissionState.ABORTED},
    MissionState.GENERATING_SUCCESS_CRITERIA: {MissionState.READY_FOR_OBSERVATION, MissionState.FAILED, MissionState.ABORTED},
    MissionState.READY_FOR_OBSERVATION: {MissionState.ACTIVE, MissionState.PAUSED, MissionState.ABORTED, MissionState.ARCHIVED},
    MissionState.ACTIVE: {MissionState.PAUSED, MissionState.COMPLETED, MissionState.FAILED, MissionState.ABORTED},
    MissionState.PAUSED: {MissionState.ACTIVE, MissionState.ABORTED, MissionState.ARCHIVED},
    MissionState.COMPLETED: {MissionState.ARCHIVED},
    MissionState.FAILED: {MissionState.ARCHIVED, MissionState.VALIDATING},  # retry
    MissionState.ABORTED: {MissionState.ARCHIVED},
    MissionState.ARCHIVED: set(),  # terminal state
}


@dataclass(frozen=True)
class StateTransitionRecord:
    """Audit record of a single state transition in the mission lifecycle."""
    from_state: MissionState
    to_state: MissionState
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    trigger: str = ""
    actor: str = "GOAL_INTELLIGENCE_ENGINE"
    rationale: str = ""
    transition_digest_sha256: str = field(default="")


class MissionStateMachine:
    """
    Validates and executes deterministic state transitions for missions.
    """

    @classmethod
    def validate_transition(cls, current_state: MissionState, next_state: MissionState) -> bool:
        """Checks if transition is mathematically valid according to the FSM grammar."""
        allowed = PERMITTED_TRANSITIONS.get(current_state, set())
        return next_state in allowed

    @classmethod
    def assert_transition(cls, current_state: MissionState, next_state: MissionState, rationale: str = "") -> None:
        """Asserts validity or raises an InvalidStateTransitionError."""
        if not cls.validate_transition(current_state, next_state):
            allowed = [s.value for s in PERMITTED_TRANSITIONS.get(current_state, set())]
            raise InvalidStateTransitionError(
                current_state=current_state.value,
                attempted_state=next_state.value,
                rationale=f"Permitted next states from '{current_state.value}': {allowed}. {rationale}".strip(),
            )
