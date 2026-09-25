"""Human Override Policies and Safety Boundary Constraints."""

from typing import List
from pydantic import BaseModel, Field
import uuid


class OverridePolicy(BaseModel):
    """Governs when and under what constraints a human can override an AI decision or safety gate."""
    policy_id: str = Field(default_factory=lambda: f"ovr_pol_{uuid.uuid4().hex[:8]}")
    tenant_id: str = "*"
    name: str
    allowed_roles: List[str] = Field(default_factory=lambda: ["admin", "compliance_officer", "supervisor"])
    min_justification_length: int = 15
    require_dual_signoff: bool = False
    max_risk_score_overrideable: float = 0.95  # Severe risk (>0.95) cannot be overridden
    prohibited_action_types: List[str] = Field(default_factory=lambda: ["SYSTEM_DESTROY", "RAW_DATABASE_DROP"])
    is_active: bool = True
