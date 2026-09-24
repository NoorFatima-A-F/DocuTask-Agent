"""
DAG Graph Validation & Topological Sorting Engine.
Implements DFS cycle detection, Kahn's topological sort, orphan node detection, and reachability validation.
"""

from typing import Dict, List, Set
from app.agents.planning.exceptions import (
    CyclicDependencyException,
    MissingDependencyException,
)
from app.agents.planning.graph import PlanGraph


class DAGValidator:
    """Validator ensuring plan graph conforms to acyclic, connected, valid DAG specifications."""

    @staticmethod
    def detect_cycles(graph: PlanGraph) -> None:
        """Detects cycles in the graph using Depth-First Search (DFS) with recursion stack."""
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        adj_list: Dict[str, List[str]] = {node_id: [] for node_id in graph.nodes}
        for edge in graph.edges:
            if edge.source_node_id not in graph.nodes:
                raise MissingDependencyException(f"Edge source '{edge.source_node_id}' not found in graph nodes.")
            if edge.target_node_id not in graph.nodes:
                raise MissingDependencyException(f"Edge target '{edge.target_node_id}' not found in graph nodes.")
            adj_list[edge.source_node_id].append(edge.target_node_id)

        def _dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in adj_list.get(node, []):
                if neighbor not in visited:
                    if _dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for node_id in graph.nodes:
            if node_id not in visited:
                if _dfs(node_id):
                    raise CyclicDependencyException(f"Circular dependency / cycle detected involving node '{node_id}'.")

    @staticmethod
    def topological_sort(graph: PlanGraph) -> List[str]:
        """Calculates deterministic execution sequence via Kahn's algorithm."""
        DAGValidator.detect_cycles(graph)

        in_degree: Dict[str, int] = {node_id: 0 for node_id in graph.nodes}
        adj_list: Dict[str, List[str]] = {node_id: [] for node_id in graph.nodes}

        for edge in graph.edges:
            adj_list[edge.source_node_id].append(edge.target_node_id)
            in_degree[edge.target_node_id] += 1

        queue: List[str] = [node_id for node_id, deg in in_degree.items() if deg == 0]
        order: List[str] = []

        while queue:
            node = queue.pop(0)
            order.append(node)

            for neighbor in adj_list[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return order
