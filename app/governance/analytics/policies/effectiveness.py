"""Policy Effectiveness Evaluator and Optimization Recommendations."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from ..warehouse.repositories import GovernanceDataWarehouseRepository
from ..warehouse.schemas import WarehouseQueryFilter


class PolicyRecommendation(BaseModel):
    policy_id: str
    recommendation_type: str  # LOOSEN_THRESHOLD, TIGHTEN_RULE, SPLIT_POLICY, DEPRECATE_UNUSED
    severity: str             # LOW, MEDIUM, HIGH
    rationale: str
    suggested_action: str


class PolicyEffectivenessSummary(BaseModel):
    tenant_id: str
    overall_effectiveness_score: float = 1.0  # 0.0 to 1.0
    false_positive_estimate_rate: float = 0.0
    recommendations: List[PolicyRecommendation] = Field(default_factory=list)


class PolicyEffectivenessEngine:
    """Evaluates whether policies achieve their intended safety goals without unnecessary enterprise friction."""

    def __init__(self, repository: Optional[GovernanceDataWarehouseRepository] = None):
        self.repo = repository or GovernanceDataWarehouseRepository()

    def evaluate_effectiveness(self, tenant_id: str = "*") -> PolicyEffectivenessSummary:
        q = WarehouseQueryFilter(tenant_id=tenant_id)
        policy_events = self.repo.query_policy_events(q)
        approvals = self.repo.query_approvals(q)

        # High overrides on approved reviews indicate false positive blocks
        overrides_on_blocks = sum(1 for a in approvals if a.is_override or a.outcome == "APPROVED")
        total_approvals = len(approvals)

        false_pos_rate = (overrides_on_blocks / total_approvals) if total_approvals > 0 else 0.05
        effectiveness_score = max(0.0, 1.0 - false_pos_rate)

        recommendations: List[PolicyRecommendation] = []

        # Generate actionable recommendations
        if false_pos_rate > 0.4:
            recommendations.append(
                PolicyRecommendation(
                    policy_id="pol_global_friction",
                    recommendation_type="LOOSEN_THRESHOLD",
                    severity="HIGH",
                    rationale=f"Over {false_pos_rate*100:.1f}% of policy triggers were manually approved or overridden by human reviewers.",
                    suggested_action="Review and loosen risk threshold triggers to reduce reviewer fatigue on legitimate requests.",
                )
            )

        # Unused policy recommendation
        all_pols = [p for p in self.repo.dim_policies.values() if tenant_id == "*" or p.tenant_id == tenant_id]
        triggered_pids = {pe.policy_id for pe in policy_events}
        for pol in all_pols:
            if pol.policy_id not in triggered_pids:
                recommendations.append(
                    PolicyRecommendation(
                        policy_id=pol.policy_id,
                        recommendation_type="DEPRECATE_UNUSED",
                        severity="LOW",
                        rationale=f"Policy '{pol.policy_name}' has 0 recorded triggers across current telemetry.",
                        suggested_action="Verify policy condition coverage or consider archiving if obsolete.",
                    )
                )

        return PolicyEffectivenessSummary(
            tenant_id=tenant_id,
            overall_effectiveness_score=round(effectiveness_score, 4),
            false_positive_estimate_rate=round(false_pos_rate, 4),
            recommendations=recommendations,
        )
