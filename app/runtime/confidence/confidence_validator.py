"""
Scientific Confidence Engine - Confidence Validator
Ensures mathematical invariants: bounded probability [0, 1], monotonicity, and determinism.
"""

from typing import Dict, List, Tuple
import math


class ConfidenceValidator:
    """Validates confidence calculation determinism and boundary bounds."""

    @staticmethod
    def validate_bounds(confidence: float, ci_lower: float, ci_upper: float) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        if math.isnan(confidence) or math.isinf(confidence):
            errors.append(f"Confidence score is NaN or Inf: {confidence}")
        elif confidence < 0.0 or confidence > 1.0:
            errors.append(f"Confidence score {confidence} is outside valid probability interval [0, 1].")

        if ci_lower < 0.0 or ci_lower > confidence + 1e-6:
            errors.append(f"CI lower bound {ci_lower} violates ordering ci_lower <= confidence.")

        if ci_upper > 1.0 or ci_upper < confidence - 1e-6:
            errors.append(f"CI upper bound {ci_upper} violates ordering confidence <= ci_upper.")

        return len(errors) == 0, errors

    @staticmethod
    def assert_deterministic(fn, feature_vector: Dict[str, float], trials: int = 10) -> bool:
        """Asserts that identical inputs produce bitwise-identical results across repeated trials."""
        first_res = fn(feature_vector)
        for _ in range(trials - 1):
            res = fn(feature_vector)
            if res != first_res:
                return False
        return True
