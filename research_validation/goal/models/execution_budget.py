"""
Execution Budget Model
======================
Specifies execution limits, iterations, retry counts, and estimated experiment counts.
"""

from dataclasses import dataclass, field
from typing import Optional
from research_validation.goal.models.resource_budget import ResourceBudget


@dataclass(frozen=True)
class ExecutionBudget:
    """Full execution budget encompassing runtime limits, iterations, and hardware allocations."""
    expected_runtime_hours: float
    maximum_runtime_hours: float
    expected_iterations: int
    maximum_iterations: int
    expected_experiments_count: int
    retry_budget: int
    resource_budget: ResourceBudget
    confidence_target: float = 0.95
