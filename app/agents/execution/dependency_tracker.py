"""
Runtime Dependency Tracker.
Evaluates predecessor node completion, barrier synchronization, and execution eligibility.
"""

from typing import List, Set
from app.agents.execution.execution_graph import ExecutionGraph
from app.agents.execution.lifecycle import ExecutionLifecycleState


class DependencyTracker:
    """Continuous dependency evaluator determining runnable nodes in the execution graph."""

    def __init__(self, execution_graph: ExecutionGraph):
        self.graph = execution_graph

    def is_node_ready(self, node_id: str) -> bool:
        """Evaluates whether all predecessor nodes of given node have reached COMPLETED state."""
        node = self.graph.get_node(node_id)
        if not node:
            return False

        if node.state not in (ExecutionLifecycleState.CREATED, ExecutionLifecycleState.WAITING):
            return False

        incoming = self.graph.get_incoming_edges(node_id)
        if not incoming:
            return True

        # Check all incoming sources
        for edge in incoming:
            pred = self.graph.get_node(edge.source_node_id)
            if not pred or pred.state != ExecutionLifecycleState.COMPLETED:
                return False

        return True

    def get_runnable_nodes(self) -> List[str]:
        """Identifies all currently runnable nodes whose dependencies are fully satisfied."""
        runnable: List[str] = []
        for node_id, node in self.graph.nodes.items():
            if node.state in (ExecutionLifecycleState.CREATED, ExecutionLifecycleState.WAITING):
                if self.is_node_ready(node_id):
                    runnable.append(node_id)
        return runnable

    def has_pending_work(self) -> bool:
        """Returns True if any nodes are still waiting, scheduled, or running."""
        for node in self.graph.nodes.values():
            if node.state in (
                ExecutionLifecycleState.CREATED,
                ExecutionLifecycleState.WAITING,
                ExecutionLifecycleState.READY,
                ExecutionLifecycleState.SCHEDULED,
                ExecutionLifecycleState.RUNNING,
                ExecutionLifecycleState.RETRYING
            ):
                return True
        return False

    def is_execution_completed(self) -> bool:
        """Returns True if all nodes in the graph have reached terminal states."""
        terminal_states: Set[ExecutionLifecycleState] = {
            ExecutionLifecycleState.COMPLETED,
            ExecutionLifecycleState.FAILED,
            ExecutionLifecycleState.CANCELLED,
            ExecutionLifecycleState.ROLLED_BACK
        }
        return all(node.state in terminal_states for node in self.graph.nodes.values())
