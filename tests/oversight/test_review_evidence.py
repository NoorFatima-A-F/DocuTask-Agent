"""Tests for Review Requests, Evidence Packages, and Deliberation Comments."""

import pytest
from app.oversight.reviews.requests import ReviewRequest, ReviewPriority
from app.oversight.reviews.evidence import ReviewEvidencePackage, SourceCitation
from app.oversight.reviews.comments import ReviewComment
from app.oversight.approvals.lifecycle import ApprovalLifecycleState


def test_review_request_creation():
    req = ReviewRequest(
        request_id="req_test_01",
        tenant_id="tenant_x",
        title="High Risk Invoice Payment Review",
        resource_id="inv_9001",
        action_type="PAYMENT_DISPATCH",
        priority=ReviewPriority.HIGH,
        required_roles=["finance_manager"],
    )
    assert req.review_id.startswith("rev_")
    assert req.status == ApprovalLifecycleState.PENDING_REVIEW
    assert req.priority == ReviewPriority.HIGH
    assert "finance_manager" in req.required_roles


def test_review_evidence_package():
    citations = [
        SourceCitation(
            source_id="doc_p1",
            document_name="master_contract.pdf",
            snippet="Supplier agrees to net-30 terms at 15% discount.",
            confidence=0.98,
        )
    ]
    pkg = ReviewEvidencePackage(
        review_id="rev_test_01",
        tenant_id="tenant_x",
        action_type="PAYMENT_DISPATCH",
        proposed_output={"amount": 45000.0, "vendor": "Acme Corp"},
        explanation="Payment exceeds automated threshold; verified vendor agreement.",
        risk_score=0.65,
        confidence_score=0.95,
        grounding_score=0.94,
        model_id="gemini-1.5-pro",
        prompt_id="prompt_invoice_v2",
        citations=citations,
        triggered_policies=["High Value Financial Transaction"],
        safety_checks_passed=["PII_MASKED", "PROMPT_INJECTION_CLEAR"],
    )
    assert pkg.package_id.startswith("evd_")
    assert len(pkg.citations) == 1
    assert pkg.citations[0].document_name == "master_contract.pdf"
    assert pkg.model_id == "gemini-1.5-pro"
    assert len(pkg.triggered_policies) == 1


def test_review_comment_deliberation():
    comment = ReviewComment(
        review_id="rev_test_01",
        tenant_id="tenant_x",
        author_id="usr_alice",
        author_name="Alice Smith",
        author_role="compliance_officer",
        text="Checked vendor bank details against ERP vendor master. Matches.",
        is_internal=True,
    )
    assert comment.comment_id.startswith("cmt_")
    assert comment.is_internal is True
    assert comment.author_name == "Alice Smith"
