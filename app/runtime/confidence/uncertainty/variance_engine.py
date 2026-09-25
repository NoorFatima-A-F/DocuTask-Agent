"""
Variance Engine for Phase 13.3 (ASCE-CGP).
Calculates sample variance across parallel worker execution signals.
"""

from typing import List


class VarianceEngine:
    """
    Computes sample and population variance across worker confidence outputs.
    """

    @classmethod
    def compute_variance(cls, values: List[float]) -> float:
        if not values or len(values) < 2:
            return 0.002

        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return round(variance, 6)
