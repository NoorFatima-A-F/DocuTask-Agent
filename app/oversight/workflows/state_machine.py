"""Approval Lifecycle State Machine."""

from typing import Dict, Any, List, Optional, Set, Tuple
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid

from ..approvals.lifecycle import ApprovalLifecycleState
from ..core.exceptions import OversightException


class StateTransitionEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:8]}")
    review_id: str
    from_state: ApprovalLifecycleState
    to_state: ApprovalLifecycleState
    actor_id: str
    reason: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ApprovalStateMachine:
    """Strict transition validator and history recorder for approval state lifecycles."""

    VALID_TRANSITIONS: Dict[ApprovalLifecycleState, Set[ApprovalLifecycleState]] = {
        ApprovalLifecycleState.CREATED: {
            ApprovalLifecycleState.PENDING_REVIEW,
            ApprovalLifecycleState.CANCELLED,
        },
        ApprovalLifecycleState.PENDING_REVIEW: {
            ApprovalLifecycleState.ASSIGNED,
            ApprovalLifecycleState.IN_REVIEW,
            ApprovalLifecycleState.CANCELLED,
            ApprovalLifecycleState.EXPIRED,
        },
        ApprovalLifecycleState.ASSIGNED: {
            ApprovalLifecycleState.IN_REVIEW,
            ApprovalLifecycleState.ESCALATED,
            ApprovalLifecycleState.CANCELLED,
            ApprovalLifecycleState.EXPIRED,
        },
        ApprovalLifecycleState.IN_REVIEW: {
            ApprovalLifecycleState.APPROVED,
            ApprovalLifecycleState.REJECTED,
            ApprovalLifecycleState.ESCALATED,
            ApprovalLifecycleState.EXPIRED,
            ApprovalLifecycleState.CANCELLED,
        },
        ApprovalLifecycleState.APPROVED: {
            ApprovalLifecycleState.ARCHIVED,
        },
        ApprovalLifecycleState.REJECTED: {
            ApprovalLifecycleState.ARCHIVED,
        },
        ApprovalLifecycleState.ESCALATED: {
            ApprovalLifecycleState.ASSIGNED,
            ApprovalLifecycleState.IN_REVIEW,
            ApprovalLifecycleState.APPROVED,
            ApprovalLifecycleState.REJECTED,
            ApprovalLifecycleState.EXPIRED,
            ApprovalLifecycleState.CANCELLED,
        },
        ApprovalLifecycleState.EXPIRED: {
            ApprovalLifecycleState.ARCHIVED,
        },
        ApprovalLifecycleState.CANCELLED: {
            ApprovalLifecycleState.ARCHIVED,
        },
        ApprovalLifecycleState.ARCHIVED: set(),  # Terminal state
    }

    def __init__(self):
        self._history: Dict[str, List[StateTransitionEvent]] = {}

    def can_transition(
        self, current_state: ApprovalLifecycleState, target_state: ApprovalLifecycleState
    ) -> bool:
        allowed = self.VALID_TRANSITIONS.get(current_state, set())
        return target_state in allowed

    def transition(
        self,
        review_id: str,
        current_state: ApprovalLifecycleState,
        target_state: ApprovalLifecycleState,
        actor_id: str,
        reason: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> StateTransitionEvent:
        """Executes and records a lifecycle state transition."""
        if not self.can_transition(current_state, target_state):
            raise OversightException(
                f"Invalid lifecycle transition from '{current_state.value}' to '{target_state.value}'"
            )

        event = StateTransitionEvent(
            review_id=review_id,
            from_state=current_state,
            to_state=target_state,
            actor_id=actor_id,
            reason=reason,
            metadata=metadata or {},
        )

        if review_id not in self._history:
            self._history[review_id] = []
        self._history[review_id].append(event)
        return event

    def get_history(self, review_id: str) -> List[StateTransitionEvent]:
        return self._history.get(review_id, [])
