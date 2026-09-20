"""
Governance Framework Models.
"""

from typing import List
from pydantic import BaseModel, Field
from app.agents.decision.policies import ApprovalPolicy, CompliancePolicy, CostPolicy, SecurityPolicy


class GovernanceFramework(BaseModel):
    """Aggregate Enterprise Governance Framework."""

    cost_policy: CostPolicy = Field(default_factory=CostPolicy)
    security_policy: SecurityPolicy = Field(default_factory=SecurityPolicy)
    compliance_policy: CompliancePolicy = Field(default_factory=CompliancePolicy)
    approval_policy: ApprovalPolicy = Field(default_factory=ApprovalPolicy)
    model_config = {"frozen": True}
