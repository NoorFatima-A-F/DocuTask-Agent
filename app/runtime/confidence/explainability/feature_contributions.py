"""
Feature Contributions Calculator for Phase 13.3 (ASCE-CGP).
Calculates marginal feature contribution and sensitivity gradients.
"""

from typing import Dict, List
from app.runtime.confidence.models.confidence_models import FeatureContribution


class FeatureContributionCalculator:
    """
    Computes normalized contributions per feature.
    """

    @classmethod
    def calculate_contributions(
        cls,
        features: Dict[str, float],
        weights: Dict[str, float],
    ) -> List[FeatureContribution]:
        total_w = sum(weights.values()) if sum(weights.values()) > 0 else 1.0
        contributions: List[FeatureContribution] = []

        for name, w in weights.items():
            val = features.get(name, 0.90)
            norm_w = w / total_w
            contrib = val * norm_w

            contributions.append(
                FeatureContribution(
                    feature_name=name,
                    raw_value=val,
                    normalized_value=val,
                    weight=norm_w,
                    contribution=round(contrib, 4),
                    description=f"Weighted contribution of {name}",
                )
            )

        return contributions
