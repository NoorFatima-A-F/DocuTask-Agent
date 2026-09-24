"""
Scientific Utility Engine - Tradeoff Analyzer
Analyzes Marginal Rate of Substitution (MRS) and opportunity costs between competing objectives.
"""

from typing import Dict


class TradeoffAnalyzer:
    """Calculates quantitative trade-offs between accuracy, latency, and cost."""

    @staticmethod
    def compute_marginal_rate_of_substitution(
        plan_a: Dict[str, float],
        plan_b: Dict[str, float],
    ) -> Dict[str, float]:
        """Calculates delta ratios between two competing plans."""
        delta_acc = plan_b.get("accuracy", 0.0) - plan_a.get("accuracy", 0.0)
        delta_lat = plan_b.get("latency_ms", 0.0) - plan_a.get("latency_ms", 0.0)
        delta_cost = plan_b.get("cost_usd", 0.0) - plan_a.get("cost_usd", 0.0)

        # Cost per 1% accuracy gain ($ / 0.01 acc)
        cost_per_acc = (delta_cost / (delta_acc * 100)) if abs(delta_acc) > 1e-5 else 0.0

        # Latency ms added per 1% accuracy gain
        lat_per_acc = (delta_lat / (delta_acc * 100)) if abs(delta_acc) > 1e-5 else 0.0

        return {
            "delta_accuracy": round(delta_acc, 4),
            "delta_latency_ms": round(delta_lat, 2),
            "delta_cost_usd": round(delta_cost, 4),
            "cost_per_accuracy_point_usd": round(cost_per_acc, 6),
            "latency_ms_per_accuracy_point": round(lat_per_acc, 2),
        }
