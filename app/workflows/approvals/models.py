"""
Human Task and Approval Domain Models.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class ApprovalType(str, Enum):
    SINGLE = "SINGLE"
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"
    MAJORITY_VOTE = "MAJORITY_VOTE"
    ROLE_BASED = "ROLE_BASED"
    CONDITIONAL = "CONDITIONAL"


class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    DELEGATED = "DELEGATED"
    EXPIRED = "EXPIRED"


@dataclass
class ApprovalVote:
    approver: str
    decision: ApprovalStatus
    comment: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ApprovalRequest:
    """Human-in-the-loop approval request."""
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    execution_id: str = ""
    task_id: str = ""
    approval_type: ApprovalType = ApprovalType.SINGLE
    required_role: str = "manager"
    assigned_to: Optional[str] = None
    status: ApprovalStatus = ApprovalStatus.PENDING
    votes: List[ApprovalVote] = field(default_factory=list)
    min_approvals: int = 1
    deadline: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "execution_id": self.execution_id,
            "task_id": self.task_id,
            "approval_type": self.approval_type.value,
            "required_role": self.required_role,
            "assigned_to": self.assigned_to,
            "status": self.status.value,
            "votes": [{"approver": v.approver, "decision": v.decision.value, "comment": v.comment} for v in self.votes],
            "created_at": self.created_at.isoformat(),
        }
