"""
Experiment ROI Calculator (Phase 85C)
====================================
Computes Return-On-Investment (ROI) of proposed experiments based on
Expected Information Gain (EIG), uncertainty reduction, and computational cost.
"""

from __future__ import annotations
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentROIEstimate:
    """Quantitative ROI score and cost-benefit breakdown."""
    experiment_type: str
    expected_information_gain_bits: float
    uncertainty_reduction_potential: float  # 0.0 to 1.0
    estimated_runtime_seconds: float
    estimated_cost_score: float
    net_roi_score: float
    recommendation_rank: int = 0


class ExperimentROICalculator:
    """
    Evaluates proposed experiments against scientific information value vs execution cost.
    """

    @classmethod
    def calculate_roi(
        cls,
        experiment_type: str,
        prior_uncertainty_std: float,
        target_sample_size: int,
        estimated_runtime_sec: float,
        criticality_weight: float = 1.0,
    ) -> ExperimentROIEstimate:
        """
        Calculates net scientific ROI:
        EIG = 0.5 * log2(1 + (prior_std / post_std)^2)
        Net ROI = (EIG * criticality_weight) / log2(2 + runtime_sec)
        """
        # Estimated posterior std given sample size
        post_std = prior_uncertainty_std / math.sqrt(max(1, target_sample_size))
        variance_ratio = (prior_uncertainty_std / max(1e-6, post_std)) ** 2
        eig_bits = 0.5 * math.log2(1.0 + variance_ratio)
        
        unc_reduction = max(0.0, min(1.0, (prior_uncertainty_std - post_std) / max(1e-6, prior_uncertainty_std)))
        cost_score = math.log2(2.0 + estimated_runtime_sec)
        
        net_roi = (eig_bits * criticality_weight * (1.0 + unc_reduction)) / max(0.1, cost_score)

        return ExperimentROIEstimate(
            experiment_type=experiment_type,
            expected_information_gain_bits=eig_bits,
            uncertainty_reduction_potential=unc_reduction,
            estimated_runtime_seconds=estimated_runtime_sec,
            estimated_cost_score=cost_score,
            net_roi_score=net_roi,
        )
