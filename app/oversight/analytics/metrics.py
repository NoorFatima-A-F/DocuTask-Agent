"""Human Oversight Analytics, Metrics Aggregation, and Feedback Telemetry."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from ..core.decisions import HumanDecision, DecisionOutcome, FeedbackAssessment
from ..reviews.requests import ReviewRequest
from ..overrides.service import HumanOverrideRecord


class OversightAnalyticsSummary(BaseModel):
    """Aggregated governance analytics and telemetry summary."""
    tenant_id: str
    total_reviews: int = 0
    approved_count: int = 0
    rejected_count: int = 0
    escalated_count: int = 0
    override_count: int = 0
    approval_rate: float = 0.0
    rejection_rate: float = 0.0
    override_rate: float = 0.0
    avg_turnaround_time_seconds: float = 0.0
    feedback_breakdown: Dict[str, int] = Field(default_factory=dict)
    ai_correctness_rate: float = 1.0


class OversightMetricsCollector:
    """Collects and computes real-time oversight metrics and feedback loops."""

    def __init__(self):
        self._reviews: List[ReviewRequest] = []
        self._decisions: List[HumanDecision] = []
        self._overrides: List[HumanOverrideRecord] = []

    def record_review(self, review: ReviewRequest) -> None:
        self._reviews.append(review)

    def record_decision(self, decision: HumanDecision) -> None:
        self._decisions.append(decision)

    def record_override(self, override: HumanOverrideRecord) -> None:
        self._overrides.append(override)

    def compute_summary(self, tenant_id: str = "*") -> OversightAnalyticsSummary:
        reviews = [r for r in self._reviews if tenant_id == "*" or r.tenant_id == tenant_id]
        decisions = [d for d in self._decisions if tenant_id == "*" or d.tenant_id == tenant_id]
        overrides = [o for o in self._overrides if tenant_id == "*" or o.tenant_id == tenant_id]

        total = len(reviews)
        approved = sum(1 for d in decisions if d.outcome == DecisionOutcome.APPROVED)
        rejected = sum(1 for d in decisions if d.outcome == DecisionOutcome.REJECTED)
        escalated = sum(1 for d in decisions if d.outcome == DecisionOutcome.ESCALATED)
        override_cnt = len(overrides)

        approval_rate = (approved / len(decisions)) if decisions else 0.0
        rejection_rate = (rejected / len(decisions)) if decisions else 0.0
        override_rate = (override_cnt / total) if total else 0.0

        # Turnaround times
        turnaround_times = []
        for r in reviews:
            if r.closed_at and r.created_at:
                turnaround_times.append((r.closed_at - r.created_at).total_seconds())

        avg_turnaround = (sum(turnaround_times) / len(turnaround_times)) if turnaround_times else 0.0

        # Feedback breakdown
        fb_counts: Dict[str, int] = {}
        ai_correct_cnt = 0
        total_feedback = 0

        for d in decisions:
            if d.feedback:
                fb_str = d.feedback.value
                fb_counts[fb_str] = fb_counts.get(fb_str, 0) + 1
                total_feedback += 1
                if d.feedback == FeedbackAssessment.AI_CORRECT:
                    ai_correct_cnt += 1

        ai_correctness_rate = (ai_correct_cnt / total_feedback) if total_feedback else 1.0

        return OversightAnalyticsSummary(
            tenant_id=tenant_id,
            total_reviews=total,
            approved_count=approved,
            rejected_count=rejected,
            escalated_count=escalated,
            override_count=override_cnt,
            approval_rate=round(approval_rate, 4),
            rejection_rate=round(rejection_rate, 4),
            override_rate=round(override_rate, 4),
            avg_turnaround_time_seconds=round(avg_turnaround, 2),
            feedback_breakdown=fb_counts,
            ai_correctness_rate=round(ai_correctness_rate, 4),
        )
