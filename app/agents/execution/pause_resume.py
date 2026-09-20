"""
Pause and Resume Manager.
Coordinates pausing in-flight tasks and resuming paused execution graphs.
"""

from app.agents.execution.execution_graph import ExecutionGraph
from app.agents.execution.execution_state_machine import ExecutionStateMachine
from app.agents.execution.lifecycle import ExecutionLifecycleState


class PauseResumeManager:
    """Manages pause and resume states for execution graphs."""

    def __init__(self, execution_graph: ExecutionGraph):
        self.graph = execution_graph
        self._is_paused = False

    @property
    def is_paused(self) -> bool:
        return self._is_paused

    def pause(self) -> None:
        """Transitions runnable/ready nodes to PAUSED."""
        self._is_paused = True
        for node_id, node in self.graph.nodes.items():
            if ExecutionStateMachine.can_transition(node.state, ExecutionLifecycleState.PAUSED):
                node.state = ExecutionLifecycleState.PAUSED

    def resume(self) -> None:
        """Resumes paused nodes back to READY."""
        self._is_paused = False
        for node_id, node in self.graph.nodes.items():
            if node.state == ExecutionLifecycleState.PAUSED:
                node.state = ExecutionLifecycleState.READY
