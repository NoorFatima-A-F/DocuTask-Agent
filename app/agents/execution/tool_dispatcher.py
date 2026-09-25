"""
Tool Dispatcher Subsystem.
Dispatches tool execution requests from workers through the ExecutionToolAdapter.
"""

from typing import Any, Dict, Optional
from app.agents.execution.exceptions import ToolDispatchException
from app.agents.execution.execution_context import TaskExecutionContext
from app.agents.execution.tool_adapter import ExecutionToolAdapter


class ToolDispatcher:
    """Dispatches node task execution to tools via ExecutionToolAdapter."""

    def __init__(self, adapter: Optional[ExecutionToolAdapter] = None):
        self.adapter = adapter or ExecutionToolAdapter()

    async def dispatch(self, context: TaskExecutionContext) -> Dict[str, Any]:
        capability = context.capability_requirement or "DEFAULT"
        try:
            result = await self.adapter.invoke_tool(capability, context.parameters)
            return result
        except Exception as e:
            raise ToolDispatchException(f"Failed to dispatch tool for capability '{capability}': {str(e)}") from e
