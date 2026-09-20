"""
Formula Validator for Phase 13.3 (ASCE-CGP).
Verifies formula mathematical soundness, boundary conditions, and monotonicity.
"""

from typing import Dict, List, Tuple


class FormulaValidator:
    """
    Validates formula outputs and ensures mathematical invariance.
    """

    @classmethod
    def validate_monotonicity(cls, base_score: float, improved_score: float) -> bool:
        """
        Monotonicity invariant: higher positive feature values must not decrease score.
        """
        return improved_score >= base_score - 1e-6

    @classmethod
    def validate_bounds(cls, score: float) -> bool:
        """
        Bounds invariant: score must remain strictly within [0.0, 1.0].
        """
        return 0.0 <= score <= 1.0
