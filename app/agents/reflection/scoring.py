"""
Composite Scoring Engine.
Applies weighted multi-factor aggregation to synthesize a single normalized reflection score.
"""

from typing import Dict
from app.agents.reflection.evaluation import EvaluationReport


class CompositeScorer:
    """Calculates weighted composite reflection scores across multiple dimensions."""

    DEFAULT_WEIGHTS = {
        "GOAL_ACHIEVEMENT": 0.30,
        "QUALITY": 0.20,
        "CORRECTNESS": 0.15,
        "EFFICIENCY": 0.10,
        "LATENCY": 0.05,
        "COST": 0.05,
        "TOKEN_UTILIZATION": 0.05,
        "RISK_AND_SAFETY": 0.10,
    }

    def compute_composite_score(
        self,
        report: EvaluationReport,
        custom_weights: Dict[str, float] = None
    ) -> float:
        """Aggregates dimensional scores into a normalized [0.0, 1.0] composite score."""
        weights = custom_weights or self.DEFAULT_WEIGHTS
        total_weight = 0.0
        weighted_sum = 0.0

        for dim_name, dim_eval in report.dimensions.items():
            w = weights.get(dim_name, 0.05)
            weighted_sum += dim_eval.score * w
            total_weight += w

        if total_weight == 0.0:
            return report.overall_score

        return max(0.0, min(1.0, weighted_sum / total_weight))
