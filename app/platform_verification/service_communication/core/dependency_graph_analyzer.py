"""
Service Dependency Graph & Topology Analyzer.
"""
from typing import Dict, List, Set
from app.platform_verification.service_communication.domain.models import (
    ServiceDependencyGraph,
    DependencyAnalysisReport,
)
from app.platform_verification.service_communication.domain.interfaces import IDependencyGraphAnalyzer


class DependencyGraphAnalyzer(IDependencyGraphAnalyzer):
    """Maps communication graph, detects cycles and excessive coupling."""

    def analyze_dependencies(self, graph: ServiceDependencyGraph) -> DependencyAnalysisReport:
        total_services = len(graph.nodes)
        cycles = self._find_cycles(graph)
        spofs: List[str] = []
        critical_paths: List[str] = []

        total_edges = 0
        incoming_counts: Dict[str, int] = {name: 0 for name in graph.nodes}

        for name, node in graph.nodes.items():
            total_edges += len(node.depends_on)
            if node.is_critical_path:
                critical_paths.append(name)
            for dep in node.depends_on:
                if dep in incoming_counts:
                    incoming_counts[dep] += 1

        for name, count in incoming_counts.items():
            if count >= max(2, total_services - 1) and name in ["database", "postgres", "redis", "gateway"]:
                spofs.append(name)

        complexity = total_edges / max(total_services * 1.5, 1)
        complexity_score = max(0.0, 100.0 - (complexity * 25.0) - (len(cycles) * 40.0))
        complexity_score = round(min(100.0, complexity_score), 2)

        status = "PASS" if len(cycles) == 0 else "FAIL"

        return DependencyAnalysisReport(
            total_services=total_services,
            dependency_complexity_score=complexity_score,
            critical_path_services=critical_paths,
            circular_dependencies=cycles,
            single_points_of_failure=spofs,
            status=status,
        )

    def _find_cycles(self, graph: ServiceDependencyGraph) -> List[List[str]]:
        cycles: List[List[str]] = []
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node: str, path: List[str]):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            if node in graph.nodes:
                for neighbor in graph.nodes[node].depends_on:
                    if neighbor not in visited:
                        dfs(neighbor, list(path))
                    elif neighbor in rec_stack:
                        cycle_idx = path.index(neighbor)
                        cycles.append(path[cycle_idx:] + [neighbor])

            rec_stack.remove(node)

        for name in graph.nodes:
            if name not in visited:
                dfs(name, [])

        return cycles
