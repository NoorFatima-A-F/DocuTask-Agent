"""FastAPI Request and Response Schemas for Human Oversight API."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from ..core.context import OversightContext
from ..core.decisions import DecisionOutcome, FeedbackAssessment, HumanDecision
from ..approvals.models import ApprovalPolicyType, ApprovalStrategy, ApprovalChain
from ..approvals.lifecycle import ApprovalLifecycleState
from ..approvals.policies import ApprovalPolicy
from ..reviews.requests import ReviewRequest, ReviewPriority
from ..reviews.evidence import ReviewEvidencePackage
from ..reviews.comments import ReviewComment
from ..reviews.assignments import Reviewer
from ..overrides.service import HumanOverrideRecord
from ..analytics.metrics import OversightAnalyticsSummary


class EvaluateContextRequest(BaseModel):
    context: OversightContext


class EvaluateContextResponse(BaseModel):
    requires_approval: bool
    policy: Optional[ApprovalPolicy] = None
    reason: str


class CreateReviewRequestPayload(BaseModel):
    context: OversightContext
    evidence: Optional[ReviewEvidencePackage] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: ReviewPriority = ReviewPriority.MEDIUM


class SubmitDecisionPayload(BaseModel):
    reviewer_id: str
    reviewer_role: Optional[str] = None
    outcome: DecisionOutcome
    reason: str
    feedback: Optional[FeedbackAssessment] = None
    modified_parameters: Optional[Dict[str, Any]] = None
    context: Optional[OversightContext] = None


class OverridePayload(BaseModel):
    reviewer_id: str
    reviewer_role: str
    original_ai_decision: Any
    overridden_human_decision: Any
    justification: str
    context: OversightContext


class AddCommentPayload(BaseModel):
    author_id: str
    author_name: str
    author_role: str
    text: str
    is_internal: bool = False
