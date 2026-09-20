"""
Stopping Condition Model
========================
Defines formal, machine-evaluable stopping conditions for autonomous missions.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


class StoppingConditionType(str, Enum):
    GOAL_ACHIEVED = "GOAL_ACHIEVED"
    CONFIDENCE_REACHED = "CONFIDENCE_REACHED"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    RUNTIME_EXHAUSTED = "RUNTIME_EXHAUSTED"
    MAX_ITERATIONS = "MAX_ITERATIONS"
    GOVERNANCE_FAILURE = "GOVERNANCE_FAILURE"
    HUMAN_APPROVAL_REQUIRED = "HUMAN_APPROVAL_REQUIRED"
    DATASET_MISSING = "DATASET_MISSING"
    EVIDENCE_INSUFFICIENT = "EVIDENCE_INSUFFICIENT"
    CONTRADICTION_DETECTED = "CONTRADICTION_DETECTED"
    CRITICAL_REGRESSION = "CRITICAL_REGRESSION"
    EXTERNAL_CANCELLATION = "EXTERNAL_CANCELLATION"


@dataclass(frozen=True)
class StoppingCondition:
    """Immutable stopping condition definition."""
    condition_type: StoppingConditionType
    description: str
    is_terminal: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)
