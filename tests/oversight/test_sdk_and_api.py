"""Tests for Developer SDK, @require_oversight decorator, and FastAPI routes."""

import pytest
from app.oversight.core.context import OversightContext
from app.oversight.core.engine import HumanOversightEngine
from app.oversight.core.decisions import DecisionOutcome, FeedbackAssessment
from app.oversight.core.exceptions import ApprovalPolicyViolationError
from app.oversight.reviews.evidence import ReviewEvidencePackage
from app.oversight.reviews.assignments import Reviewer, ReviewerAuthority
from app.oversight.sdk.client import OversightSDK
from app.oversight.sdk.decorators import require_oversight
from app.oversight.api.routes import (
    evaluate_context,
    create_review_request,
    list_reviews,
    get_review,
    get_review_evidence,
    submit_decision,
    execute_override,
    add_comment,
    list_comments,
    get_analytics,
    register_reviewer,
    list_reviewers,
)
from app.oversight.api.schemas import (
    EvaluateContextRequest,
    CreateReviewRequestPayload,
    SubmitDecisionPayload,
    OverridePayload,
    AddCommentPayload,
)


def test_oversight_sdk_flow():
    engine = HumanOversightEngine()
    sdk = OversightSDK(engine)

    # Register reviewers
    reviewer1 = Reviewer(
        user_id="usr_compliance",
        name="Compliance Officer",
        email="comp@example.com",
        department="Audit",
        roles=["compliance_officer"],
        authority=ReviewerAuthority(max_financial_limit=100000.0, authorized_risk_levels=["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
    )
    reviewer2 = Reviewer(
        user_id="usr_secops",
        name="SecOps Lead",
        email="secops@example.com",
        department="Security",
        roles=["secops_lead"],
        authority=ReviewerAuthority(max_financial_limit=100000.0, authorized_risk_levels=["LOW", "MEDIUM", "HIGH", "CRITICAL"]),
    )
    engine.assignment_engine.register_reviewer(reviewer1)
    engine.assignment_engine.register_reviewer(reviewer2)

    # Evaluate context (high risk -> triggers 2-tier approval policy)
    ctx = OversightContext(
        tenant_id="tenant_sdk",
        risk_score=0.88,
        financial_impact=5000.0,
    )
    req_eval, pol, _ = sdk.evaluate_decision(ctx)
    assert req_eval is True
    assert pol is not None

    # Request review with evidence
    evidence = ReviewEvidencePackage(
        review_id="",
        tenant_id="tenant_sdk",
        action_type="HIGH_RISK_EXECUTION",
        proposed_output={"status": "INITIATED"},
        risk_score=0.88,
    )
    review, chain = sdk.request_review(context=ctx, evidence=evidence)
    assert review.review_id.startswith("rev_")

    # Tier 1 Approval (Compliance Officer)
    d1 = sdk.submit_decision(
        review_id=review.review_id,
        reviewer_id="usr_compliance",
        reviewer_role="compliance_officer",
        outcome=DecisionOutcome.APPROVED,
        reason="Tier 1 compliance verified.",
        feedback=FeedbackAssessment.AI_CORRECT,
        context=ctx,
    )
    assert d1.outcome == DecisionOutcome.APPROVED

    # Check intermediate state is IN_REVIEW (waiting for Tier 2)
    in_review_state = sdk.get_review(review.review_id)
    assert in_review_state.status.value == "IN_REVIEW"

    # Tier 2 Approval (SecOps Lead)
    d2 = sdk.submit_decision(
        review_id=review.review_id,
        reviewer_id="usr_secops",
        reviewer_role="secops_lead",
        outcome=DecisionOutcome.APPROVED,
        reason="Tier 2 secops verified.",
        feedback=FeedbackAssessment.AI_CORRECT,
        context=ctx,
    )
    assert d2.outcome == DecisionOutcome.APPROVED

    # Check final review status is APPROVED
    final_rev = sdk.get_review(review.review_id)
    assert final_rev.status.value == "APPROVED"

    # Check evidence retrieval
    evd = sdk.get_evidence(review.review_id)
    assert evd is not None
    assert evd.risk_score == 0.88

    # Check analytics
    summary = sdk.get_analytics("tenant_sdk")
    assert summary.total_reviews == 1
    assert summary.approved_count == 2


def test_require_oversight_decorator():
    engine = HumanOversightEngine()

    @require_oversight(action_type="DEPLOY", tenant_id="tenant_dec", engine=engine)
    def sensitive_action(oversight_context: OversightContext):
        return "SUCCESS_EXECUTED"

    # Context with low risk -> executes normally
    safe_ctx = OversightContext(
        tenant_id="tenant_dec",
        risk_score=0.10,
        confidence_score=0.99,
    )
    res = sensitive_action(oversight_context=safe_ctx)
    assert res == "SUCCESS_EXECUTED"

    # Context with high risk -> triggers policy violation and halts execution
    risky_ctx = OversightContext(
        tenant_id="tenant_dec",
        risk_score=0.90,
    )
    with pytest.raises(ApprovalPolicyViolationError) as exc_info:
        sensitive_action(oversight_context=risky_ctx)
    assert "Execution halted by Human Oversight Policy" in str(exc_info.value)


@pytest.mark.anyio
async def test_fastapi_oversight_endpoints():
    engine = HumanOversightEngine()

    # 1. Register reviewer
    rev_profile = Reviewer(
        user_id="api_user_1",
        name="API Reviewer",
        email="reviewer@api.com",
        department="Operations",
        roles=["reviewer", "operator"],
        skills=["general_review"],
        authority=ReviewerAuthority(
            max_financial_limit=50000.0,
            authorized_risk_levels=["LOW", "MEDIUM", "HIGH", "CRITICAL"],
            authorized_roles=["reviewer", "operator"],
            authorized_data_classifications=["PUBLIC", "INTERNAL"],
            can_override=True,
            can_delegate=True,
        ),
        is_active=True,
        active_reviews_count=0,
        max_concurrency=10,
    )
    registered = await register_reviewer(rev_profile, engine=engine)
    assert registered.user_id == "api_user_1"

    all_reviewers = await list_reviewers(engine=engine)
    assert len(all_reviewers) == 1

    # 2. Evaluate context (low confidence triggers 1-tier review)
    ctx = OversightContext(
        tenant_id="tenant_api",
        confidence_score=0.75,
        action_type="CLASSIFY_DOCUMENT",
    )
    eval_resp = await evaluate_context(EvaluateContextRequest(context=ctx), engine=engine)
    assert eval_resp.requires_approval is True

    # 3. Create review request
    evidence = ReviewEvidencePackage(
        review_id="",
        tenant_id="tenant_api",
        action_type="CLASSIFY_DOCUMENT",
        proposed_output={"data": "test"},
        confidence_score=0.75,
    )
    create_payload = CreateReviewRequestPayload(
        context=ctx,
        evidence=evidence,
        title="API Extraction Review",
    )
    created_review = await create_review_request(create_payload, engine=engine)
    assert created_review.review_id.startswith("rev_")
    review_id = created_review.review_id

    # 4. Get evidence
    evd_resp = await get_review_evidence(review_id, engine=engine)
    assert evd_resp.confidence_score == 0.75

    # 5. Add comment
    cmt_payload = AddCommentPayload(
        author_id="api_user_1",
        author_name="API Reviewer",
        author_role="reviewer",
        text="Initial inspection complete.",
    )
    cmt = await add_comment(review_id, cmt_payload, engine=engine)
    assert cmt.text == "Initial inspection complete."

    cmts = await list_comments(review_id, engine=engine)
    assert len(cmts) == 1

    # 6. Submit decision
    dec_payload = SubmitDecisionPayload(
        reviewer_id="api_user_1",
        reviewer_role="reviewer",
        outcome=DecisionOutcome.APPROVED,
        reason="Approved through automated API test.",
        feedback=FeedbackAssessment.AI_CORRECT,
    )
    dec = await submit_decision(review_id, dec_payload, engine=engine)
    assert dec.outcome == DecisionOutcome.APPROVED

    # 7. Check analytics
    analytics = await get_analytics(tenant_id="tenant_api", engine=engine)
    assert analytics.total_reviews == 1
    assert analytics.approved_count == 1
