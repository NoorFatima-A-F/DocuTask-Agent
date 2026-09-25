"""
Runtime Recovery Engine.
Implements recovery strategies: retry task, retry subtree, alternate tool, checkpoint restore.
"""

from uuid import UUID
from app.agents.execution.checkpoint_manager import CheckpointManager
from app.agents.execution.execution_graph import ExecutionGraph
from app.agents.execution.execution_state_machine import ExecutionStateMachine
from app.agents.execution.lifecycle import ExecutionLifecycleState


class RecoveryEngine:
    """Coordinates fault recovery mechanisms upon node failure."""

    def __init__(self, execution_graph: ExecutionGraph, checkpoint_manager: CheckpointManager):
        self.graph = execution_graph
        self.checkpoint_manager = checkpoint_manager

    def reset_node_for_retry(self, node_id: str) -> bool:
        """Resets a failed node to RETRYING then READY for scheduler re-entry."""
        node = self.graph.get_node(node_id)
        if not node:
            return False

        if ExecutionStateMachine.can_transition(node.state, ExecutionLifecycleState.RETRYING):
            node.state = ExecutionLifecycleState.RETRYING
            node.retry_count += 1
            node.state = ExecutionLifecycleState.READY
            return True
        return False

    def restore_from_checkpoint(self, execution_id: UUID) -> bool:
        """Restores graph node states and outputs from the latest available checkpoint."""
        checkpoint = self.checkpoint_manager.get_latest_checkpoint(execution_id)
        if not checkpoint:
            return False

        for node_id, state in checkpoint.node_states.items():
            node = self.graph.get_node(node_id)
            if node:
                node.state = state

        return True
