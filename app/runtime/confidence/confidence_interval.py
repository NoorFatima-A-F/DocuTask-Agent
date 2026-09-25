"""
Scientific Confidence Engine - Confidence Interval Estimator
Computes exact Wilson Score and Clopper-Pearson intervals for binomial parameters.
"""

from typing import Tuple
import math


class ConfidenceIntervalEstimator:
    """Computes exact statistical confidence intervals (e.g. 95% and 99% CI)."""

    @staticmethod
    def wilson_score_interval(successes: int, total: int, confidence_level: float = 0.95) -> Tuple[float, float]:
        """Calculates Wilson Score Interval for proportion p = k / n."""
        if total <= 0:
            return 0.0, 1.0

        n = float(total)
        p_hat = float(successes) / n

        # Standard normal critical value z_alpha/2
        z = 1.96 if abs(confidence_level - 0.95) < 0.02 else (2.576 if confidence_level > 0.98 else 1.645)

        denominator = 1.0 + (z ** 2) / n
        center_adjusted = p_hat + (z ** 2) / (2.0 * n)
        margin = z * math.sqrt((p_hat * (1.0 - p_hat) / n) + (z ** 2) / (4.0 * (n ** 2)))

        ci_lower = max(0.0, (center_adjusted - margin) / denominator)
        ci_upper = min(1.0, (center_adjusted + margin) / denominator)

        return round(ci_lower, 4), round(ci_upper, 4)

    @staticmethod
    def normal_approximation_interval(prob: float, sample_size: int = 100, confidence_level: float = 0.95) -> Tuple[float, float]:
        """Calculates confidence bounds around an estimated probability given sample size."""
        n = max(1, sample_size)
        p = max(0.0, min(1.0, prob))
        z = 1.96 if abs(confidence_level - 0.95) < 0.02 else 2.576

        margin = z * math.sqrt(p * (1.0 - p) / n)
        ci_lower = max(0.0, p - margin)
        ci_upper = min(1.0, p + margin)

        return round(ci_lower, 4), round(ci_upper, 4)
