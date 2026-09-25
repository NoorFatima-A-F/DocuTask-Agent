"""
Counterfactual Simulator - Comparison Engine
Calculates Opportunity Cost, Delta Utility, and Planner Regret between factual and counterfactual outcomes.
"""

from typing import Dict, Any
from dataclasses import dataclass, asdict
from app.runtime.counterfactual.alternate_planner import CounterfactualCandidate


@dataclass
class CounterfactualDifferential:
    factual_choice: str
    counterfactual_choice: str
    factual_utility: float
    counterfactual_utility: float
    delta_utility: float  # U(factual) - U(counterfactual)
    opportunity_cost_usd: float
    latency_delta_ms: float
    accuracy_delta: float
    factual_was_optimal: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CounterfactualComparisonEngine:
    """Evaluates the post-hoc regret and opportunity costs of real vs simulated branches."""

    @staticmethod
    def compare_branch(
        factual_model: str,
        factual_acc: float,
        factual_lat_ms: float,
        factual_cost_usd: float,
        factual_u: float,
        candidate: CounterfactualCandidate,
    ) -> CounterfactualDifferential:
        delta_u = factual_u - candidate.simulated_utility
        opp_cost = max(0.0, candidate.simulated_cost_usd - factual_cost_usd)
        lat_diff = candidate.simulated_latency_ms - factual_lat_ms
        acc_diff = candidate.simulated_accuracy - factual_acc

        return CounterfactualDifferential(
            factual_choice=factual_model,
            counterfactual_choice=candidate.intervention_label,
            factual_utility=round(factual_u, 4),
            counterfactual_utility=round(candidate.simulated_utility, 4),
            delta_utility=round(delta_u, 4),
            opportunity_cost_usd=round(opp_cost, 5),
            latency_delta_ms=round(lat_diff, 1),
            accuracy_delta=round(acc_diff, 4),
            factual_was_optimal=delta_u >= 0.0,
        )
