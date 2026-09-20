"""
Workflow Dispatcher.
Dispatches workflow tasks to the Execution Engine or Multi-Agent Coordination layer.
"""

from typing import Any, Dict, Optional
from uuid import UUID
from app.agents.workflow.workflow_node import WorkflowNode


class WorkflowDispatcher:
    """Routes workflow node execution requests to appropriate execution adapters."""

    def __init__(self, execution_adapter: Optional[Any] = None, coordination_adapter: Optional[Any] = None):
        self.execution_adapter = execution_adapter
        self.coordination_adapter = coordination_adapter

    async def dispatch_node(self, node: WorkflowNode, state_vars: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches an individual workflow node."""
        if self.execution_adapter and hasattr(self.execution_adapter, "execute_task_plan"):
            return await self.execution_adapter.execute_task_plan(node.handler, state_vars)
        # Default mock simulation
        return {
            "status": "COMPLETED",
            "node_id": node.node_id,
            "output": f"Output of {node.name}"
        }
