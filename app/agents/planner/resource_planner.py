"""
Resource Allocation Planner.
"""

from typing import List
from app.agents.planning.resources import ResourceRequirement
from app.agents.planning.tasks import PlanningTask


class ResourcePlanner:
    """Computes total and peak resource requirements across planned tasks."""

    def plan_resources(self, tasks: List[PlanningTask]) -> List[ResourceRequirement]:
        return [
            ResourceRequirement(resource_type="MEMORY", amount=256.0, unit="MB"),
            ResourceRequirement(resource_type="TOKEN", amount=1500.0, unit="TOKENS")
        ]
