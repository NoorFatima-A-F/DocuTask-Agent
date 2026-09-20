"""Release Approvals, Multi-Stakeholder Gates, and Policy Verification."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import threading


class ApprovalDecision(str, Enum):
    """Release approval decision."""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class ReleaseApproval:
    """An individual stakeholder approval sign-off."""
    approver: str
    role: str  # governance, security, sre, qa, lead
    decision: ApprovalDecision = ApprovalDecision.PENDING
    comments: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ReleaseApprovalGate:
    """Manages required stakeholder sign-offs before a release can be deployed to production."""

    REQUIRED_ROLES = ["governance", "security", "sre"]

    def __init__(self) -> None:
        self._approvals: Dict[str, List[ReleaseApproval]] = {}  # release_id -> [ReleaseApproval]
        self._lock = threading.RLock()

    def record_decision(self, release_id: str, approver: str, role: str, decision: ApprovalDecision, comments: Optional[str] = None) -> ReleaseApproval:
        """Record an approval or rejection decision."""
        with self._lock:
            app = ReleaseApproval(
                approver=approver,
                role=role.lower(),
                decision=decision,
                comments=comments,
            )
            self._approvals.setdefault(release_id, []).append(app)
            return app

    def is_release_approved(self, release_id: str) -> bool:
        """Check if all mandatory roles approved and none rejected."""
        with self._lock:
            apps = self._approvals.get(release_id, [])
            if any(a.decision == ApprovalDecision.REJECTED for a in apps):
                return False

            approved_roles = set(a.role for a in apps if a.decision == ApprovalDecision.APPROVED)
            return all(req in approved_roles for req in self.REQUIRED_ROLES)

    def get_approvals(self, release_id: str) -> List[ReleaseApproval]:
        """Fetch all approvals for a release."""
        with self._lock:
            return list(self._approvals.get(release_id, []))
