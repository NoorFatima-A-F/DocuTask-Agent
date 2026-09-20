"""
Recovery Executor.
Executes the steps of a planned RecoveryGraph using decoupled adapters.
"""

from app.agents.recovery.execution_adapter import RecoveryExecutionAdapter
from app.agents.recovery.planner_adapter import RecoveryPlannerAdapter
from app.agents.recovery.recovery_graph import RecoveryGraph


class RecoveryExecutor:
    """Executes actions in a RecoveryGraph by invoking the appropriate subsystem adapter."""

    def __init__(
        self,
        execution_adapter: RecoveryExecutionAdapter | None = None,
        planner_adapter: RecoveryPlannerAdapter | None = None
    ):
        self.execution_adapter = execution_adapter or RecoveryExecutionAdapter()
        self.planner_adapter = planner_adapter or RecoveryPlannerAdapter()

    async def execute_recovery_graph(self, graph: RecoveryGraph) -> bool:
        """Iterates and executes recovery steps in order."""
        for node_id, node in graph.nodes.items():
            if node.action == "RESET_NODE_STATE":
                await self.execution_adapter.reset_node_for_retry(node.target_id or "")
            elif node.action == "RESTORE_CHECKPOINT":
                pass
            elif node.action == "ROLLBACK_WORKFLOW":
                pass
            elif node.action == "ESCALATE_INCIDENT":
                pass
        return True
