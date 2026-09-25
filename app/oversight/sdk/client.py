"""Human Oversight Developer SDK Client."""

from typing import Dict, Any, List, Optional, Tuple

from ..core.context import OversightContext
from ..core.decisions import HumanDecision, DecisionOutcome, FeedbackAssessment
from ..core.engine import HumanOversightEngine
from ..approvals.models import ApprovalChain
from ..approvals.policies import ApprovalPolicy
from ..reviews.requests import ReviewRequest, ReviewPriority
from ..reviews.evidence import ReviewEvidencePackage
from ..overrides.service import HumanOverrideRecord
from ..analytics.metrics import OversightAnalyticsSummary


class OversightSDK:
    """Developer SDK client for evaluating human oversight policies, creating reviews, and tracking decisions."""

    def __init__(self, engine: Optional[HumanOversightEngine] = None):
        self.engine = engine or HumanOversightEngine()

    def evaluate_decision(self, context: OversightContext) -> Tuple[bool, Optional[ApprovalPolicy], str]:
        """Evaluates whether an action requires human review."""
        return self.engine.evaluate_context(context)

    def request_review(
        self,
        context: OversightContext,
        evidence: Optional[ReviewEvidencePackage] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: ReviewPriority = ReviewPriority.MEDIUM,
    ) -> Tuple[ReviewRequest, ApprovalChain]:
        """Submits a human review request."""
        return self.engine.create_review_request(
            context=context,
            evidence=evidence,
            title=title,
            description=description,
            priority=priority,
        )

    def submit_decision(
        self,
        review_id: str,
        reviewer_id: str,
        outcome: DecisionOutcome,
        reason: str,
        reviewer_role: Optional[str] = None,
        feedback: Optional[FeedbackAssessment] = None,
        modified_parameters: Optional[Dict[str, Any]] = None,
        context: Optional[OversightContext] = None,
    ) -> HumanDecision:
        """Records a human review outcome."""
        return self.engine.submit_decision(
            review_id=review_id,
            reviewer_id=reviewer_id,
            outcome=outcome,
            reason=reason,
            reviewer_role=reviewer_role,
            feedback=feedback,
            modified_parameters=modified_parameters,
            context=context,
        )

    def override_decision(
        self,
        review_id: str,
        reviewer_id: str,
        reviewer_role: str,
        original_ai_decision: Any,
        overridden_human_decision: Any,
        justification: str,
        context: OversightContext,
    ) -> HumanOverrideRecord:
        """Executes a controlled human override."""
        return self.engine.execute_override(
            review_id=review_id,
            reviewer_id=reviewer_id,
            reviewer_role=reviewer_role,
            original_ai_decision=original_ai_decision,
            overridden_human_decision=overridden_human_decision,
            justification=justification,
            context=context,
        )

    def get_review(self, review_id: str) -> Optional[ReviewRequest]:
        return self.engine.get_review_request(review_id)

    def list_reviews(
        self, tenant_id: Optional[str] = None, status: Optional[str] = None
    ) -> List[ReviewRequest]:
        return self.engine.list_review_requests(tenant_id=tenant_id)

    def get_evidence(self, review_id: str) -> Optional[ReviewEvidencePackage]:
        return self.engine.get_evidence(review_id)

    def get_analytics(self, tenant_id: str = "*") -> OversightAnalyticsSummary:
        return self.engine.get_analytics(tenant_id)
