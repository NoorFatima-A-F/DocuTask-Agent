"""
Weighted Scoring Engine and Certification Band Classifier.
"""
from __future__ import annotations
from typing import Dict, List, Optional
from app.platform_verification.evaluation_engine.domain.models import (
    MetricCategory,
    CertificationBand,
    MetricResult,
    DimensionScore,
    OverallScore,
)
from app.platform_verification.evaluation_engine.domain.interfaces import IScoringEngine

# Default enterprise weighting model
DEFAULT_DIMENSION_WEIGHTS: Dict[MetricCategory, float] = {
    MetricCategory.FUNCTIONAL_CORRECTNESS: 0.30,
    MetricCategory.RELIABILITY: 0.20,
    MetricCategory.PERFORMANCE: 0.15,
    MetricCategory.SECURITY: 0.15,
    MetricCategory.ROBUSTNESS: 0.10,
    MetricCategory.AI_QUALITY: 0.10,
}


class ScoringEngine(IScoringEngine):
    """Calculates weighted dimension scores and assigns certification bands."""

    def __init__(self, default_weights: Optional[Dict[MetricCategory, float]] = None):
        self.weights = default_weights or dict(DEFAULT_DIMENSION_WEIGHTS)

    def compute_overall_score(
        self, metric_results: List[MetricResult], custom_weights: Optional[Dict[MetricCategory, float]] = None
    ) -> OverallScore:
        active_weights = custom_weights or self.weights

        # Group metrics by category
        grouped: Dict[MetricCategory, List[MetricResult]] = {}
        for r in metric_results:
            grouped.setdefault(r.category, []).append(r)

        dimension_scores: Dict[MetricCategory, DimensionScore] = {}
        total_weighted_sum = 0.0
        total_weight_applied = 0.0

        for category, weight in active_weights.items():
            metrics = grouped.get(category, [])
            if not metrics:
                # If category has no metrics, dimension defaults to 100 or is skipped
                dim_score = 100.0
                dim_passed = True
            else:
                dim_score = sum(m.normalized_score for m in metrics) / len(metrics)
                dim_passed = all(m.passed for m in metrics)

            weighted = dim_score * weight
            total_weighted_sum += weighted
            total_weight_applied += weight

            dimension_scores[category] = DimensionScore(
                dimension=category,
                score=round(dim_score, 2),
                weight=weight,
                weighted_score=round(weighted, 2),
                metrics=metrics,
                passed=dim_passed,
            )

        final_score = (
            round(total_weighted_sum / total_weight_applied, 2)
            if total_weight_applied > 0
            else 0.0
        )

        band = self._classify_band(final_score)
        total_m = len(metric_results)
        passed_m = sum(1 for m in metric_results if m.passed)

        return OverallScore(
            overall_score=final_score,
            certification_band=band,
            dimensions=dimension_scores,
            total_metrics=total_m,
            passed_metrics=passed_m,
        )

    def _classify_band(self, score: float) -> CertificationBand:
        if score >= 95.0:
            return CertificationBand.ENTERPRISE_CERTIFIED
        elif score >= 90.0:
            return CertificationBand.PRODUCTION_READY
        elif score >= 80.0:
            return CertificationBand.CONDITIONALLY_READY
        elif score >= 70.0:
            return CertificationBand.DEVELOPMENT_QUALITY
        else:
            return CertificationBand.NOT_READY
