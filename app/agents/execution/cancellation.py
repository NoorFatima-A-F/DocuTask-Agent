"""
Execution Cancellation Manager.
Manages graceful and forced cancellation across active nodes and workers.
"""

from app.agents.execution.execution_graph import ExecutionGraph
from app.agents.execution.execution_state_machine import ExecutionStateMachine
from app.agents.execution.lifecycle import ExecutionLifecycleState


class CancellationManager:
    """Handles cancellation signals across active execution sessions."""

    def __init__(self, execution_graph: ExecutionGraph):
        self.graph = execution_graph
        self._is_cancelled = False

    @property
    def is_cancelled(self) -> bool:
        return self._is_cancelled

    def cancel_execution(self, reason: str = "User requested cancellation") -> None:
        """Cancels all active and waiting nodes in the graph."""
        self._is_cancelled = True
        for node_id, node in self.graph.nodes.items():
            if ExecutionStateMachine.can_transition(node.state, ExecutionLifecycleState.CANCELLED):
                node.state = ExecutionLifecycleState.CANCELLED
                node.error_message = reason
