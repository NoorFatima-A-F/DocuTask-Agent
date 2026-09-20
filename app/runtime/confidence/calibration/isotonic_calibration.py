"""
Isotonic Regression Calibrator for Phase 13.3 (ASCE-CGP).
Non-parametric monotonic piecewise calibration.
"""

from typing import List, Tuple


class IsotonicCalibrator:
    """
    Applies monotonic piecewise linear calibration curves.
    """

    DEFAULT_KNOTS: List[Tuple[float, float]] = [
        (0.0, 0.0),
        (0.5, 0.48),
        (0.7, 0.69),
        (0.85, 0.84),
        (0.95, 0.94),
        (0.99, 0.985),
        (1.0, 1.0),
    ]

    @classmethod
    def calibrate(cls, score: float) -> float:
        score = max(0.0, min(1.0, score))
        knots = cls.DEFAULT_KNOTS

        for i in range(len(knots) - 1):
            x0, y0 = knots[i]
            x1, y1 = knots[i + 1]
            if x0 <= score <= x1:
                denom = (x1 - x0) if (x1 - x0) > 0 else 1.0
                t = (score - x0) / denom
                interpolated = y0 + t * (y1 - y0)
                return round(interpolated, 4)

        return round(score, 4)
