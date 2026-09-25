"""Review Request Models and Priority Levels."""

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid

from ..approvals.lifecycle import ApprovalLifecycleState


class ReviewPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    URGENT = "URGENT"
    CRITICAL = "CRITICAL"


class ReviewRequest(BaseModel):
    """Encapsulates an active human oversight review item."""
    review_id: str = Field(default_factory=lambda: f"rev_{uuid.uuid4().hex[:10]}")
    request_id: str
    tenant_id: str
    title: str
    description: Optional[str] = None
    
    # State & Priority
    status: ApprovalLifecycleState = ApprovalLifecycleState.PENDING_REVIEW
    priority: ReviewPriority = ReviewPriority.MEDIUM
    
    # Targets & Context
    resource_type: str = "WORKFLOW"
    resource_id: str
    action_type: str = "EXECUTE"
    chain_id: Optional[str] = None
    
    # Reviewer Routing
    required_roles: List[str] = Field(default_factory=list)
    assigned_reviewers: List[str] = Field(default_factory=list)
    
    # SLA & Timing
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    assigned_at: Optional[datetime] = None
    deadline: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    
    # Decision References
    decision_id: Optional[str] = None
    escalation_level: int = 0
    
    metadata: Dict[str, Any] = Field(default_factory=dict)
