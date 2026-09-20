"""Enterprise Governance & Approval Authority for DocuTask ADIP.

Enforces role-based approvals, high-risk gatekeeping, emergency operational overrides,
and compliance safeguards on autonomous planning decisions.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ApprovalTier(str, Enum):
    AUTO_APPROVED = "AUTO_APPROVED"
    SUPERVISOR_REQUIRED = "SUPERVISOR_REQUIRED"
    COMPLIANCE_OFFICER_REQUIRED = "COMPLIANCE_OFFICER_REQUIRED"
    BLOCKED_HIGH_RISK = "BLOCKED_HIGH_RISK"


class GovernanceDecision(BaseModel):
    """Decision made by the enterprise governance gatekeeper."""
    governance_id: str = Field(default_factory=lambda: f"gov_{uuid.uuid4().hex[:8]}")
    mission_id: str
    strategy_id: str
    approval_tier: ApprovalTier
    is_approved: bool
    requires_human_signoff: bool
    risk_score: float
    applied_policy: str
    rationale: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EnterpriseGovernanceEngine:
    """Evaluates mission risk profiles against regulatory and enterprise governance rules."""

    def evaluate_governance(
        self,
        mission_id: str,
        strategy_id: str,
        estimated_risk: float,
        is_smt_verified: bool,
        cost_usd: float,
        policy_name: str = "Enterprise Standard Policy",
    ) -> GovernanceDecision:
        if not is_smt_verified:
            return GovernanceDecision(
                mission_id=mission_id,
                strategy_id=strategy_id,
                approval_tier=ApprovalTier.BLOCKED_HIGH_RISK,
                is_approved=False,
                requires_human_signoff=True,
                risk_score=estimated_risk,
                applied_policy=policy_name,
                rationale="Blocked: Strategy failed formal SMT constraint verification.",
            )

        if estimated_risk > 0.20 or cost_usd > 1.00:
            return GovernanceDecision(
                mission_id=mission_id,
                strategy_id=strategy_id,
                approval_tier=ApprovalTier.COMPLIANCE_OFFICER_REQUIRED,
                is_approved=False,
                requires_human_signoff=True,
                risk_score=estimated_risk,
                applied_policy=policy_name,
                rationale="Elevated risk or high cost requires human compliance officer authorization.",
            )

        if estimated_risk > 0.10:
            return GovernanceDecision(
                mission_id=mission_id,
                strategy_id=strategy_id,
                approval_tier=ApprovalTier.SUPERVISOR_REQUIRED,
                is_approved=False,
                requires_human_signoff=True,
                risk_score=estimated_risk,
                applied_policy=policy_name,
                rationale="Moderate risk: supervisor dual-signoff recommended.",
            )

        return GovernanceDecision(
            mission_id=mission_id,
            strategy_id=strategy_id,
            approval_tier=ApprovalTier.AUTO_APPROVED,
            is_approved=True,
            requires_human_signoff=False,
            risk_score=estimated_risk,
            applied_policy=policy_name,
            rationale="Approved: Formal verification passed and risk is below automated threshold (<= 10%).",
        )
