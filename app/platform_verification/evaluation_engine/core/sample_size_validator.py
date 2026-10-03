"""
Statistical Power and Sample Size Validation Engine.
"""
from __future__ import annotations
import math
from app.platform_verification.evaluation_engine.domain.models import SampleSizeValidationResult
from app.platform_verification.evaluation_engine.domain.interfaces import ISampleSizeValidator


class SampleSizeValidator(ISampleSizeValidator):
    """Evaluates whether evaluation datasets meet statistical power requirements."""

    def validate_power(
        self, sample_size: int, confidence: float = 0.95, margin_of_error: float = 0.05
    ) -> SampleSizeValidationResult:
        z = 1.95996 if confidence == 0.95 else (2.57583 if confidence == 0.99 else 1.64485)
        # Cochran's formula for sample size: N = (Z^2 * p * (1-p)) / e^2 (assuming p=0.5 for maximum variability)
        p = 0.5
        min_required = int(math.ceil((z ** 2 * p * (1 - p)) / (margin_of_error ** 2)))

        is_sufficient = sample_size >= min_required
        power = min(1.0, round(sample_size / max(1, min_required), 2))

        if is_sufficient:
            rec = f"Sample size {sample_size} is statistically powered (confidence: {int(confidence*100)}%, margin of error: {margin_of_error*100}%)."
        else:
            rec = f"Sample size {sample_size} is insufficient for definitive certification (minimum required: {min_required} samples for +/-{margin_of_error*100}% precision)."

        return SampleSizeValidationResult(
            sample_size=sample_size,
            is_sufficient=is_sufficient,
            minimum_required=min_required,
            confidence_level=confidence,
            margin_of_error_pct=round(margin_of_error * 100.0, 2),
            statistical_power=power,
            recommendation=rec,
        )
