"""
Confidence Interval Engine for Phase 13.3 (ASCE-CGP).
Calculates 95% and 99% confidence intervals for decision certainty.
"""

from typing import Tuple


class ConfidenceIntervalEngine:
    """
    Computes statistical confidence intervals for confidence scores.
    """

    @classmethod
    def compute_interval(
        cls,
        confidence: float,
        uncertainty: float,
        level: float = 0.95,
    ) -> Tuple[float, float]:
        # Z-score for standard confidence intervals
        z = 1.96 if level == 0.95 else 2.576
        margin = z * uncertainty

        lower = round(max(0.0, confidence - margin), 4)
        upper = round(min(1.0, confidence + margin), 4)
        return lower, upper
