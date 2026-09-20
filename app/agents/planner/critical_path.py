"""
Critical Path Analysis Planner.
"""

from typing import List
from app.agents.planning.graph import PlanGraph
from app.agents.planning.sequencing import CriticalPathCalculator, TaskSequence


class CriticalPathPlanner:
    """Calculates critical path for planned graph."""

    def compute_critical_path(self, graph: PlanGraph, topological_order: List[str]) -> TaskSequence:
        return CriticalPathCalculator.calculate_critical_path(graph, topological_order)
