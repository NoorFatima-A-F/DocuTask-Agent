"""
Success Criteria Model
======================
Defines measurable, statistically testable criteria for goal achievement.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


class Comparator(str, Enum):
    GREATER_THAN = ">"
    GREATER_THAN_OR_EQUAL = ">="
    LESS_THAN = "<"
    LESS_THAN_OR_EQUAL = "<="
    EQUAL = "=="
    NOT_EQUAL = "!="
    WITHIN_RANGE = "WITHIN_RANGE"


@dataclass(frozen=True)
class SuccessCriterion:
    """A single measurable criterion required for goal fulfillment."""
    metric_name: str
    comparator: Comparator
    target_value: float
    tolerance: float = 0.0
    confidence_requirement: float = 0.95
    minimum_sample_size: int = 30
    statistical_test: str = "WILCOXON_OR_BOOTSTRAP"
    evidence_required: bool = True
    independent_verification_required: bool = False
    blocking: bool = True
    weight: float = 1.0

    def evaluate(self, measured_value: float) -> bool:
        """Evaluates whether a measured metric satisfies this criterion."""
        if self.comparator == Comparator.GREATER_THAN:
            return measured_value > (self.target_value - self.tolerance)
        elif self.comparator == Comparator.GREATER_THAN_OR_EQUAL:
            return measured_value >= (self.target_value - self.tolerance)
        elif self.comparator == Comparator.LESS_THAN:
            return measured_value < (self.target_value + self.tolerance)
        elif self.comparator == Comparator.LESS_THAN_OR_EQUAL:
            return measured_value <= (self.target_value + self.tolerance)
        elif self.comparator == Comparator.EQUAL:
            return abs(measured_value - self.target_value) <= self.tolerance
        elif self.comparator == Comparator.NOT_EQUAL:
            return abs(measured_value - self.target_value) > self.tolerance
        return False
