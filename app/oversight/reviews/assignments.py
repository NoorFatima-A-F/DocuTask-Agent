"""Reviewer Assignment Engine, Roles, and Delegation Authorities."""

from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field
from datetime import datetime, timezone

from ..core.exceptions import UnauthorizedReviewerError
from ..core.context import OversightContext
from .requests import ReviewRequest


class ReviewerAuthority(BaseModel):
    """Authority matrix determining what a reviewer is permitted to approve or override."""
    max_financial_limit: float = 10000.0
    authorized_risk_levels: List[str] = Field(default_factory=lambda: ["LOW", "MEDIUM"])
    authorized_roles: List[str] = Field(default_factory=lambda: ["reviewer"])
    authorized_data_classifications: List[str] = Field(default_factory=lambda: ["PUBLIC", "INTERNAL"])
    can_override: bool = False
    can_delegate: bool = True


class Reviewer(BaseModel):
    """Reviewer profile with skillset, department, and active queue telemetry."""
    user_id: str
    name: str
    email: str
    department: str
    roles: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    authority: ReviewerAuthority = Field(default_factory=ReviewerAuthority)
    is_active: bool = True
    active_reviews_count: int = 0
    max_concurrency: int = 10


class ReviewerAssignmentEngine:
    """Smart routing and load balancing for human review requests."""

    def __init__(self, reviewers: Optional[List[Reviewer]] = None):
        self._reviewers: Dict[str, Reviewer] = {}
        if reviewers:
            for r in reviewers:
                self._reviewers[r.user_id] = r

    def register_reviewer(self, reviewer: Reviewer) -> Reviewer:
        self._reviewers[reviewer.user_id] = reviewer
        return reviewer

    def get_reviewer(self, user_id: str) -> Optional[Reviewer]:
        return self._reviewers.get(user_id)

    def list_reviewers(self) -> List[Reviewer]:
        return list(self._reviewers.values())

    def verify_authority(self, reviewer: Reviewer, context: OversightContext) -> Tuple[bool, str]:
        """Verifies if the reviewer has sufficient authority for the context."""
        # 1. Financial check
        if context.financial_impact > reviewer.authority.max_financial_limit:
            return (
                False,
                f"Financial impact (${context.financial_impact:.2f}) exceeds reviewer limit (${reviewer.authority.max_financial_limit:.2f})",
            )

        # 2. Data classification check
        if context.data_classification not in reviewer.authority.authorized_data_classifications:
            return (
                False,
                f"Data classification '{context.data_classification}' not in authorized list {reviewer.authority.authorized_data_classifications}",
            )

        # 3. Risk level check
        impact_level = context.business_impact.upper()
        if impact_level not in reviewer.authority.authorized_risk_levels and "CRITICAL" not in reviewer.authority.authorized_risk_levels:
            if context.risk_score > 0.8 and "HIGH" not in reviewer.authority.authorized_risk_levels:
                return (
                    False,
                    f"Risk score ({context.risk_score:.2f}) exceeds reviewer authorized risk scope",
                )

        return True, "Authority verified"

    def find_eligible_reviewers(
        self,
        required_roles: List[str],
        context: Optional[OversightContext] = None,
        department: Optional[str] = None,
        required_skills: Optional[List[str]] = None,
    ) -> List[Reviewer]:
        """Filters active reviewers matching roles, skills, department, and authority."""
        eligible = []
        for r in self._reviewers.values():
            if not r.is_active:
                continue
            if r.active_reviews_count >= r.max_concurrency:
                continue
            if department and r.department != department:
                continue
            if required_roles and not any(role in r.roles for role in required_roles):
                continue
            if required_skills and not all(s in r.skills for s in required_skills):
                continue
            if context:
                authorized, _ = self.verify_authority(r, context)
                if not authorized:
                    continue
            eligible.append(r)
        return eligible

    def assign_reviewer(
        self,
        request: ReviewRequest,
        context: Optional[OversightContext] = None,
        strategy: str = "LEAST_BUSY",
    ) -> Optional[Reviewer]:
        """Assigns the best reviewer using load balancing / least-busy strategy."""
        eligible = self.find_eligible_reviewers(
            required_roles=request.required_roles,
            context=context,
        )
        if not eligible:
            return None

        if strategy == "LEAST_BUSY":
            selected = min(eligible, key=lambda r: r.active_reviews_count)
        else:
            selected = eligible[0]

        selected.active_reviews_count += 1
        request.assigned_reviewers.append(selected.user_id)
        request.assigned_at = datetime.now(timezone.utc)
        return selected

    def release_reviewer(self, user_id: str) -> None:
        """Decrements the active review count when a review is resolved or cancelled."""
        if user_id in self._reviewers:
            self._reviewers[user_id].active_reviews_count = max(
                0, self._reviewers[user_id].active_reviews_count - 1
            )
