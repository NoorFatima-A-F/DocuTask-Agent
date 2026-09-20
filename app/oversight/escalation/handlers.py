"""Escalation Event Handlers and Alert Generation."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid

from .rules import EscalationLevel, EscalationRule
from ..reviews.requests import ReviewRequest, ReviewPriority


class EscalationEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"escevt_{uuid.uuid4().hex[:8]}")
    review_id: str
    tenant_id: str
    from_level: EscalationLevel
    to_level: EscalationLevel
    escalated_to_roles: List[str]
    reason: str
    escalated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EscalationHandler:
    """Dispatches escalation events and bumps review priorities."""

    def __init__(self):
        self._events: List[EscalationEvent] = []

    def handle_escalation(
        self,
        request: ReviewRequest,
        rule: EscalationRule,
        reason: str,
    ) -> EscalationEvent:
        from_level = EscalationLevel(request.escalation_level)
        to_level = rule.target_level

        # Update request
        request.escalation_level = int(to_level)
        request.required_roles = list(rule.target_roles)
        if rule.priority_bump:
            if request.priority == ReviewPriority.LOW:
                request.priority = ReviewPriority.MEDIUM
            elif request.priority == ReviewPriority.MEDIUM:
                request.priority = ReviewPriority.HIGH
            elif request.priority == ReviewPriority.HIGH:
                request.priority = ReviewPriority.URGENT
            elif request.priority == ReviewPriority.URGENT:
                request.priority = ReviewPriority.CRITICAL

        event = EscalationEvent(
            review_id=request.review_id,
            tenant_id=request.tenant_id,
            from_level=from_level,
            to_level=to_level,
            escalated_to_roles=rule.target_roles,
            reason=reason,
            metadata={"rule_id": rule.rule_id, "new_priority": request.priority.value},
        )
        self._events.append(event)
        return event

    def get_events_for_review(self, review_id: str) -> List[EscalationEvent]:
        return [e for e in self._events if e.review_id == review_id]
