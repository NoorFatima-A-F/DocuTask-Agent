"""
Domain Model Validation Guards & Cycle Detectors.
Provides fast validation for goals, tasks, workflow graphs, and task dependency DAGs.
"""

from typing import Dict, List, Set
from app.agents.exceptions import AgentException
from app.agents.domain.goals import Goal
from app.agents.domain.tasks import AgentTask
from app.agents.domain.workflows import WorkflowGraph


class DomainValidationException(AgentException):
    """Raised when domain validation rules are violated."""
    pass


class DomainValidator:
    """Domain validation helper functions."""

    @staticmethod
    def validate_goal(goal: Goal) -> None:
        """Validates Goal aggregate integrity."""
        if not goal.statement or not goal.statement.strip():
            raise DomainValidationException("Goal statement cannot be empty.")

    @staticmethod
    def validate_workflow_graph(graph: WorkflowGraph) -> None:
        """
        Validates WorkflowGraph DAG topology.
        Detects duplicate node IDs, unknown edge references, and circular dependencies (cycles).
        """
        node_ids: Set[str] = set(graph.nodes.keys())

        # Check edge endpoints exist in graph nodes
        for edge in graph.edges:
            if edge.source_node_id not in node_ids:
                raise DomainValidationException(f"Edge source node '{edge.source_node_id}' not found in workflow graph.")
            if edge.target_node_id not in node_ids:
                raise DomainValidationException(f"Edge target node '{edge.target_node_id}' not found in workflow graph.")

        # Cycle Detection via Depth-First Search (DFS)
        adjacency: Dict[str, List[str]] = {node_id: [] for node_id in node_ids}
        for edge in graph.edges:
            adjacency[edge.source_node_id].append(edge.target_node_id)

        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)

            for neighbor in adjacency.get(node_id, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True  # Cycle detected

            rec_stack.remove(node_id)
            return False

        for node_id in node_ids:
            if node_id not in visited:
                if dfs(node_id):
                    raise DomainValidationException("Circular dependency cycle detected in workflow graph DAG topology.")
