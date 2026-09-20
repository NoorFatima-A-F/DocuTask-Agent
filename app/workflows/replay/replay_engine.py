"""
Enterprise Workflow Replay Engine.
Enables deterministic replay of full workflows, specific failed tasks, or state recovery from checkpoints.
"""

from typing import Any, Dict, Optional
from ..domain.models import ExecutionRecord, WorkflowDefinition
from ..domain.exceptions import WorkflowExecutionException
from ..runtime.runtime import WorkflowRuntime


class WorkflowReplayEngine:
    """Orchestrates deterministic replay of workflow executions."""

    def __init__(self, runtime: WorkflowRuntime):
        self.runtime = runtime

    async def replay_execution(
        self,
        execution_id: str,
        definition: WorkflowDefinition,
        override_variables: Optional[Dict[str, Any]] = None,
    ) -> ExecutionRecord:
        """Replay a workflow execution with original or overridden variables."""
        original_rec = self.runtime.state_manager.get_execution(execution_id)
        if not original_rec:
            raise WorkflowExecutionException(f"Historical execution '{execution_id}' not found for replay")

        replay_vars = dict(original_rec.context.variables)
        if override_variables:
            replay_vars.update(override_variables)

        # Execute as fresh execution instance with replay audit tags
        self.runtime.auditor.record_event(
            execution_id,
            "workflow.replay_initiated",
            details={"original_execution_id": execution_id},
        )

        return await self.runtime.execute_workflow(
            definition=definition,
            initial_variables=replay_vars,
        )
