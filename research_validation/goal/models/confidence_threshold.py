"""
Confidence Threshold Model
==========================
Defines formal confidence levels and their numeric mappings for scientific goal gating.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Optional


class ConfidenceLevel(str, Enum):
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"
    CUSTOM = "CUSTOM"


CONFIDENCE_NUMERIC_MAP = {
    ConfidenceLevel.VERY_LOW: 0.30,
    ConfidenceLevel.LOW: 0.50,
    ConfidenceLevel.MEDIUM: 0.70,
    ConfidenceLevel.HIGH: 0.90,
    ConfidenceLevel.VERY_HIGH: 0.99,
}


@dataclass(frozen=True)
class ConfidenceThreshold:
    """Immutable confidence threshold specification."""
    level: ConfidenceLevel
    custom_numeric_value: Optional[float] = None

    @property
    def value(self) -> float:
        """Returns effective numeric confidence threshold (0.0 to 1.0)."""
        if self.level == ConfidenceLevel.CUSTOM:
            if self.custom_numeric_value is None or not (0.0 <= self.custom_numeric_value <= 1.0):
                raise ValueError("Custom confidence threshold must provide a float between 0.0 and 1.0")
            return self.custom_numeric_value
        return CONFIDENCE_NUMERIC_MAP[self.level]

    def is_satisfied_by(self, empirical_confidence: float) -> bool:
        """Verifies if an empirical confidence score meets this threshold."""
        return empirical_confidence >= self.value
