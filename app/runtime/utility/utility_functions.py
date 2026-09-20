"""
Scientific Utility Engine - Utility Functions
Defines risk-neutral, risk-averse, concave, and multi-attribute utility transformations.
"""

import math
from typing import Dict, Any, Callable
from enum import Enum


class RiskProfile(str, Enum):
    RISK_NEUTRAL = "risk_neutral"
    RISK_AVERSE = "risk_averse"
    RISK_SEEKING = "risk_seeking"
    STRICT_ENTERPRISE = "strict_enterprise"


class UtilityFunctions:
    """Mathematical utility functions mapping raw metrics to utility payoffs U in [0, 1]."""

    @staticmethod
    def linear_utility(val: float, is_cost: bool = False) -> float:
        """Linear mapping U(x) = x for benefits, U(x) = 1 - x for costs."""
        clamped = max(0.0, min(1.0, float(val)))
        return 1.0 - clamped if is_cost else clamped

    @staticmethod
    def exponential_utility(val: float, risk_aversion_lambda: float = 2.0, is_cost: bool = False) -> float:
        """Concave exponential utility U(x) = (1 - exp(-lambda * x)) / (1 - exp(-lambda)).
        Expresses diminishing marginal returns and strong risk aversion.
        """
        clamped = max(0.0, min(1.0, float(val)))
        x = 1.0 - clamped if is_cost else clamped

        if abs(risk_aversion_lambda) < 1e-6:
            return x

        denom = 1.0 - math.exp(-risk_aversion_lambda)
        if abs(denom) < 1e-9:
            return x
        return (1.0 - math.exp(-risk_aversion_lambda * x)) / denom

    @staticmethod
    def s_curve_utility(val: float, midpoint: float = 0.5, steepness: float = 10.0, is_cost: bool = False) -> float:
        """Sigmoidal threshold utility for SLA and compliance constraints."""
        clamped = max(0.0, min(1.0, float(val)))
        x = 1.0 - clamped if is_cost else clamped
        z = steepness * (x - midpoint)
        return 1.0 / (1.0 + math.exp(-z))
