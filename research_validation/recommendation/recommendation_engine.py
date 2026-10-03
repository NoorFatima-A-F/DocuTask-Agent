"""
Experiment Recommendation Engine (Phase 85C)
============================================
Synthesizes top recommendations across benchmarks, datasets,
hyperparameter sweeps, and missing statistical validations.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from research_validation.recommendation.roi_calculator import (
    ExperimentROICalculator, ExperimentROIEstimate
)
from research_validation.recommendation.uncertainty_sampler import (
    UncertaintySampler
)
from research_validation.provenance.hashing import hash_canonical_json


class RecommendationType(str, Enum):
    NEXT_BENCHMARK = "NEXT_BENCHMARK"
    NEXT_DATASET = "NEXT_DATASET"
    HYPERPARAMETER_SEARCH = "HYPERPARAMETER_SEARCH"
    STATISTICAL_VALIDATION = "STATISTICAL_VALIDATION"
    MISSING_EVIDENCE = "MISSING_EVIDENCE"
    REPLICATION_AUDIT = "REPLICATION_AUDIT"


@dataclass(frozen=True)
class ExperimentRecommendation:
    """Actionable scientific experiment recommendation."""
    recommendation_id: str
    recommendation_type: RecommendationType
    title: str
    rationale: str
    target_benchmark_or_param: str
    roi_estimate: ExperimentROIEstimate
    priority_score: float
    required_resources: Dict[str, Any] = field(default_factory=dict)
    recommendation_digest_sha256: str = field(default="")


class ExperimentRecommendationEngine:
    """
    Master engine synthesizing high-value research recommendations.
    """

    def __init__(self, roi_calculator: Optional[ExperimentROICalculator] = None):
        self.roi_calc = roi_calculator or ExperimentROICalculator()

    def generate_recommendations(
        self,
        benchmark_observations: Dict[str, Tuple[int, float]],  # name -> (count, std)
        active_regressions_count: int = 0,
        untested_hyperparameters: Optional[List[str]] = None,
    ) -> List[ExperimentRecommendation]:
        recommendations: List[ExperimentRecommendation] = []
        untested_params = untested_hyperparameters or []

        # 1. Evaluate uncertainty gaps across benchmarks
        uncertainty_targets = UncertaintySampler.identify_gaps(benchmark_observations)
        for idx, target in enumerate(uncertainty_targets):
            roi = self.roi_calc.calculate_roi(
                experiment_type=f"Benchmark_{target.target_name}",
                prior_uncertainty_std=target.current_uncertainty_std,
                target_sample_size=target.required_sample_count,
                estimated_runtime_sec=float(target.required_sample_count) * 0.1,
                criticality_weight=1.5 if target.priority_level == "HIGH" else 1.0,
            )
            rec_id = f"rec_bench_{target.target_name}_{idx}"
            payload = {"rec_id": rec_id, "type": RecommendationType.NEXT_BENCHMARK.value, "target": target.target_name}
            digest = hash_canonical_json(payload)

            recommendations.append(ExperimentRecommendation(
                recommendation_id=rec_id,
                recommendation_type=RecommendationType.NEXT_BENCHMARK,
                title=f"Augment empirical observations for {target.target_name}",
                rationale=f"Current sample count is {target.current_sample_count} with standard error {target.current_uncertainty_std:.4f}. Epistemic gap: {target.epistemic_gap:.2f}.",
                target_benchmark_or_param=target.target_name,
                roi_estimate=roi,
                priority_score=roi.net_roi_score * 1.2,
                required_resources={"target_samples": target.required_sample_count},
                recommendation_digest_sha256=digest,
            ))

        # 2. Hyperparameter explorations
        for p in untested_params:
            roi = self.roi_calc.calculate_roi(
                experiment_type=f"HPO_{p}",
                prior_uncertainty_std=0.08,
                target_sample_size=50,
                estimated_runtime_sec=15.0,
                criticality_weight=1.1,
            )
            rec_id = f"rec_hpo_{p}"
            payload = {"rec_id": rec_id, "type": RecommendationType.HYPERPARAMETER_SEARCH.value, "param": p}
            digest = hash_canonical_json(payload)

            recommendations.append(ExperimentRecommendation(
                recommendation_id=rec_id,
                recommendation_type=RecommendationType.HYPERPARAMETER_SEARCH,
                title=f"Explore hyperparameter dimension: {p}",
                rationale=f"Parameter {p} has zero empirical evaluations in memory.",
                target_benchmark_or_param=p,
                roi_estimate=roi,
                priority_score=roi.net_roi_score,
                required_resources={"trials": 20},
                recommendation_digest_sha256=digest,
            ))

        # Sort by priority score descending
        return sorted(recommendations, key=lambda r: r.priority_score, reverse=True)
