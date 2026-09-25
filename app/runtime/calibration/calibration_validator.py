"""
Scientific Calibration Platform - Calibration Validator
Validates that model predictions comply with enterprise calibration thresholds (e.g. ECE < 0.08).
"""

from typing import Dict, List, Tuple


class CalibrationValidator:
    """Validates calibration error thresholds."""

    @staticmethod
    def validate_calibration_quality(
        metrics: Dict[str, float],
        max_allowed_ece: float = 0.08,
        max_allowed_brier: float = 0.15,
    ) -> Tuple[bool, List[str]]:
        errors = []
        ece = metrics.get("ece", 0.0)
        brier = metrics.get("brier_score", 0.0)

        if ece > max_allowed_ece:
            errors.append(f"Expected Calibration Error ({ece:.4f}) exceeds threshold ({max_allowed_ece:.4f})")

        if brier > max_allowed_brier:
            errors.append(f"Brier Score ({brier:.4f}) exceeds threshold ({max_allowed_brier:.4f})")

        return len(errors) == 0, errors
