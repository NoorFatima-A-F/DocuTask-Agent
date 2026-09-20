"""Tests for Escalation Rules, Handlers, and Timeout Engine."""

from datetime import datetime, timezone, timedelta
import pytest

from app.oversight.reviews.requests import ReviewRequest, ReviewPriority
from app.oversight.approvals.lifecycle import ApprovalLifecycleState
from app.oversight.escalation.rules import EscalationLevel, EscalationRule
from app.oversight.escalation.handlers import EscalationHandler
from app.oversight.escalation.engine import EscalationEngine


def test_escalation_engine_timeout_trigger():
    engine = EscalationEngine()
    created_time = datetime.now(timezone.utc) - timedelta(seconds=2000)  # Breaches L1 (1800s)

    req = ReviewRequest(
        request_id="req_esc_01",
        tenant_id="tenant_1",
        title="Stalled Low-Confidence Review",
        resource_id="doc_99",
        status=ApprovalLifecycleState.ASSIGNED,
        priority=ReviewPriority.MEDIUM,
        created_at=created_time,
        required_roles=["reviewer"],
    )

    escalated, event = engine.check_and_escalate(req)
    assert escalated is True
    assert event is not None
    assert event.to_level == EscalationLevel.LEVEL_1_TEAM_LEAD
    assert req.escalation_level == 1
    assert req.priority == ReviewPriority.HIGH  # Bumped priority
    assert req.status == ApprovalLifecycleState.ESCALATED
    assert "team_lead" in req.required_roles


def test_no_escalation_when_within_sla():
    engine = EscalationEngine()
    created_time = datetime.now(timezone.utc) - timedelta(seconds=300)  # Only 5 min elapsed

    req = ReviewRequest(
        request_id="req_esc_02",
        tenant_id="tenant_1",
        title="Fresh Review Request",
        resource_id="doc_100",
        status=ApprovalLifecycleState.ASSIGNED,
        priority=ReviewPriority.LOW,
        created_at=created_time,
        required_roles=["reviewer"],
    )

    escalated, event = engine.check_and_escalate(req)
    assert escalated is False
    assert event is None
    assert req.escalation_level == 0


def test_no_escalation_on_completed_reviews():
    engine = EscalationEngine()
    old_time = datetime.now(timezone.utc) - timedelta(seconds=10000)

    req = ReviewRequest(
        request_id="req_esc_03",
        tenant_id="tenant_1",
        title="Already Approved Request",
        resource_id="doc_101",
        status=ApprovalLifecycleState.APPROVED,
        created_at=old_time,
    )

    escalated, event = engine.check_and_escalate(req)
    assert escalated is False
