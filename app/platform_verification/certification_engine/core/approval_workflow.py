"""
Approval Workflow Manager for human governance and multi-stakeholder reviews.
"""
from __future__ import annotations
from typing import Dict, List, Optional
from app.platform_verification.certification_engine.domain.interfaces import IApprovalWorkflowManager
from app.platform_verification.certification_engine.domain.models import (
    ApprovalAction,
    ApprovalReview,
)


class EnterpriseApprovalWorkflow(IApprovalWorkflowManager):
    """Manages role-based governance reviews and multi-signature approvals."""

    def __init__(self):
        self._reviews: Dict[str, List[ApprovalReview]] = {}  # cert_id -> list of reviews

    def submit_review(self, review: ApprovalReview) -> bool:
        if review.certification_id not in self._reviews:
            self._reviews[review.certification_id] = []
        self._reviews[review.certification_id].append(review)
        return True

    def get_reviews_for_certification(self, certification_id: str) -> List[ApprovalReview]:
        return self._reviews.get(certification_id, [])

    def is_fully_approved(self, certification_id: str, required_roles: Optional[List[str]] = None) -> bool:
        roles = required_roles or ["ReleaseArchitect", "SecurityLead"]
        reviews = self.get_reviews_for_certification(certification_id)
        approved_roles = {
            r.reviewer_role for r in reviews if r.action == ApprovalAction.APPROVE
        }
        return all(req in approved_roles for req in roles)
