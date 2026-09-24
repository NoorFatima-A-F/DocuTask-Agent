"""
Workflow Executor.
Executes sequence of workflow nodes, updating workflow instance state, checkpoints, and history.
"""

from typing import Optional
from app.agents.workflow.lifecycle import WorkflowLifecycleState
from app.agents.workflow.workflow_definition import WorkflowDefinition
from app.agents.workflow.workflow_dispatcher import WorkflowDispatcher
from app.agents.workflow.workflow_instance import WorkflowInstance


class WorkflowExecutor:
    """Executes workflow nodes through the dispatcher and maintains instance state progression."""

    def __init__(self, dispatcher: Optional[WorkflowDispatcher] = None):
        self.dispatcher = dispatcher or WorkflowDispatcher()

    async def execute_instance(
        self,
        definition: WorkflowDefinition,
        instance: WorkflowInstance
    ) -> WorkflowInstance:
        """Executes nodes in topological sequence."""
        current_instance = instance.transition_to(WorkflowLifecycleState.RUNNING)
        order = definition.graph.get_topological_order()

        for node_id in order:
            node = definition.graph.nodes[node_id]
            # Dispatch node
            out = await self.dispatcher.dispatch_node(node, current_instance.workflow_state.variables)
            # Update workflow state
            new_wf_state = current_instance.workflow_state.record_node_completion(node_id, output=out)
            current_instance = current_instance.model_copy(update={"workflow_state": new_wf_state})

        return current_instance.transition_to(WorkflowLifecycleState.COMPLETED)
