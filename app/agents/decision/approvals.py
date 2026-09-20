"""
Approval Requirements & Workflows.
Defines ApprovalRequirement, EscalationRequirement, and ApprovalWorkflow.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ApprovalRequirement(BaseModel):
    """Specification of required human or supervisor approval."""

    requires_approval: bool = Field(default=False)
    reason: Optional[str] = Field(default=None)
    approver_role: str = Field(default="ADMIN")
    escalation_timeout_seconds: float = Field(default=3600.0, gt=0.0)
    model_config = {"frozen": True}


class EscalationRequirement(BaseModel):
    """Specification of required system or management escalation."""

    requires_escalation: bool = Field(default=False)
    escalation_tier: str = Field(default="SECURITY_OFFICER")
    reason: Optional[str] = Field(default=None)
    model_config = {"frozen": True}


class ApprovalWorkflow(BaseModel):
    """Multi-step approval chain definition."""

    workflow_id: str
    required_approvals: List[ApprovalRequirement] = Field(default_factory=list)
    escalations: List[EscalationRequirement] = Field(default_factory=list)
    model_config = {"frozen": True}
