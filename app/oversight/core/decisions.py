"""Human Decision Models & Feedback Assessment Classifications."""

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


class DecisionOutcome(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"
    MODIFIED = "MODIFIED"
    DELEGATED = "DELEGATED"
    CANCELLED = "CANCELLED"


class FeedbackAssessment(str, Enum):
    AI_CORRECT = "AI_CORRECT"
    AI_INCORRECT = "AI_INCORRECT"
    AI_UNSAFE = "AI_UNSAFE"
    MISSING_INFORMATION = "MISSING_INFORMATION"
    WRONG_SOURCE = "WRONG_SOURCE"
    WRONG_ACTION = "WRONG_ACTION"


class HumanDecision(BaseModel):
    """Permanent recorded human decision with full accountability and feedback loop."""
    decision_id: str = Field(default_factory=lambda: f"hdec_{uuid.uuid4().hex[:10]}")
    review_id: str
    tenant_id: str
    reviewer_id: str
    reviewer_role: str
    outcome: DecisionOutcome
    reason: str
    feedback: Optional[FeedbackAssessment] = None
    modified_parameters: Optional[Dict[str, Any]] = None
    evidence_viewed: List[str] = Field(default_factory=list)
    policy_context: Optional[Dict[str, Any]] = None
    decided_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
