"""
Budget Estimator Service
========================
Estimates runtime, hardware, energy, cost, and experiment counts for an autonomous goal.
"""

from research_validation.goal.models.goal import Goal, GoalType
from research_validation.goal.models.execution_budget import ExecutionBudget
from research_validation.goal.models.resource_budget import ResourceBudget


class BudgetEstimator:
    """
    Computes required computational budget allocations based on goal complexity and dataset counts.
    """

    @classmethod
    def estimate_budget(cls, goal: Goal) -> ExecutionBudget:
        """Estimates resource and execution budget."""
        dataset_count = max(1, len(goal.required_datasets))
        criteria_count = max(1, len(goal.success_metrics))

        # Base estimates depending on goal type
        if goal.goal_type == GoalType.OPTIMIZATION:
            exp_experiments = 20
            exp_runtime_hours = 4.0 * dataset_count
            gpu_hours = 2.0 * dataset_count if "GPU" in goal.required_compute else 0.0
            cpu_hours = 8.0 * dataset_count
            cost = 15.0 * dataset_count
        elif goal.goal_type == GoalType.BENCHMARK:
            exp_experiments = 5 * dataset_count
            exp_runtime_hours = 1.0 * dataset_count
            gpu_hours = 0.5 * dataset_count if "GPU" in goal.required_compute else 0.0
            cpu_hours = 4.0 * dataset_count
            cost = 5.0 * dataset_count
        elif goal.goal_type == GoalType.RESEARCH:
            exp_experiments = 10 * dataset_count
            exp_runtime_hours = 2.5 * dataset_count
            gpu_hours = 1.0 * dataset_count if "GPU" in goal.required_compute else 0.0
            cpu_hours = 6.0 * dataset_count
            cost = 10.0 * dataset_count
        else:
            exp_experiments = 2 * dataset_count
            exp_runtime_hours = 0.5 * dataset_count
            gpu_hours = 0.0
            cpu_hours = 2.0 * dataset_count
            cost = 2.0 * dataset_count

        res_budget = ResourceBudget(
            gpu_hours=gpu_hours,
            cpu_hours=cpu_hours,
            ram_gb=min(goal.constraints.max_ram_gb, 8.0 * dataset_count),
            storage_gb=min(goal.constraints.max_storage_gb, 5.0 * dataset_count),
            network_gb=1.0 * dataset_count,
            energy_kwh=0.5 * cpu_hours,
            cost_usd=min(goal.maximum_cost_usd, cost),
            api_calls_count=100 * exp_experiments,
        )

        return ExecutionBudget(
            expected_runtime_hours=min(goal.maximum_runtime_hours, exp_runtime_hours),
            maximum_runtime_hours=goal.maximum_runtime_hours,
            expected_iterations=min(goal.maximum_iterations, exp_experiments),
            maximum_iterations=goal.maximum_iterations,
            expected_experiments_count=exp_experiments,
            retry_budget=goal.constraints.max_retries,
            resource_budget=res_budget,
            confidence_target=goal.confidence_threshold.value,
        )
