"""
AOIS-HROP Phase 13.7 - Dependency Health Graph
Graph-based dependency health propagation across subsystems to model cascading failure risks.
"""

from typing import Dict, List, Set
from app.runtime.operations.events.operation_events import SubsystemType


class DependencyHealthGraph:
    """
    Models causal topology and simulates upstream-downstream health propagation.
    """

    def __init__(self):
        # downstream -> upstream dependencies
        self._adjacency: Dict[str, List[str]] = {
            SubsystemType.API.value: [SubsystemType.PLANNER.value, SubsystemType.DATABASE.value],
            SubsystemType.PLANNER.value: [SubsystemType.WORKERS.value, SubsystemType.OPTIMIZATION.value, SubsystemType.MEMORY.value],
            SubsystemType.WORKERS.value: [SubsystemType.DATABASE.value, SubsystemType.TELEMETRY.value],
            SubsystemType.OPTIMIZATION.value: [SubsystemType.TELEMETRY.value, SubsystemType.LEARNING.value],
            SubsystemType.REPLAY.value: [SubsystemType.TRUTH.value, SubsystemType.TELEMETRY.value],
            SubsystemType.LEARNING.value: [SubsystemType.TRUTH.value, SubsystemType.REPLAY.value],
            SubsystemType.TRUTH.value: [SubsystemType.DATABASE.value],
            SubsystemType.TELEMETRY.value: [SubsystemType.DATABASE.value],
            SubsystemType.MEMORY.value: [SubsystemType.DATABASE.value],
            SubsystemType.DATABASE.value: [],
        }

    def get_dependencies(self, subsystem: str) -> List[str]:
        return self._adjacency.get(subsystem, [])

    def get_dependents(self, subsystem: str) -> List[str]:
        dependents = []
        for node, deps in self._adjacency.items():
            if subsystem in deps:
                dependents.append(node)
        return dependents

    def calculate_propagated_impact(self, degraded_subsystem: str, initial_score: float) -> Dict[str, float]:
        """
        Calculates how degradation in one subsystem degrades downstream dependent subsystems.
        """
        impacts: Dict[str, float] = {degraded_subsystem: initial_score}
        queue = [degraded_subsystem]
        visited: Set[str] = set()

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            current_score = impacts[current]

            for dependent in self.get_dependents(current):
                # Downstream degradation factor
                damped_score = max(0.0, min(100.0, 100.0 - (100.0 - current_score) * 0.65))
                if dependent not in impacts or impacts[dependent] > damped_score:
                    impacts[dependent] = round(damped_score, 2)
                    queue.append(dependent)

        return impacts
