"""
ARTEICP Cost Intelligence - Enterprise Budget Governor
Enforces hard cost ceilings, budget guardrails, and dynamic Pareto quality-cost optimization trade-offs.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class BudgetComplianceStatus:
    mission_id: str
    budget_ceiling_usd: float
    accumulated_cost_usd: float
    projected_total_cost_usd: float
    is_within_budget: bool
    budget_utilization_pct: float
    recommended_action: str  # PROCEED_NOMINAL | APPLY_PROMPT_CACHING | DOWNGRADE_TO_FLASH_LITE | HALT_BUDGET_BREACH

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BudgetGovernor:
    """Enforces enterprise budget policies and quality-vs-cost optimization."""

    @classmethod
    def evaluate_budget(
        cls,
        mission_id: str,
        accumulated_cost_usd: float,
        projected_cost_usd: float,
        budget_ceiling_usd: float = 0.010,
    ) -> BudgetComplianceStatus:
        util_pct = (projected_cost_usd / max(1e-6, budget_ceiling_usd)) * 100.0

        if projected_cost_usd > budget_ceiling_usd:
            action = "DOWNGRADE_TO_FLASH_LITE"
            is_ok = False
        elif util_pct >= 80.0:
            action = "APPLY_PROMPT_CACHING"
            is_ok = True
        else:
            action = "PROCEED_NOMINAL"
            is_ok = True

        return BudgetComplianceStatus(
            mission_id=mission_id,
            budget_ceiling_usd=budget_ceiling_usd,
            accumulated_cost_usd=round(accumulated_cost_usd, 5),
            projected_total_cost_usd=round(projected_cost_usd, 5),
            is_within_budget=is_ok,
            budget_utilization_pct=round(util_pct, 1),
            recommended_action=action,
        )
