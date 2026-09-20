"""
Policy Evaluation Engine - Regret Analysis
Calculates instantaneous and cumulative regret against an ex-post optimal oracle decision.
"""

from typing import List, Dict, Any
import math


class RegretAnalyzer:
    """Computes planner regret metrics: Regret_t = U(pi*) - U(pi_t)."""

    @staticmethod
    def compute_regret(
        selected_utilities: List[float],
        oracle_utilities: List[float],
    ) -> Dict[str, Any]:
        if not selected_utilities or len(selected_utilities) != len(oracle_utilities):
            return {
                "instantaneous_regrets": [],
                "cumulative_regrets": [],
                "total_regret": 0.0,
                "average_regret": 0.0,
                "sublinear_rate": True,
            }

        instant_regrets = []
        cum_regrets = []
        cum = 0.0

        for sel_u, orac_u in zip(selected_utilities, oracle_utilities):
            r = max(0.0, orac_u - sel_u)
            instant_regrets.append(round(r, 4))
            cum += r
            cum_regrets.append(round(cum, 4))

        n = len(instant_regrets)
        avg_regret = cum / n if n > 0 else 0.0

        # Sublinear test: check if average regret is decreasing over time
        is_sublinear = (
            cum_regrets[-1] / n <= (cum_regrets[max(0, n // 2)] / max(1, n // 2)) + 0.01
            if n > 4
            else True
        )

        return {
            "instantaneous_regrets": instant_regrets,
            "cumulative_regrets": cum_regrets,
            "total_regret": round(cum, 4),
            "average_regret": round(avg_regret, 4),
            "sublinear_rate": is_sublinear,
        }
