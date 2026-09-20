"""FastAPI REST API Routes for Enterprise Human Oversight Platform."""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends

from ..core.engine import HumanOversightEngine
from ..core.exceptions import OversightException, UnauthorizedReviewerError, InvalidOverrideError
from ..approvals.policies import ApprovalPolicy
from ..reviews.requests import ReviewRequest
from ..reviews.evidence import ReviewEvidencePackage
from ..reviews.comments import ReviewComment
from ..reviews.assignments import Reviewer
from ..core.decisions import HumanDecision
from ..overrides.service import HumanOverrideRecord
from ..analytics.metrics import OversightAnalyticsSummary

from .schemas import (
    EvaluateContextRequest,
    EvaluateContextResponse,
    CreateReviewRequestPayload,
    SubmitDecisionPayload,
    OverridePayload,
    AddCommentPayload,
)

router = APIRouter(prefix="/api/v1/oversight", tags=["Human Oversight & Approvals"])

# Singleton engine instance for API layer
_engine: Optional[HumanOversightEngine] = None


def get_engine() -> HumanOversightEngine:
    global _engine
    if _engine is None:
        _engine = HumanOversightEngine()
    return _engine


@router.post("/evaluate", response_model=EvaluateContextResponse)
async def evaluate_context(
    payload: EvaluateContextRequest,
    engine: HumanOversightEngine = Depends(get_engine),
):
    """Evaluates context against oversight policies."""
    requires_approval, policy, reason = engine.evaluate_context(payload.context)
    return EvaluateContextResponse(
        requires_approval=requires_approval,
        policy=policy,
        reason=reason,
    )


@router.post("/reviews", response_model=ReviewRequest, status_code=status.HTTP_201_CREATED)
async def create_review_request(
    payload: CreateReviewRequestPayload,
    engine: HumanOversightEngine = Depends(get_engine),
):
    """Creates a new human review request."""
    review, _ = engine.create_review_request(
        context=payload.context,
        evidence=payload.evidence,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
    )
    return review


@router.get("/reviews", response_model=List[ReviewRequest])
async def list_reviews(
    tenant_id: Optional[str] = None,
    status: Optional[str] = None,
    reviewer_id: Optional[str] = None,
    engine: HumanOversightEngine = Depends(get_engine),
):
    """Lists reviews matching filters."""
    return engine.list_review_requests(
        tenant_id=tenant_id,
        reviewer_id=reviewer_id,
    )


@router.get("/reviews/{review_id}", response_model=ReviewRequest)
async def get_review(
    review_id: str,
    engine: HumanOversightEngine = Depends(get_engine),
):
    """Gets details of a specific review."""
    review = engine.get_review_request(review_id)
    if not review:
        raise HTTPException(status_code=404, detail=f"Review '{review_id}' not found")
    return review


@router.get("/reviews/{review_id}/evidence", response_model=ReviewEvidencePackage)
async def get_review_evidence(
    review_id: str,
    engine: HumanOversightEngine = Depends(get_engine),
):
    """Retrieves full contextual evidence package for a review."""
    evidence = engine.get_evidence(review_id)
    if not evidence:
        raise HTTPException(status_code=404, detail=f"Evidence for review '{review_id}' not found")
    return evidence


@router.post("/reviews/{review_id}/decisions", response_model=HumanDecision)
async def submit_decision(
    review_id: str,
    payload: SubmitDecisionPayload,
    engine: HumanOversightEngine = Depends(get_engine),
):
    """Submits a human decision (APPROVE / REJECT / ESCALATE)."""
    try:
        decision = engine.submit_decision(
            review_id=review_id,
            reviewer_id=payload.reviewer_id,
            outcome=payload.outcome,
            reason=payload.reason,
            reviewer_role=payload.reviewer_role,
            feedback=payload.feedback,
            modified_parameters=payload.modified_parameters,
            context=payload.context,
        )
        return decision
    except UnauthorizedReviewerError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except OversightException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reviews/{review_id}/override", response_model=HumanOverrideRecord)
async def execute_override(
    review_id: str,
    payload: OverridePayload,
    engine: HumanOversightEngine = Depends(get_engine),
):
    """Executes a controlled human override."""
    try:
        record = engine.execute_override(
            review_id=review_id,
            reviewer_id=payload.reviewer_id,
            reviewer_role=payload.reviewer_role,
            original_ai_decision=payload.original_ai_decision,
            overridden_human_decision=payload.overridden_human_decision,
            justification=payload.justification,
            context=payload.context,
        )
        return record
    except InvalidOverrideError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except OversightException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/reviews/{review_id}/comments", response_model=ReviewComment)
async def add_comment(
    review_id: str,
    payload: AddCommentPayload,
    engine: HumanOversightEngine = Depends(get_engine),
):
    """Adds a deliberation comment to a review request."""
    try:
        return engine.add_comment(
            review_id=review_id,
            author_id=payload.author_id,
            author_name=payload.author_name,
            author_role=payload.author_role,
            text=payload.text,
            is_internal=payload.is_internal,
        )
    except OversightException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/reviews/{review_id}/comments", response_model=List[ReviewComment])
async def list_comments(
    review_id: str,
    engine: HumanOversightEngine = Depends(get_engine),
):
    """Lists deliberation comments for a review."""
    return engine.get_comments(review_id)


@router.get("/analytics", response_model=OversightAnalyticsSummary)
async def get_analytics(
    tenant_id: str = "*",
    engine: HumanOversightEngine = Depends(get_engine),
):
    """Returns governance telemetry and review analytics."""
    return engine.get_analytics(tenant_id=tenant_id)


@router.post("/reviewers", response_model=Reviewer, status_code=status.HTTP_201_CREATED)
async def register_reviewer(
    reviewer: Reviewer,
    engine: HumanOversightEngine = Depends(get_engine),
):
    """Registers or updates a reviewer profile."""
    return engine.assignment_engine.register_reviewer(reviewer)


@router.get("/reviewers", response_model=List[Reviewer])
async def list_reviewers(
    engine: HumanOversightEngine = Depends(get_engine),
):
    """Lists all active reviewer profiles."""
    return engine.assignment_engine.list_reviewers()
