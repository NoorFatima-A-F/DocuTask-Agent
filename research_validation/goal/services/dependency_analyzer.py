"""
Dependency Analyzer Service
===========================
Infers dependencies across goals, tasks, datasets, tools, and models; detects circular dependency cycles.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

from research_validation.goal.models.dependency import GoalDependency, DependencyType
from research_validation.goal.exceptions import CircularDependencyError


@dataclass(frozen=True)
class DependencyAnalysisResult:
    """Consolidated outcome of dependency graph evaluation."""
    is_valid: bool
    total_dependencies_count: int
    topological_order: List[str]
    detected_cycles: List[List[str]] = field(default_factory=list)
    diagnostic: str = ""


class DependencyAnalyzer:
    """
    Builds and analyzes dependency graphs for goals and missions.
    """

    @classmethod
    def analyze_dependencies(
        cls,
        nodes: List[str],
        dependencies: List[GoalDependency],
    ) -> DependencyAnalysisResult:
        """Evaluates acyclicity and computes topological ordering."""
        adj: Dict[str, Set[str]] = {n: set() for n in nodes}
        in_degree: Dict[str, int] = {n: 0 for n in nodes}

        for dep in dependencies:
            if dep.source_id in adj and dep.target_id in adj:
                adj[dep.source_id].add(dep.target_id)

        for u in adj:
            for v in adj[u]:
                in_degree[v] += 1

        # Kahn's algorithm for topological sorting and cycle detection
        queue = [n for n in nodes if in_degree[n] == 0]
        order: List[str] = []

        while queue:
            u = queue.pop(0)
            order.append(u)
            for v in adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(order) != len(nodes):
            # Cycle exists
            cycles = cls._find_cycles(nodes, adj)
            return DependencyAnalysisResult(
                is_valid=False,
                total_dependencies_count=len(dependencies),
                topological_order=[],
                detected_cycles=cycles,
                diagnostic=f"Circular dependency detected in graph: {cycles}",
            )

        return DependencyAnalysisResult(
            is_valid=True,
            total_dependencies_count=len(dependencies),
            topological_order=order,
            detected_cycles=[],
            diagnostic="Dependency graph is acyclic and valid.",
        )

    @classmethod
    def _find_cycles(cls, nodes: List[str], adj: Dict[str, Set[str]]) -> List[List[str]]:
        visited: Dict[str, int] = {n: 0 for n in nodes}
        stack: List[str] = []
        cycles: List[List[str]] = []

        def dfs(u: str):
            visited[u] = 1
            stack.append(u)
            for v in adj.get(u, set()):
                if visited[v] == 1:
                    idx = stack.index(v)
                    cycles.append(stack[idx:] + [v])
                elif visited[v] == 0:
                    dfs(v)
            stack.pop()
            visited[u] = 2

        for n in nodes:
            if visited[n] == 0:
                dfs(n)
        return cycles
