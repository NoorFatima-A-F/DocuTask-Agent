"""Deployment and Release State Machines for Platform Delivery Operating System."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Set


class DeploymentState(str, Enum):
    """Authoritative lifecycle states for an enterprise deployment."""
    REQUESTED = "REQUESTED"
    VALIDATING = "VALIDATING"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"
    APPROVED = "APPROVED"
    PREPARING = "PREPARING"
    DEPLOYING = "DEPLOYING"
    VERIFYING = "VERIFYING"
    CANARY = "CANARY"
    PROMOTING = "PROMOTING"
    ACTIVE = "ACTIVE"
    # Failure & Recovery States
    FAILED = "FAILED"
    ABORTED = "ABORTED"
    ROLLING_BACK = "ROLLING_BACK"
    ROLLED_BACK = "ROLLED_BACK"
    QUARANTINED = "QUARANTINED"


class ReleaseState(str, Enum):
    """Lifecycle states for immutable release packages."""
    CREATED = "CREATED"
    BUILDING = "BUILDING"
    VALIDATING = "VALIDATING"
    SECURITY_REVIEW = "SECURITY_REVIEW"
    READY = "READY"
    APPROVED = "APPROVED"
    RELEASED = "RELEASED"
    PROMOTING = "PROMOTING"
    PRODUCTION = "PRODUCTION"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"


@dataclass
class TransitionLog:
    """Historical audit record for state machine transitions."""
    from_state: str
    to_state: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reason: Optional[str] = None
    actor: str = "system"


class DeploymentStateMachine:
    """Strict state machine engine enforcing deployment state transition invariants."""

    VALID_TRANSITIONS: Dict[DeploymentState, Set[DeploymentState]] = {
        DeploymentState.REQUESTED: {DeploymentState.VALIDATING, DeploymentState.FAILED, DeploymentState.ABORTED},
        DeploymentState.VALIDATING: {DeploymentState.AWAITING_APPROVAL, DeploymentState.APPROVED, DeploymentState.FAILED, DeploymentState.QUARANTINED},
        DeploymentState.AWAITING_APPROVAL: {DeploymentState.APPROVED, DeploymentState.ABORTED, DeploymentState.FAILED},
        DeploymentState.APPROVED: {DeploymentState.PREPARING, DeploymentState.ABORTED, DeploymentState.FAILED},
        DeploymentState.PREPARING: {DeploymentState.DEPLOYING, DeploymentState.FAILED, DeploymentState.ROLLING_BACK},
        DeploymentState.DEPLOYING: {DeploymentState.VERIFYING, DeploymentState.CANARY, DeploymentState.FAILED, DeploymentState.ROLLING_BACK},
        DeploymentState.VERIFYING: {DeploymentState.PROMOTING, DeploymentState.ACTIVE, DeploymentState.FAILED, DeploymentState.ROLLING_BACK},
        DeploymentState.CANARY: {DeploymentState.PROMOTING, DeploymentState.ACTIVE, DeploymentState.FAILED, DeploymentState.ABORTED, DeploymentState.ROLLING_BACK},
        DeploymentState.PROMOTING: {DeploymentState.ACTIVE, DeploymentState.FAILED, DeploymentState.ROLLING_BACK},
        DeploymentState.ACTIVE: {DeploymentState.ROLLING_BACK, DeploymentState.QUARANTINED, DeploymentState.FAILED},
        DeploymentState.ROLLING_BACK: {DeploymentState.ROLLED_BACK, DeploymentState.FAILED},
        DeploymentState.FAILED: {DeploymentState.ROLLING_BACK, DeploymentState.REQUESTED, DeploymentState.QUARANTINED},
        DeploymentState.ABORTED: set(),
        DeploymentState.ROLLED_BACK: {DeploymentState.REQUESTED},
        DeploymentState.QUARANTINED: set(),
    }

    def __init__(self, initial_state: DeploymentState = DeploymentState.REQUESTED):
        self._current_state = initial_state
        self._history: List[TransitionLog] = [
            TransitionLog(
                from_state=initial_state.value,
                to_state=initial_state.value,
                reason="Initial state initialized",
                actor="system",
            )
        ]

    @property
    def current_state(self) -> DeploymentState:
        return self._current_state

    @property
    def history(self) -> List[TransitionLog]:
        return list(self._history)

    def can_transition_to(self, target: DeploymentState) -> bool:
        allowed = self.VALID_TRANSITIONS.get(self._current_state, set())
        return target in allowed

    def transition_to(
        self,
        target: DeploymentState,
        reason: Optional[str] = None,
        actor: str = "system",
    ) -> TransitionLog:
        if not self.can_transition_to(target):
            raise ValueError(
                f"Deterministic State Violation: Cannot transition from {self._current_state.value} to {target.value}. "
                f"Valid next states: {[s.value for s in self.VALID_TRANSITIONS.get(self._current_state, set())]}"
            )
        log = TransitionLog(
            from_state=self._current_state.value,
            to_state=target.value,
            reason=reason,
            actor=actor,
        )
        self._current_state = target
        self._history.append(log)
        return log
