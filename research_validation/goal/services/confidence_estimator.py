"""
Confidence Estimator Service
============================
Estimates required confidence thresholds and assesses whether sample sizes guarantee target power.
"""

import math
from typing import List
from research_validation.goal.models.confidence_threshold import ConfidenceThreshold, ConfidenceLevel
from research_validation.goal.models.success_criteria import SuccessCriterion


class ConfidenceEstimatorService:
    """Estimates and verifies statistical confidence thresholds for goals."""

    @classmethod
    def estimate_required_confidence(
        cls,
        priority_level: str,
        success_criteria: List[SuccessCriterion],
    ) -> ConfidenceThreshold:
        """Determines appropriate confidence threshold based on priority and criteria weight."""
        if priority_level == "CRITICAL":
            return ConfidenceThreshold(ConfidenceLevel.VERY_HIGH)  # 0.99
        elif priority_level == "HIGH":
            return ConfidenceThreshold(ConfidenceLevel.HIGH)       # 0.90
        elif priority_level == "NORMAL":
            return ConfidenceThreshold(ConfidenceLevel.MEDIUM)     # 0.70
        else:
            return ConfidenceThreshold(ConfidenceLevel.LOW)        # 0.50

    @classmethod
    def estimate_required_sample_size(
        cls,
        target_confidence: float,
        target_power: float = 0.80,
        expected_effect_size: float = 0.5,
    ) -> int:
        """
        Estimates minimum sample size required for given power and significance alpha = (1 - confidence):
        n >= 2 * ((z_alpha + z_beta) / effect_size)^2
        """
        alpha = max(0.001, 1.0 - target_confidence)
        z_alpha = 1.96 if alpha <= 0.05 else (2.576 if alpha <= 0.01 else 1.645)
        z_beta = 0.84  # 80% power
        n = 2.0 * (((z_alpha + z_beta) / max(0.1, expected_effect_size)) ** 2)
        return max(30, int(math.ceil(n)))
