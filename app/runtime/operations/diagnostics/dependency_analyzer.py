"""
AOIS-HROP Phase 13.7 - Dependency Analyzer
Analyzes dependency topologies to identify primary failure sources vs secondary symptoms.
"""

from typing import Dict, List, Set


class DependencyAnalyzer:
    """
    Separates root cause originators from symptom cascades across subsystem dependencies.
    """

    def __init__(self):
        self._upstream_map: Dict[str, List[str]] = {
            "API": ["PLANNER", "DATABASE"],
            "PLANNER": ["WORKERS", "OPTIMIZATION", "MEMORY"],
            "WORKERS": ["DATABASE", "TELEMETRY"],
            "OPTIMIZATION": ["TELEMETRY", "LEARNING"],
            "REPLAY": ["TRUTH", "TELEMETRY"],
            "LEARNING": ["TRUTH", "REPLAY"],
            "TRUTH": ["DATABASE"],
            "TELEMETRY": ["DATABASE"],
            "MEMORY": ["DATABASE"],
            "DATABASE": [],
        }

    def trace_root_culprit(self, anomalous_subsystems: List[str]) -> str:
        if not anomalous_subsystems:
            return "UNKNOWN"
        if len(anomalous_subsystems) == 1:
            return anomalous_subsystems[0]

        # Find the node that has the fewest dependencies among anomalous subsystems
        # i.e., deepest in the dependency stack (closest to DATABASE)
        scores: Dict[str, int] = {}
        for sub in anomalous_subsystems:
            # Score is depth in dependency graph
            deps = self._get_transitive_deps(sub)
            anom_deps = [d for d in deps if d in anomalous_subsystems]
            scores[sub] = len(anom_deps)

        # The node with the least anomalous dependencies is the root originator
        sorted_nodes = sorted(scores.items(), key=lambda x: x[1])
        return sorted_nodes[0][0]

    def _get_transitive_deps(self, node: str) -> Set[str]:
        visited: Set[str] = set()
        queue = [node]
        while queue:
            curr = queue.pop(0)
            for dep in self._upstream_map.get(curr, []):
                if dep not in visited:
                    visited.add(dep)
                    queue.append(dep)
        return visited
