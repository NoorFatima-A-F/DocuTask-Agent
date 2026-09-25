"""
Parallelization and Concurrency Optimization Engine.
Identifies tasks with disjoint dependencies to maximize parallel execution throughput.
"""

from typing import List
from app.agents.planning.tasks import PlanningTask


class ParallelizationOptimizer:
    """Identifies and clusters parallel execution groups."""

    def find_independent_task_groups(self, tasks: List[PlanningTask]) -> List[List[str]]:
        independent: List[str] = [t.task_id for t in tasks if not t.dependencies]
        dependent: List[str] = [t.task_id for t in tasks if t.dependencies]
        return [independent, dependent] if independent else [dependent]
