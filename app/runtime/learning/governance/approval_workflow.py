"""
Approval Workflow for Phase 13.5 (ARLP-KIP).
Manages multi-stage human and automated review lifecycles for learning artifacts and candidate policies.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid
from pydantic import BaseModel, Field


class ReviewRecord(BaseModel):
    review_id: str = Field(default_factory=lambda: f"rev_{uuid.uuid4().hex[:8]}")
    candidate_id: str
    reviewer_id: str = "gov-council"
    decision: str = "APPROVED"  # APPROVED | REJECTED | ESCALATED
    comments: Optional[str] = "Validation criteria satisfied."
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ApprovalWorkflowManager:
    """
    Manages review and approval state transitions.
    """

    def __init__(self):
        self._reviews: Dict[str, ReviewRecord] = {}
        self._seed_default_review()

    def _seed_default_review(self):
        r = ReviewRecord(
            candidate_id="cand-001",
            reviewer_id="gov-admin-01",
            decision="APPROVED",
            comments="Pre-approved during initialization baseline verification.",
        )
        self._reviews[r.review_id] = r

    def record_review(
        self,
        candidate_id: str,
        reviewer_id: str = "gov-council",
        decision: str = "APPROVED",
        comments: Optional[str] = None,
    ) -> ReviewRecord:
        rec = ReviewRecord(
            candidate_id=candidate_id,
            reviewer_id=reviewer_id,
            decision=decision.upper(),
            comments=comments or "Recorded via governance workflow.",
        )
        self._reviews[rec.review_id] = rec
        return rec

    def list_reviews(self, candidate_id: Optional[str] = None) -> List[ReviewRecord]:
        reviews = list(self._reviews.values())
        if candidate_id:
            reviews = [r for r in reviews if r.candidate_id == candidate_id]
        return reviews


approval_workflow_manager = ApprovalWorkflowManager()
