from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Set
from app.shared_kernel.exceptions import InvariantViolationError

class VerificationState(str, Enum):
    DRAFT = "DRAFT"
    DEFINED = "DEFINED"
    PLANNED = "PLANNED"
    READY = "READY"
    EXECUTING = "EXECUTING"
    COLLECTING_EVIDENCE = "COLLECTING_EVIDENCE"
    ANALYZING = "ANALYZING"
    EVALUATING = "EVALUATING"
    CERTIFICATION_PENDING = "CERTIFICATION_PENDING"
    CERTIFIED = "CERTIFIED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

ALLOWED_TRANSITIONS: Dict[VerificationState, Set[VerificationState]] = {
    VerificationState.DRAFT: {VerificationState.DEFINED, VerificationState.CANCELLED},
    VerificationState.DEFINED: {VerificationState.PLANNED, VerificationState.DRAFT, VerificationState.CANCELLED},
    VerificationState.PLANNED: {VerificationState.READY, VerificationState.DEFINED, VerificationState.CANCELLED},
    VerificationState.READY: {VerificationState.EXECUTING, VerificationState.CANCELLED},
    VerificationState.EXECUTING: {VerificationState.COLLECTING_EVIDENCE, VerificationState.FAILED, VerificationState.CANCELLED},
    VerificationState.COLLECTING_EVIDENCE: {VerificationState.ANALYZING, VerificationState.FAILED, VerificationState.CANCELLED},
    VerificationState.ANALYZING: {VerificationState.EVALUATING, VerificationState.FAILED, VerificationState.CANCELLED},
    VerificationState.EVALUATING: {VerificationState.CERTIFICATION_PENDING, VerificationState.REJECTED, VerificationState.FAILED, VerificationState.CANCELLED},
    VerificationState.CERTIFICATION_PENDING: {VerificationState.CERTIFIED, VerificationState.REJECTED, VerificationState.CANCELLED},
    VerificationState.CERTIFIED: {VerificationState.ARCHIVED},
    VerificationState.REJECTED: {VerificationState.ARCHIVED, VerificationState.DRAFT},
    VerificationState.FAILED: {VerificationState.ARCHIVED, VerificationState.READY, VerificationState.DRAFT},
    VerificationState.CANCELLED: {VerificationState.ARCHIVED, VerificationState.DRAFT},
    VerificationState.ARCHIVED: set()
}

@dataclass(frozen=True)
class StateTransitionRecord:
    from_state: VerificationState
    to_state: VerificationState
    actor: str
    reason: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, str] = field(default_factory=dict)

class VerificationStateMachine:
    def __init__(self, initial_state: VerificationState = VerificationState.DRAFT):
        self._current_state = initial_state
        self._history: List[StateTransitionRecord] = []

    @property
    def current_state(self) -> VerificationState:
        return self._current_state

    @property
    def history(self) -> List[StateTransitionRecord]:
        return list(self._history)

    def can_transition_to(self, target_state: VerificationState) -> bool:
        allowed = ALLOWED_TRANSITIONS.get(self._current_state, set())
        return target_state in allowed

    def transition_to(
        self,
        target_state: VerificationState,
        actor: str = "system",
        reason: str = "Lifecycle step progression",
        metadata: Optional[Dict[str, str]] = None
    ) -> StateTransitionRecord:
        if not self.can_transition_to(target_state):
            raise InvariantViolationError(
                f"Invalid lifecycle state transition from '{self._current_state.value}' to '{target_state.value}'. "
                f"Allowed target states: {[s.value for s in ALLOWED_TRANSITIONS.get(self._current_state, set())]}",
                details={"from_state": self._current_state.value, "to_state": target_state.value, "actor": actor}
            )

        record = StateTransitionRecord(
            from_state=self._current_state,
            to_state=target_state,
            actor=actor,
            reason=reason,
            metadata=metadata or {}
        )
        self._current_state = target_state
        self._history.append(record)
        return record


# Backward-compatible 16-Stage Model
class LifecycleState(str, Enum):
    CREATED = "CREATED"
    REGISTERED = "REGISTERED"
    CONFIGURED = "CONFIGURED"
    RESOLVED = "RESOLVED"
    PROVISIONED = "PROVISIONED"
    INITIALIZED = "INITIALIZED"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    EVIDENCE_SEALED = "EVIDENCE_SEALED"
    METRICS_COMPUTED = "METRICS_COMPUTED"
    STATISTICALLY_ANALYZED = "STATISTICALLY_ANALYZED"
    QUALITY_GATED = "QUALITY_GATED"
    CERTIFIED = "CERTIFIED"
    REPORTED = "REPORTED"
    ARCHIVED = "ARCHIVED"
    REPRODUCED = "REPRODUCED"

CANONICAL_16_STAGE_ORDER: List[LifecycleState] = [
    LifecycleState.CREATED,
    LifecycleState.REGISTERED,
    LifecycleState.CONFIGURED,
    LifecycleState.RESOLVED,
    LifecycleState.PROVISIONED,
    LifecycleState.INITIALIZED,
    LifecycleState.SCHEDULED,
    LifecycleState.RUNNING,
    LifecycleState.EVIDENCE_SEALED,
    LifecycleState.METRICS_COMPUTED,
    LifecycleState.STATISTICALLY_ANALYZED,
    LifecycleState.QUALITY_GATED,
    LifecycleState.CERTIFIED,
    LifecycleState.REPORTED,
    LifecycleState.ARCHIVED,
    LifecycleState.REPRODUCED,
]

@dataclass(frozen=True)
class LifecycleTransitionRecord:
    from_state: LifecycleState
    to_state: LifecycleState
    is_valid: bool = True
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class LifecycleStateMachine:
    _VALID_PAIRS = {
        (LifecycleState.CREATED, LifecycleState.REGISTERED),
        (LifecycleState.REGISTERED, LifecycleState.CONFIGURED),
        (LifecycleState.CONFIGURED, LifecycleState.RESOLVED),
        (LifecycleState.RESOLVED, LifecycleState.PROVISIONED),
        (LifecycleState.PROVISIONED, LifecycleState.INITIALIZED),
        (LifecycleState.INITIALIZED, LifecycleState.SCHEDULED),
        (LifecycleState.SCHEDULED, LifecycleState.RUNNING),
        (LifecycleState.RUNNING, LifecycleState.EVIDENCE_SEALED),
        (LifecycleState.EVIDENCE_SEALED, LifecycleState.METRICS_COMPUTED),
        (LifecycleState.METRICS_COMPUTED, LifecycleState.STATISTICALLY_ANALYZED),
        (LifecycleState.STATISTICALLY_ANALYZED, LifecycleState.QUALITY_GATED),
        (LifecycleState.QUALITY_GATED, LifecycleState.CERTIFIED),
        (LifecycleState.CERTIFIED, LifecycleState.REPORTED),
        (LifecycleState.REPORTED, LifecycleState.ARCHIVED),
        (LifecycleState.ARCHIVED, LifecycleState.REPRODUCED),
    }

    @classmethod
    def validate_transition(cls, from_state: LifecycleState, to_state: LifecycleState) -> LifecycleTransitionRecord:
        if (from_state, to_state) in cls._VALID_PAIRS:
            return LifecycleTransitionRecord(from_state=from_state, to_state=to_state, is_valid=True)
        raise ValueError(f"Illegal lifecycle state transition: {from_state.value} -> {to_state.value}")
