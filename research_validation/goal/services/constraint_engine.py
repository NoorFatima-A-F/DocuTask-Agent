"""
Constraint Engine Service
=========================
Evaluates proposed goals and resource requests against hard limits and policy restrictions.
"""

from typing import List, Tuple
from research_validation.goal.models.goal_constraints import GoalConstraints
from research_validation.goal.models.execution_budget import ExecutionBudget
from research_validation.goal.exceptions import BudgetExceededError


class ConstraintEngine:
    """Validates that requested resources and configurations respect constraints."""

    @classmethod
    def validate_budget_against_constraints(
        cls,
        budget: ExecutionBudget,
        constraints: GoalConstraints,
    ) -> Tuple[bool, List[str]]:
        """Verifies if the estimated budget fits inside the defined constraints."""
        violations: List[str] = []

        if budget.expected_runtime_hours > constraints.max_runtime_hours:
            violations.append(
                f"Expected runtime {budget.expected_runtime_hours:.1f}h exceeds max {constraints.max_runtime_hours:.1f}h"
            )

        if budget.resource_budget.gpu_hours > constraints.max_gpu_hours:
            violations.append(
                f"Estimated GPU hours {budget.resource_budget.gpu_hours:.1f} exceeds limit {constraints.max_gpu_hours:.1f}"
            )

        if budget.resource_budget.cpu_hours > constraints.max_cpu_hours:
            violations.append(
                f"Estimated CPU hours {budget.resource_budget.cpu_hours:.1f} exceeds limit {constraints.max_cpu_hours:.1f}"
            )

        if budget.resource_budget.ram_gb > constraints.max_ram_gb:
            violations.append(
                f"Estimated RAM {budget.resource_budget.ram_gb:.1f}GB exceeds limit {constraints.max_ram_gb:.1f}GB"
            )

        if budget.resource_budget.storage_gb > constraints.max_storage_gb:
            violations.append(
                f"Estimated Storage {budget.resource_budget.storage_gb:.1f}GB exceeds limit {constraints.max_storage_gb:.1f}GB"
            )

        if budget.resource_budget.cost_usd > constraints.max_cost_usd:
            violations.append(
                f"Estimated Cost ${budget.resource_budget.cost_usd:.2f} exceeds limit ${constraints.max_cost_usd:.2f}"
            )

        return (len(violations) == 0), violations
