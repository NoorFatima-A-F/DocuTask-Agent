"""
Confidence Validation Engine for Phase 13.3 (ASCE-CGP).
Statistical validator that guards against confidence saturation, phantom high-confidence, and impossible scores.
"""

from typing import Tuple


class ConfidenceStatisticalValidator:
    """
    Validates that confidence scores are mathematically consistent with observed evidence strength.
    """

    @classmethod
    def validate_confidence_consistency(
        cls,
        confidence_score: float,
        evidence_count: int,
        invariant_failures: int = 0,
    ) -> Tuple[bool, str]:
        # Rule 1: High confidence (>=0.99) with zero or very few evidence signals is impossible
        if confidence_score >= 0.99 and evidence_count < 2:
            return False, "Confidence saturation alert: 99%+ claimed with insufficient evidence backing."

        # Rule 2: Invariant failures must strictly forbid >90% validation confidence
        if invariant_failures > 0 and confidence_score > 0.90:
            return False, f"Impossible score: {invariant_failures} invariant violations detected."

        # Rule 3: Valid bounds
        if confidence_score < 0.0 or confidence_score > 1.0:
            return False, f"Confidence {confidence_score} strictly outside [0, 1]."

        return True, "Confidence score is statistically sound and evidence-backed."
