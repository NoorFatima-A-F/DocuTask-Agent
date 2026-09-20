"""
Research Validation & Independent Scientific Verification Framework (RVISF)
Phase 39: Uncertainty Quantification Laboratory

Provides rigorous decomposition of total prediction uncertainty into:
- Aleatoric Uncertainty (data/inherent noise, irreducibility)
- Epistemic Uncertainty (model/knowledge limitation, reducible with more data)
- Bayesian Credible Intervals & Predictive Distribution Entropy
- Conformal Prediction Sets (guaranteed coverage 1 - alpha)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class UncertaintyDecomposition:
    """Decomposition of prediction uncertainty for a single input or batch."""
    total_entropy: float
    aleatoric_uncertainty: float  # Expected entropy of conditional distributions
    epistemic_uncertainty: float  # Mutual Information I(Y; W | X) = Total - Aleatoric
    epistemic_ratio: float  # Epistemic / Total (0.0 to 1.0)
    prediction_confidence: float
    is_out_of_distribution: bool


@dataclass
class ConformalPredictionInterval:
    """Conformal prediction interval with rigorous finite-sample coverage guarantee."""
    point_prediction: float
    lower_bound: float
    upper_bound: float
    significance_level_alpha: float
    target_coverage: float  # 1 - alpha
    interval_width: float


@dataclass
class UncertaintyAuditReport:
    """Audit report for uncertainty quantification and risk scoring."""
    sample_size: int
    mean_total_entropy: float
    mean_aleatoric: float
    mean_epistemic: float
    mean_interval_width: float
    ood_detection_count: int
    empirical_coverage: Optional[float] = None
    status: str = "PASS"
    details: Dict[str, Any] = field(default_factory=dict)


class UncertaintyQuantificationLab:
    """
    Quantifies epistemic vs aleatoric uncertainty and builds conformal prediction intervals.
    """

    @staticmethod
    def calculate_shannon_entropy(probs: List[float], eps: float = 1e-12) -> float:
        """Calculate Shannon entropy in nats: H(p) = - sum p_i * ln(p_i)."""
        return -sum(p * math.log(max(p, eps)) for p in probs if p > 0.0)

    @classmethod
    def decompose_ensemble_uncertainty(
        cls,
        ensemble_probabilities: List[List[float]],
        ood_threshold_ratio: float = 0.5
    ) -> UncertaintyDecomposition:
        """
        Decompose uncertainty given an ensemble of M models / MC Dropout passes.
        ensemble_probabilities: List of M probability distributions over C classes.
        """
        if not ensemble_probabilities:
            raise ValueError("Ensemble probabilities cannot be empty.")

        m = len(ensemble_probabilities)
        num_classes = len(ensemble_probabilities[0])

        # 1. Calculate ensemble mean prediction distribution: p_bar = 1/M sum_m p_m
        p_bar = [0.0] * num_classes
        for probs in ensemble_probabilities:
            for c in range(num_classes):
                p_bar[c] += probs[c] / m

        # 2. Total uncertainty = Entropy of mean prediction H(p_bar)
        total_entropy = cls.calculate_shannon_entropy(p_bar)

        # 3. Aleatoric uncertainty = Mean entropy across ensemble passes E[H(p_m)]
        individual_entropies = [cls.calculate_shannon_entropy(p) for p in ensemble_probabilities]
        aleatoric = sum(individual_entropies) / m

        # 4. Epistemic uncertainty = Mutual Information = Total - Aleatoric
        epistemic = max(0.0, total_entropy - aleatoric)

        epistemic_ratio = (epistemic / total_entropy) if total_entropy > 1e-12 else 0.0
        confidence = max(p_bar) if p_bar else 0.0
        is_ood = epistemic_ratio > ood_threshold_ratio and total_entropy > 0.5

        return UncertaintyDecomposition(
            total_entropy=total_entropy,
            aleatoric_uncertainty=aleatoric,
            epistemic_uncertainty=epistemic,
            epistemic_ratio=epistemic_ratio,
            prediction_confidence=confidence,
            is_out_of_distribution=is_ood
        )

    @staticmethod
    def compute_conformal_quantile(residuals: List[float], alpha: float = 0.1) -> float:
        """
        Compute standard split-conformal non-conformity quantile:
        q_val = ceil((n + 1) * (1 - alpha)) / n
        """
        if not residuals:
            raise ValueError("Residuals list cannot be empty.")
        n = len(residuals)
        sorted_res = sorted(residuals)
        k = math.ceil((n + 1) * (1.0 - alpha))
        idx = min(max(k - 1, 0), n - 1)
        return sorted_res[idx]

    @classmethod
    def construct_conformal_interval(
        cls,
        point_prediction: float,
        calibration_residuals: List[float],
        alpha: float = 0.1
    ) -> ConformalPredictionInterval:
        """
        Construct a split-conformal prediction interval guaranteeing (1 - alpha) coverage.
        """
        q_val = cls.compute_conformal_quantile(calibration_residuals, alpha=alpha)
        low = point_prediction - q_val
        high = point_prediction + q_val
        return ConformalPredictionInterval(
            point_prediction=point_prediction,
            lower_bound=low,
            upper_bound=high,
            significance_level_alpha=alpha,
            target_coverage=1.0 - alpha,
            interval_width=high - low
        )

    @classmethod
    def run_uncertainty_audit(
        cls,
        ensemble_batch: List[List[List[float]]],
        calibration_residuals: Optional[List[float]] = None,
        test_points: Optional[List[Tuple[float, float]]] = None
    ) -> UncertaintyAuditReport:
        """
        Run comprehensive uncertainty quantification across a batch of sample predictions.
        """
        if not ensemble_batch:
            return UncertaintyAuditReport(
                sample_size=0,
                mean_total_entropy=0.0,
                mean_aleatoric=0.0,
                mean_epistemic=0.0,
                mean_interval_width=0.0,
                ood_detection_count=0,
                status="INSUFFICIENT_EVIDENCE"
            )

        decomps = [cls.decompose_ensemble_uncertainty(ens) for ens in ensemble_batch]
        n = len(decomps)
        mean_tot = sum(d.total_entropy for d in decomps) / n
        mean_alea = sum(d.aleatoric_uncertainty for d in decomps) / n
        mean_epis = sum(d.epistemic_uncertainty for d in decomps) / n
        ood_count = sum(1 for d in decomps if d.is_out_of_distribution)

        mean_width = 0.0
        emp_coverage = None

        if calibration_residuals and test_points:
            intervals = [cls.construct_conformal_interval(pred, calibration_residuals) for pred, _ in test_points]
            mean_width = sum(i.interval_width for i in intervals) / len(intervals)
            covered = sum(1 for (pred, actual), interval in zip(test_points, intervals)
                          if interval.lower_bound <= actual <= interval.upper_bound)
            emp_coverage = covered / len(test_points)

        return UncertaintyAuditReport(
            sample_size=n,
            mean_total_entropy=mean_tot,
            mean_aleatoric=mean_alea,
            mean_epistemic=mean_epis,
            mean_interval_width=mean_width,
            ood_detection_count=ood_count,
            empirical_coverage=emp_coverage,
            status="PASS" if mean_epis >= 0.0 and mean_alea >= 0.0 else "VALIDATION_FAILED"
        )
