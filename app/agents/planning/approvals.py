"""
Planning Approval Gate Models.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class PlanApprovalGate(BaseModel):
    """Approval gate blocking plan execution until authorized."""
    gate_id: str
    node_id: str
    approver_roles: List[str] = Field(default_factory=lambda: ["ADMIN"])
    is_approved: bool = Field(default=False)
    approval_reason: Optional[str] = Field(default=None)
    model_config = {"frozen": True}
