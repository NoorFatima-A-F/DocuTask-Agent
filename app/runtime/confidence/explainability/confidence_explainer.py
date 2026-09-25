"""
Confidence Explainer for Phase 13.3 (ASCE-CGP).
Provides transparent sensitivity attribution and feature contribution explanations.
"""

from typing import Dict, List, Any
from app.runtime.confidence.models.confidence_models import FeatureContribution


class ConfidenceExplainer:
    """
    Generates human-readable and graphical breakdown of how raw features resulted in the final confidence score.
    """

    @classmethod
    def explain_score(
        cls,
        dimension: str,
        score: float,
        contributions: List[FeatureContribution],
    ) -> Dict[str, Any]:
        top_positive = sorted(contributions, key=lambda c: c.contribution, reverse=True)[:3]

        return {
            "dimension": dimension,
            "final_score": score,
            "total_features": len(contributions),
            "top_drivers": [c.model_dump() for c in top_positive],
            "waterfall_steps": [
                {
                    "step": i + 1,
                    "feature": c.feature_name,
                    "contribution": c.contribution,
                    "weight_pct": round(c.weight * 100, 1),
                }
                for i, c in enumerate(contributions)
            ],
            "summary": f"{dimension} confidence achieved {round(score * 100, 2)}% driven primarily by {top_positive[0].feature_name if top_positive else 'verified evidence'}.",
        }
