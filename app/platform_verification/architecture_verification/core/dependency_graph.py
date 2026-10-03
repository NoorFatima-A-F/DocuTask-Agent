"""
Dependency Graph Engine with Tarjan cycle detection.
"""
from __future__ import annotations
from typing import Dict, List, Set
from app.platform_verification.architecture_verification.domain.interfaces import IDependencyGraphEngine
from app.platform_verification.architecture_verification.domain.models import (
    ArchitectureDependency,
    CircularDependencyCycle,
    RuleSeverity,
)


class EnterpriseDependencyGraphEngine(IDependencyGraphEngine):
    """Builds dependency adjacency graphs and detects circular references."""

    def build_graph(self, dependencies: List[ArchitectureDependency]) -> Dict[str, List[str]]:
        graph: Dict[str, List[str]] = {}
        for dep in dependencies:
            if not dep.target_module:
                continue
            if dep.source_module not in graph:
                graph[dep.source_module] = []
            if dep.target_module not in graph[dep.source_module]:
                graph[dep.source_module].append(dep.target_module)
        return graph

    def detect_circular_dependencies(self, graph: Dict[str, List[str]]) -> List[CircularDependencyCycle]:
        """Detects simple cycles using depth-first search cycle finding."""
        cycles: List[CircularDependencyCycle] = []
        visited: Set[str] = set()
        rec_stack: List[str] = []
        found_cycle_tuples: Set[Tuple[str, ...]] = set()

        def dfs(node: str):
            visited.add(node)
            rec_stack.append(node)

            for neighbor in graph.get(node, []):
                # Only check internal project modules
                if not neighbor.startswith("app.") and not neighbor.startswith("tests."):
                    continue

                if neighbor not in visited:
                    dfs(neighbor)
                elif neighbor in rec_stack:
                    # Cycle detected
                    idx = rec_stack.index(neighbor)
                    cycle_nodes = rec_stack[idx:] + [neighbor]
                    canonical = tuple(cycle_nodes[:-1])
                    if canonical not in found_cycle_tuples:
                        found_cycle_tuples.add(canonical)
                        cycles.append(
                            CircularDependencyCycle(
                                cycle_path=cycle_nodes,
                                severity=RuleSeverity.CRITICAL,
                                description=f"Circular dependency detected: {' -> '.join(cycle_nodes)}",
                            )
                        )

            rec_stack.pop()

        for node in list(graph.keys()):
            if node not in visited and (node.startswith("app.") or node.startswith("tests.")):
                dfs(node)

        return cycles
