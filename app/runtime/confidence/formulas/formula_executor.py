"""
Formula Executor for Phase 13.3 (ASCE-CGP).
Executes mathematical models (Weighted Sum, Bayesian, Reliability Multiplication, Logistic Scaling, Hybrid Ensemble).
"""

import math
from typing import Dict, List, Tuple
from app.runtime.confidence.models.confidence_models import FeatureContribution


class FormulaExecutor:
    """
    Executes version-controlled mathematical confidence formulas.
    """

    @classmethod
    def execute_weighted_sum(
        cls,
        features: Dict[str, float],
        weights: Dict[str, float],
    ) -> Tuple[float, List[FeatureContribution]]:
        total_weight = sum(weights.values()) if sum(weights.values()) > 0 else 1.0
        contributions: List[FeatureContribution] = []
        score = 0.0

        for name, weight in weights.items():
            val = features.get(name, 0.85)
            normalized_weight = weight / total_weight
            contrib = val * normalized_weight
            score += contrib

            contributions.append(
                FeatureContribution(
                    feature_name=name,
                    raw_value=val,
                    normalized_value=val,
                    weight=normalized_weight,
                    contribution=round(contrib, 4),
                    description=f"Feature {name} weighted by {round(normalized_weight * 100, 1)}%",
                )
            )

        final_score = round(max(0.0, min(1.0, score)), 4)
        return final_score, contributions

    @classmethod
    def execute_bayesian_update(cls, prior: float, likelihood: float) -> float:
        """
        Calculates posterior confidence: P(H|E) = (P(E|H) * P(H)) / P(E)
        """
        numerator = likelihood * prior
        evidence = numerator + ((1.0 - likelihood) * (1.0 - prior))
        if evidence <= 0.0:
            return prior
        return round(max(0.0, min(1.0, numerator / evidence)), 4)

    @classmethod
    def execute_reliability_multiplication(cls, scores: List[float]) -> float:
        """
        Multiplies independent reliability components: R_total = prod(R_i)
        """
        if not scores:
            return 1.0
        res = 1.0
        for s in scores:
            res *= max(0.0, min(1.0, s))
        return round(res, 4)
