"""
Goal Validator Service
======================
Enforces strict scientific validation rules, rejecting underspecified,
unmeasurable, or contradictory goals with machine-readable error reasons.
"""

from dataclasses import dataclass, field
from typing import List, Tuple
from research_validation.goal.models.goal import Goal
from research_validation.goal.models.confidence_threshold import ConfidenceLevel
from research_validation.goal.services.dependency_analyzer import DependencyAnalyzer
from research_validation.goal.exceptions import GoalValidationError


@dataclass(frozen=True)
class GoalValidationResult:
    """Detailed machine-readable validation report."""
    is_valid: bool
    goal_id: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class GoalValidator:
    """
    Validates goals against scientific measurability, governance, and resource constraints.
    """

    @classmethod
    def validate_goal(cls, goal: Goal) -> GoalValidationResult:
        errors: List[str] = []
        warnings: List[str] = []

        # 1. Measurable Outcomes & Success Criteria
        if not goal.success_metrics:
            errors.append("Goal lacks measurable outcomes (success_metrics cannot be empty).")

        # 2. Stopping Conditions
        if not goal.stopping_conditions:
            errors.append("Goal lacks stopping conditions (stopping_conditions cannot be empty).")

        # 3. Confidence Threshold validity
        if goal.confidence_threshold.level == ConfidenceLevel.CUSTOM:
            if (
                goal.confidence_threshold.custom_numeric_value is None
                or not (0.0 < goal.confidence_threshold.custom_numeric_value <= 1.0)
            ):
                errors.append("Custom confidence threshold must be a float between 0.0 (exclusive) and 1.0.")

        # 4. Circular Dependencies
        if goal.dependencies:
            nodes = list(set([d.source_id for d in goal.dependencies] + [d.target_id for d in goal.dependencies]))
            dep_res = DependencyAnalyzer.analyze_dependencies(nodes, list(goal.dependencies))
            if not dep_res.is_valid:
                errors.append(f"Circular dependency detected in goal dependencies: {dep_res.detected_cycles}")

        # 5. Resource and Budget Limits
        if goal.maximum_runtime_hours <= 0:
            errors.append("Maximum runtime hours must be strictly positive.")
        if goal.maximum_cost_usd <= 0:
            errors.append("Maximum cost USD must be strictly positive.")
        if goal.maximum_iterations <= 0:
            errors.append("Maximum iterations must be strictly positive.")

        # 6. Contradictory Objectives
        if "REDUCE_LATENCY_TO_ZERO" in goal.objective.upper() and "MAXIMIZE_ACCURACY" in goal.objective.upper():
            warnings.append("Objective mentions zero latency with maximum accuracy; verify Pareto feasibility.")

        # 7. Governance and Privacy Violations
        if "PII_UNMASKED_ALLOW" in goal.governance_policies:
            errors.append("Zero-PII / Data Minimization policy violation: PII_UNMASKED_ALLOW is forbidden.")

        return GoalValidationResult(
            is_valid=(len(errors) == 0),
            goal_id=goal.goal_id,
            errors=errors,
            warnings=warnings,
        )
