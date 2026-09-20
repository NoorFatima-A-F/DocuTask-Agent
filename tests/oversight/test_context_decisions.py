"""Tests for Oversight Context, Human Decision models, and Exceptions."""

import pytest
from app.oversight.core.context import OversightContext
from app.oversight.core.decisions import HumanDecision, DecisionOutcome, FeedbackAssessment
from app.oversight.core.exceptions import (
    OversightException,
    UnauthorizedReviewerError,
    InvalidOverrideError,
    EscalationTimeoutError,
    ApprovalPolicyViolationError,
)


def test_oversight_context_defaults():
    ctx = OversightContext(
        tenant_id="tenant_123",
        action_type="EXTRACT_DOCUMENT",
        resource_id="doc_invoice_99",
        risk_score=0.45,
        confidence_score=0.92,
        business_impact="MEDIUM",
        financial_impact=15000.0,
    )
    assert ctx.tenant_id == "tenant_123"
    assert ctx.risk_score == 0.45
    assert ctx.confidence_score == 0.92
    assert ctx.business_impact == "MEDIUM"
    assert ctx.data_classification == "INTERNAL"
    assert ctx.request_id.startswith("req_")
    assert ctx.decision_id.startswith("dec_")


def test_human_decision_recording():
    decision = HumanDecision(
        review_id="rev_abc123",
        tenant_id="tenant_123",
        reviewer_id="usr_reviewer_1",
        reviewer_role="compliance_officer",
        outcome=DecisionOutcome.APPROVED,
        reason="Verified invoice total and supplier VAT number against ERP.",
        feedback=FeedbackAssessment.AI_CORRECT,
        evidence_viewed=["evd_1", "evd_2"],
    )
    assert decision.outcome == DecisionOutcome.APPROVED
    assert decision.feedback == FeedbackAssessment.AI_CORRECT
    assert decision.reviewer_id == "usr_reviewer_1"
    assert len(decision.evidence_viewed) == 2


def test_oversight_exceptions_hierarchy():
    with pytest.raises(OversightException):
        raise UnauthorizedReviewerError("Reviewer not authorized")

    with pytest.raises(OversightException):
        raise InvalidOverrideError("Invalid override")

    with pytest.raises(OversightException):
        raise EscalationTimeoutError("Escalation timeout")

    with pytest.raises(OversightException):
        raise ApprovalPolicyViolationError("Policy violation")
