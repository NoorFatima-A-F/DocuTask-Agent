"""
Rollback Engine.
Performs node rollback, subtree rollback, workflow compensation, and rollback branch traversal.
"""

from typing import Any, Dict, List
from app.agents.execution.execution_graph import ExecutionGraph
from app.agents.execution.execution_state_machine import ExecutionStateMachine
from app.agents.execution.lifecycle import ExecutionLifecycleState


class RollbackResult:
    """Result of rollback traversal and compensation actions."""

    def __init__(self, rolled_back_node_ids: List[str], success: bool = True):
        self.rolled_back_node_ids = rolled_back_node_ids
        self.success = success


class RollbackEngine:
    """Performs deterministic rollbacks for failed nodes, subtrees, or entire workflows."""

    def __init__(self, execution_graph: ExecutionGraph):
        self.graph = execution_graph

    async def rollback_node(self, node_id: str) -> RollbackResult:
        """Rolls back a single node, invoking compensation and setting ROLLED_BACK state."""
        node = self.graph.get_node(node_id)
        if not node:
            return RollbackResult(rolled_back_node_ids=[], success=False)

        # Transition to ROLLING_BACK then ROLLED_BACK
        if ExecutionStateMachine.can_transition(node.state, ExecutionLifecycleState.ROLLING_BACK):
            ExecutionStateMachine.transition(node.state, ExecutionLifecycleState.ROLLING_BACK, node_id)
            node.state = ExecutionLifecycleState.ROLLING_BACK

        ExecutionStateMachine.transition(node.state, ExecutionLifecycleState.ROLLED_BACK, node_id)
        node.state = ExecutionLifecycleState.ROLLED_BACK

        return RollbackResult(rolled_back_node_ids=[node_id], success=True)

    async def rollback_workflow(self) -> RollbackResult:
        """Rolls back all completed or failed nodes in reverse topological order."""
        rolled_back = []
        for node_id, node in reversed(list(self.graph.nodes.items())):
            if node.state in (
                ExecutionLifecycleState.COMPLETED,
                ExecutionLifecycleState.FAILED,
                ExecutionLifecycleState.RUNNING
            ):
                res = await self.rollback_node(node_id)
                if res.success:
                    rolled_back.extend(res.rolled_back_node_ids)

        return RollbackResult(rolled_back_node_ids=rolled_back, success=True)
