"""Deployment Lifecycle and State Machine Engine."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Set
from .exceptions import DeploymentException


class DeploymentStatus(str, Enum):
    """Lifecycle states for deployments."""
    PENDING = "PENDING"
    VALIDATING = "VALIDATING"
    PREPARING = "PREPARING"
    DEPLOYING = "DEPLOYING"
    VERIFYING = "VERIFYING"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    DECOMMISSIONED = "DECOMMISSIONED"


@dataclass
class StateTransitionRecord:
    """Audit record for a single state transition."""
    from_status: DeploymentStatus
    to_status: DeploymentStatus
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reason: Optional[str] = None
    triggered_by: Optional[str] = None


class DeploymentStateEngine:
    """State transition validator and history recorder for deployments."""

    ALLOWED_TRANSITIONS: Dict[DeploymentStatus, Set[DeploymentStatus]] = {
        DeploymentStatus.PENDING: {DeploymentStatus.VALIDATING, DeploymentStatus.FAILED},
        DeploymentStatus.VALIDATING: {DeploymentStatus.PREPARING, DeploymentStatus.FAILED},
        DeploymentStatus.PREPARING: {DeploymentStatus.DEPLOYING, DeploymentStatus.FAILED},
        DeploymentStatus.DEPLOYING: {DeploymentStatus.VERIFYING, DeploymentStatus.FAILED, DeploymentStatus.ROLLED_BACK},
        DeploymentStatus.VERIFYING: {DeploymentStatus.ACTIVE, DeploymentStatus.FAILED, DeploymentStatus.ROLLED_BACK},
        DeploymentStatus.ACTIVE: {DeploymentStatus.ROLLED_BACK, DeploymentStatus.DECOMMISSIONED, DeploymentStatus.FAILED},
        DeploymentStatus.FAILED: {DeploymentStatus.ROLLED_BACK, DeploymentStatus.PENDING, DeploymentStatus.DECOMMISSIONED},
        DeploymentStatus.ROLLED_BACK: {DeploymentStatus.DECOMMISSIONED, DeploymentStatus.PENDING},
        DeploymentStatus.DECOMMISSIONED: set(),
    }

    def __init__(self, initial_status: DeploymentStatus = DeploymentStatus.PENDING):
        self._current_status = initial_status
        self._history: List[StateTransitionRecord] = [
            StateTransitionRecord(
                from_status=initial_status,
                to_status=initial_status,
                reason="Initial state creation",
                triggered_by="system",
            )
        ]

    @property
    def current_status(self) -> DeploymentStatus:
        """Returns the current deployment status."""
        return self._current_status

    @property
    def history(self) -> List[StateTransitionRecord]:
        """Returns historical state transition records."""
        return list(self._history)

    def can_transition_to(self, target_status: DeploymentStatus) -> bool:
        """Checks if a transition to target_status is valid from current status."""
        allowed = self.ALLOWED_TRANSITIONS.get(self._current_status, set())
        return target_status in allowed

    def transition_to(
        self,
        target_status: DeploymentStatus,
        reason: Optional[str] = None,
        triggered_by: Optional[str] = None,
    ) -> StateTransitionRecord:
        """Transitions to the target status if valid, otherwise raises DeploymentException."""
        if not self.can_transition_to(target_status):
            raise DeploymentException(
                f"Invalid state transition from {self._current_status.value} to {target_status.value}. "
                f"Allowed transitions: {[s.value for s in self.ALLOWED_TRANSITIONS.get(self._current_status, set())]}"
            )

        record = StateTransitionRecord(
            from_status=self._current_status,
            to_status=target_status,
            reason=reason,
            triggered_by=triggered_by,
        )
        self._current_status = target_status
        self._history.append(record)
        return record
