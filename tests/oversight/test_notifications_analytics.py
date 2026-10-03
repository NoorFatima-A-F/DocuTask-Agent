"""Tests for Notification Dispatcher, Channels, and Oversight Metrics Collector."""

from datetime import datetime, timezone, timedelta
import pytest

from app.oversight.notifications.channels import NotificationChannel, NotificationEventType
from app.oversight.notifications.dispatcher import NotificationDispatcher
from app.oversight.analytics.metrics import OversightMetricsCollector
from app.oversight.reviews.requests import ReviewRequest
from app.oversight.core.decisions import HumanDecision, DecisionOutcome, FeedbackAssessment
from app.oversight.overrides.service import HumanOverrideRecord


def test_notification_dispatcher():
    dispatcher = NotificationDispatcher()
    msg = dispatcher.dispatch(
        event_type=NotificationEventType.REVIEW_ASSIGNED,
        recipient_id="usr_reviewer_1",
        title="New Review Ticket",
        body="Please review extraction payload for invoice 55.",
        channel=NotificationChannel.SLACK,
        review_id="rev_55",
    )

    assert msg.message_id.startswith("notif_")
    assert msg.channel == NotificationChannel.SLACK
    assert len(dispatcher.get_notifications_for_recipient("usr_reviewer_1")) == 1
    assert len(dispatcher.get_notifications_for_review("rev_55")) == 1


def test_oversight_metrics_collector():
    collector = OversightMetricsCollector()
    t_now = datetime.now(timezone.utc)
    t_start = t_now - timedelta(minutes=10)

    # Record 2 reviews
    r1 = ReviewRequest(
        request_id="req_1",
        tenant_id="tenant_x",
        title="Review 1",
        resource_id="res_1",
        created_at=t_start,
        closed_at=t_now,
    )
    r2 = ReviewRequest(
        request_id="req_2",
        tenant_id="tenant_x",
        title="Review 2",
        resource_id="res_2",
        created_at=t_start,
        closed_at=t_now,
    )
    collector.record_review(r1)
    collector.record_review(r2)

    # Record decisions
    d1 = HumanDecision(
        review_id=r1.review_id,
        tenant_id="tenant_x",
        reviewer_id="u1",
        reviewer_role="reviewer",
        outcome=DecisionOutcome.APPROVED,
        reason="Looks great",
        feedback=FeedbackAssessment.AI_CORRECT,
    )
    d2 = HumanDecision(
        review_id=r2.review_id,
        tenant_id="tenant_x",
        reviewer_id="u2",
        reviewer_role="reviewer",
        outcome=DecisionOutcome.REJECTED,
        reason="Hallucinated fields",
        feedback=FeedbackAssessment.AI_INCORRECT,
    )
    collector.record_decision(d1)
    collector.record_decision(d2)

    # Record 1 override
    ovr = HumanOverrideRecord(
        review_id=r2.review_id,
        tenant_id="tenant_x",
        reviewer_id="u2",
        reviewer_role="reviewer",
        original_ai_decision="bad",
        overridden_human_decision="good",
        justification="Manual correction applied",
    )
    collector.record_override(ovr)

    summary = collector.compute_summary("tenant_x")
    assert summary.total_reviews == 2
    assert summary.approved_count == 1
    assert summary.rejected_count == 1
    assert summary.approval_rate == 0.5
    assert summary.rejection_rate == 0.5
    assert summary.override_count == 1
    assert summary.override_rate == 0.5
    assert summary.ai_correctness_rate == 0.5
    assert summary.feedback_breakdown["AI_CORRECT"] == 1
    assert summary.feedback_breakdown["AI_INCORRECT"] == 1
    assert summary.avg_turnaround_time_seconds == pytest.approx(600.0, rel=1e-1)
