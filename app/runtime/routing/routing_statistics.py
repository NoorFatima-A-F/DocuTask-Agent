"""
Scientific Model Router - Routing Statistics
Aggregates routing distributions, latency-cost tradeoff profiles, and empirical accuracy per model.
"""

from typing import Dict, List, Any


class ModelRoutingStatistics:
    """Tracks routing selection frequencies and performance differentials."""

    def __init__(self):
        self._counts: Dict[str, int] = {}
        self._cost_totals: Dict[str, float] = {}

    def record_selection(self, model_id: str, cost_usd: float) -> None:
        self._counts[model_id] = self._counts.get(model_id, 0) + 1
        self._cost_totals[model_id] = self._cost_totals.get(model_id, 0.0) + cost_usd

    def get_summary(self) -> Dict[str, Any]:
        total_routes = sum(self._counts.values()) or 1
        return {
            "total_routed_requests": total_routes,
            "distribution_percentages": {
                m: round((count / total_routes) * 100, 2)
                for m, count in self._counts.items()
            },
            "cumulative_cost_by_model": {
                m: round(c, 4) for m, c in self._cost_totals.items()
            },
        }


routing_statistics = ModelRoutingStatistics()
