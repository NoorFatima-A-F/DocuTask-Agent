"""Regret Engine for DocuTask ADIP Meta-Reasoning Layer.

Calculates Expected Regret, Counterfactual Regret, and Opportunity Cost across strategy candidates.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RegretAnalysisResult(BaseModel):
    """Mathematical regret evaluation for a chosen strategy."""
    mission_id: str
    chosen_strategy_id: str
    optimal_strategy_id: str
    expected_regret: float = Field(ge=0.0, description="Max Expected Utility - Chosen Expected Utility")
    counterfactual_regret: float = Field(ge=0.0)
    opportunity_cost_usd: float
    regret_ratio: float = Field(ge=0.0, le=1.0)
    verdict: str = ""
    formula_provenance: str = "\\mathbb{E}[R] = \\max_{a} \\mathbb{E}[U(a)] - \\mathbb{E}[U(a^*)]"


class RegretEngine:
    """Computes bounded regret metrics for strategic decisions."""

    def compute_regret(
        self,
        mission_id: str,
        chosen_strategy_id: str,
        strategy_utilities: Dict[str, float],
        strategy_costs: Dict[str, float],
    ) -> RegretAnalysisResult:
        if not strategy_utilities:
            return RegretAnalysisResult(
                mission_id=mission_id,
                chosen_strategy_id=chosen_strategy_id,
                optimal_strategy_id=chosen_strategy_id,
                expected_regret=0.0,
                counterfactual_regret=0.0,
                opportunity_cost_usd=0.0,
                regret_ratio=0.0,
                verdict="Zero regret.",
            )

        best_id = max(strategy_utilities, key=strategy_utilities.get) # type: ignore
        max_u = strategy_utilities[best_id]
        chosen_u = strategy_utilities.get(chosen_strategy_id, 0.0)

        exp_regret = max(0.0, round(max_u - chosen_u, 4))
        cf_regret = exp_regret * 1.15  # Counterfactual risk buffer

        best_cost = strategy_costs.get(best_id, 0.0)
        chosen_cost = strategy_costs.get(chosen_strategy_id, 0.0)
        opp_cost = max(0.0, round(chosen_cost - best_cost, 6))

        regret_ratio = round(exp_regret / max(1e-4, abs(max_u) + abs(chosen_u)), 4)

        if exp_regret < 0.01:
            verdict = "Optimal policy. Minimized regret bound."
        elif exp_regret < 0.08:
            verdict = "Low regret. Sub-optimal within acceptable tolerance."
        else:
            verdict = "Elevated regret. High opportunity cost detected."

        return RegretAnalysisResult(
            mission_id=mission_id,
            chosen_strategy_id=chosen_strategy_id,
            optimal_strategy_id=best_id,
            expected_regret=exp_regret,
            counterfactual_regret=round(cf_regret, 4),
            opportunity_cost_usd=opp_cost,
            regret_ratio=min(1.0, regret_ratio),
            verdict=verdict,
        )
