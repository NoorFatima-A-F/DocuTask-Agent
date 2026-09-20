"""
Human Task Model.
Represents an asynchronous human review or approval checkpoint requiring human intervention.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class HumanTaskStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"
    TIMED_OUT = "TIMED_OUT"


class HumanTaskDecision(str, Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    ESCALATE = "ESCALATE"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"



class HumanTask(BaseModel):
    """Interactive human approval / review request."""
    task_id: UUID = Field(default_factory=uuid4)
    workflow_instance_id: UUID
    title: str
    description: str
    assigned_user_or_role: str
    status: HumanTaskStatus = HumanTaskStatus.PENDING
    decision_reason: Optional[str] = None
    decided_by: Optional[str] = None
    timeout_seconds: float = Field(default=86400.0, gt=0.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def approve(self, user_id: str, reason: str = "") -> "HumanTask":
        return self.model_copy(update={
            "status": HumanTaskStatus.APPROVED,
            "decided_by": user_id,
            "decision_reason": reason
        })

    def reject(self, user_id: str, reason: str = "") -> "HumanTask":
        return self.model_copy(update={
            "status": HumanTaskStatus.REJECTED,
            "decided_by": user_id,
            "decision_reason": reason
        })

    def escalate(self, escalated_to: str) -> "HumanTask":
        return self.model_copy(update={
            "status": HumanTaskStatus.ESCALATED,
            "assigned_user_or_role": escalated_to
        })
