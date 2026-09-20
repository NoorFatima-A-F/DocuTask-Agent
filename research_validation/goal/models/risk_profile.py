"""
Risk Profile Model
==================
Evaluates multidimensional risk vectors across 9 scientific and operational categories.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional


class RiskSeverity(str, Enum):
    NEGLIGIBLE = "NEGLIGIBLE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class RiskItem:
    """A specific evaluated risk item."""
    category: str  # "TECHNICAL", "SCIENTIFIC", "STATISTICAL", "GOVERNANCE", "PRIVACY", "EXECUTION", "RESOURCE", "DEPENDENCY", "OPERATIONAL"
    description: str
    likelihood: float  # 0.0 to 1.0
    impact: float      # 0.0 to 1.0
    severity: RiskSeverity
    mitigation_strategy: str
    is_blocking: bool = False

    @property
    def risk_magnitude(self) -> float:
        return self.likelihood * self.impact


@dataclass(frozen=True)
class RiskProfile:
    """Multidimensional risk profile encompassing all 9 risk vectors."""
    overall_risk_score: float  # 0.0 to 1.0
    severity: RiskSeverity
    risk_items: List[RiskItem] = field(default_factory=list)
    has_blocking_risks: bool = False
    approved_mitigations_count: int = 0
    diagnostic: str = ""
