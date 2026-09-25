"""
Node Executor.
Executes individual task nodes through ToolDispatcher within the granted worker lease.
"""

from typing import Any, Dict
from app.agents.execution.dispatcher import TaskDispatcher
from app.agents.execution.execution_context import TaskExecutionContext
from app.agents.execution.execution_graph import ExecutionNode
from app.agents.execution.execution_state_machine import ExecutionStateMachine
from app.agents.execution.lifecycle import ExecutionLifecycleState
from app.agents.execution.tool_dispatcher import ToolDispatcher


class NodeExecutor:
    """Executes a single node, managing state transitions and tool invocation."""

    def __init__(self, dispatcher: TaskDispatcher, tool_dispatcher: ToolDispatcher):
        self.dispatcher = dispatcher
        self.tool_dispatcher = tool_dispatcher

    async def execute_node(self, exec_node: ExecutionNode, context: TaskExecutionContext) -> Dict[str, Any]:
        """Runs the node through SCHEDULED -> RUNNING -> COMPLETED with worker lease management."""
        # 1. SCHEDULED
        ExecutionStateMachine.transition(exec_node.state, ExecutionLifecycleState.SCHEDULED, exec_node.node.node_id)
        exec_node.state = ExecutionLifecycleState.SCHEDULED

        lease = await self.dispatcher.dispatch_task(
            exec_node.node.node_id,
            exec_node.node.capability_requirement
        )
        exec_node.assigned_worker_id = lease.worker_id

        # 2. RUNNING
        ExecutionStateMachine.transition(exec_node.state, ExecutionLifecycleState.RUNNING, exec_node.node.node_id)
        exec_node.state = ExecutionLifecycleState.RUNNING

        try:
            # 3. Tool invocation
            outputs = await self.tool_dispatcher.dispatch(context)
            exec_node.outputs = outputs

            # 4. COMPLETED
            ExecutionStateMachine.transition(exec_node.state, ExecutionLifecycleState.COMPLETED, exec_node.node.node_id)
            exec_node.state = ExecutionLifecycleState.COMPLETED
            return outputs
        except Exception as e:
            exec_node.error_message = str(e)
            ExecutionStateMachine.transition(exec_node.state, ExecutionLifecycleState.FAILED, exec_node.node.node_id)
            exec_node.state = ExecutionLifecycleState.FAILED
            raise
        finally:
            await self.dispatcher.complete_task(lease)
