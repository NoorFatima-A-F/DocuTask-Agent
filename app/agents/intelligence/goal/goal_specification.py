"""Enterprise Goal Specification Domain Models.

Represents fully validated and structured goal representations parsed from natural
language or machine inputs for autonomous execution.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional


class GoalPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class GoalStatus(str, Enum):
    PENDING = "PENDING"
    ANALYZING = "ANALYZING"
    READY = "READY"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


@dataclass
class SuccessCriteria:
    """Quantitative and qualitative criteria for evaluating goal completion."""

    metric_name: str
    target_value: float
    comparison_operator: str = ">="  # ">=", "<=", "==", "!="
    weight: float = 1.0
    is_mandatory: bool = True
    actual_value: Optional[float] = None

    def evaluate(self, actual: float) -> bool:
        self.actual_value = actual
        if self.comparison_operator == ">=":
            return actual >= self.target_value
        elif self.comparison_operator == "<=":
            return actual <= self.target_value
        elif self.comparison_operator == "==":
            return abs(actual - self.target_value) < 1e-6
        elif self.comparison_operator == "!=":
            return abs(actual - self.target_value) >= 1e-6
        return False


@dataclass
class GoalSpecification:
    """Full enterprise goal specification."""

    objective: str
    goal_id: str = field(default_factory=lambda: f"goal_{uuid.uuid4().hex[:12]}")
    intent: str = "GENERIC_TASK"
    domain: str = "DOCUMENT_PROCESSING"
    priority: GoalPriority = GoalPriority.MEDIUM
    risk_level: RiskLevel = RiskLevel.LOW
    status: GoalStatus = GoalStatus.PENDING
    input_requirements: Dict[str, Any] = field(default_factory=dict)
    expected_output: Dict[str, Any] = field(default_factory=dict)
    constraints: Dict[str, Any] = field(default_factory=dict)
    success_criteria: List[SuccessCriteria] = field(default_factory=list)
    confidence_score: float = 1.0
    sla_seconds: Optional[float] = None
    deadline: Optional[datetime] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_ambiguous(self) -> bool:
        """Determines if goal specification lacks minimum required precision."""
        if not self.objective or len(self.objective.strip()) < 5:
            return True
        if self.confidence_score < 0.60:
            return True
        return False

    def add_criterion(self, metric: str, target: float, op: str = ">=", weight: float = 1.0, mandatory: bool = True) -> None:
        self.success_criteria.append(SuccessCriteria(
            metric_name=metric,
            target_value=target,
            comparison_operator=op,
            weight=weight,
            is_mandatory=mandatory
        ))

    def evaluate_success(self, metrics: Dict[str, float]) -> tuple[bool, float]:
        """Evaluates metrics against success criteria, returns (passed, overall_score)."""
        if not self.success_criteria:
            return True, 1.0

        total_weight = 0.0
        achieved_weight = 0.0
        mandatory_passed = True

        for sc in self.success_criteria:
            val = metrics.get(sc.metric_name, 0.0)
            passed = sc.evaluate(val)
            if sc.is_mandatory and not passed:
                mandatory_passed = False
            total_weight += sc.weight
            if passed:
                achieved_weight += sc.weight

        score = (achieved_weight / total_weight) if total_weight > 0 else 1.0
        return (mandatory_passed and score >= 0.8), score
