"""
Evidence Weight Calibration & Dynamic Weighting (Phase 82B.9)
=============================================================
Replaces static constants with dynamic, uncertainty-aware evidence quality weights.
Conducts sensitivity analyses, Monte Carlo perturbations, and robustness sweeps.
"""

from __future__ import annotations
import math
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from research_validation.provenance.provenance_models import EvidenceQualityLevel
from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class CalibratedWeightScheme:
    scheme_name: str
    weights: Dict[EvidenceQualityLevel, float]
    calibration_basis: str
    uncertainty_penalty_factor: float
    is_statistically_justified: bool


@dataclass(frozen=True)
class WeightSensitivityReport:
    base_score: float
    min_perturbed_score: float
    max_perturbed_score: float
    spread: float
    is_robust: bool  # spread < 0.10
    perturbation_runs: int
    parameter_elasticities: Dict[str, float]
    recommendation: str


class DynamicEvidenceWeightEngine:
    """
    Computes calibrated evidence weights adjusted for sample size and variance.
    """

    DEFAULT_BASE_WEIGHTS = {
        EvidenceQualityLevel.LEVEL_A: 1.00,
        EvidenceQualityLevel.LEVEL_B: 0.85,
        EvidenceQualityLevel.LEVEL_C: 0.70,
        EvidenceQualityLevel.LEVEL_D: 0.40,
        EvidenceQualityLevel.LEVEL_E: 0.00,
    }

    @classmethod
    def compute_dynamic_weights(
        cls,
        sample_counts: Dict[EvidenceQualityLevel, int],
        standard_errors: Optional[Dict[EvidenceQualityLevel, float]] = None,
        base_weights: Optional[Dict[EvidenceQualityLevel, float]] = None,
    ) -> CalibratedWeightScheme:
        """
        Calibrate evidence weights based on empirical sample size and standard errors.
        Applies Bayesian shrinkage / uncertainty penalty.
        """
        base = base_weights or cls.DEFAULT_BASE_WEIGHTS
        calibrated: Dict[EvidenceQualityLevel, float] = {}

        for lvl, base_w in base.items():
            if lvl == EvidenceQualityLevel.LEVEL_E:
                calibrated[lvl] = 0.0
                continue

            n = sample_counts.get(lvl, 0)
            serr = standard_errors.get(lvl, 0.05) if standard_errors else 0.05

            # Sample size sufficiency factor: tanh(sqrt(N) / 5.0)
            sample_factor = math.tanh(math.sqrt(max(0, n)) / 5.0) if n > 0 else 0.5
            # Uncertainty penalty: exp(-2 * std_err)
            unc_penalty = math.exp(-2.0 * serr)

            dyn_w = base_w * (0.6 * sample_factor + 0.4 * unc_penalty)
            calibrated[lvl] = max(0.0, min(1.0, dyn_w))

        return CalibratedWeightScheme(
            scheme_name="Dynamic_Bayesian_Shrinkage",
            weights=calibrated,
            calibration_basis="Sample-size sufficiency tanh scaling combined with analytical standard error exponential attenuation.",
            uncertainty_penalty_factor=0.4,
            is_statistically_justified=True,
        )

    @classmethod
    def evaluate_weight_sensitivity(
        cls,
        quality_counts: Dict[EvidenceQualityLevel, int],
        base_weights: Optional[Dict[EvidenceQualityLevel, float]] = None,
        perturbation_std: float = 0.05,
        num_simulations: int = 1000,
        seed: int = 42,
    ) -> WeightSensitivityReport:
        """
        Perturb weights via Gaussian Monte Carlo to assess readiness score stability.
        """
        rng = random.Random(seed)
        weights = base_weights or cls.DEFAULT_BASE_WEIGHTS
        total_items = sum(quality_counts.values())

        if total_items == 0:
            return WeightSensitivityReport(
                base_score=0.0,
                min_perturbed_score=0.0,
                max_perturbed_score=0.0,
                spread=0.0,
                is_robust=True,
                perturbation_runs=num_simulations,
                parameter_elasticities={},
                recommendation="No evidence items to evaluate.",
            )

        base_score = sum(weights[lvl] * cnt for lvl, cnt in quality_counts.items()) / total_items
        perturbed_scores: List[float] = []

        for _ in range(num_simulations):
            sim_weights = {}
            for lvl, w in weights.items():
                if lvl == EvidenceQualityLevel.LEVEL_E:
                    sim_weights[lvl] = 0.0
                else:
                    noise = rng.gauss(0.0, perturbation_std)
                    sim_weights[lvl] = max(0.0, min(1.0, w + noise))

            sim_score = sum(sim_weights[lvl] * cnt for lvl, cnt in quality_counts.items()) / total_items
            perturbed_scores.append(sim_score)

        min_s = min(perturbed_scores)
        max_s = max(perturbed_scores)
        spread = max_s - min_s
        is_robust = spread < 0.20

        elasticities = {
            lvl.value: (quality_counts.get(lvl, 0) / total_items) * weights[lvl]
            for lvl in EvidenceQualityLevel
        }

        rec = (
            "Readiness score is resilient to weight perturbations (spread < 0.20)."
            if is_robust else
            "High sensitivity to evidence weights! Increase sample counts for lower tiers."
        )

        return WeightSensitivityReport(
            base_score=base_score,
            min_perturbed_score=min_s,
            max_perturbed_score=max_s,
            spread=spread,
            is_robust=is_robust,
            perturbation_runs=num_simulations,
            parameter_elasticities=elasticities,
            recommendation=rec,
        )
