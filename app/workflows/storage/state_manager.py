"""
Durable Workflow State Manager.
Persists execution state, task transitions, variables, and event logs.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from ..domain.models import ExecutionRecord, ExecutionState, TaskExecutionRecord, WorkflowContext
from ..domain.exceptions import WorkflowExecutionException
from .checkpoint_manager import CheckpointManager


class WorkflowStateManager:
    """Central durable state manager for workflow instances and task lifecycle records."""

    def __init__(self, checkpoint_manager: Optional[CheckpointManager] = None):
        self.checkpoint_manager = checkpoint_manager or CheckpointManager()
        # Key: execution_id -> ExecutionRecord
        self._executions: Dict[str, ExecutionRecord] = {}

    def create_execution(
        self,
        execution_id: str,
        workflow_id: str,
        workflow_version: str,
        context: WorkflowContext,
    ) -> ExecutionRecord:
        """Initialize a new execution record."""
        record = ExecutionRecord(
            execution_id=execution_id,
            workflow_id=workflow_id,
            workflow_version=workflow_version,
            status=ExecutionState.CREATED,
            context=context,
            start_time=datetime.now(timezone.utc),
        )
        self._executions[execution_id] = record
        return record

    def get_execution(self, execution_id: str) -> Optional[ExecutionRecord]:
        """Retrieve execution record by ID."""
        return self._executions.get(execution_id)

    def update_execution_state(
        self,
        execution_id: str,
        state: ExecutionState,
        error_message: Optional[str] = None,
    ) -> ExecutionRecord:
        """Update overall execution state."""
        record = self.get_execution(execution_id)
        if not record:
            raise WorkflowExecutionException(f"Execution '{execution_id}' not found", execution_id=execution_id)

        record.status = state
        if error_message:
            record.error_message = error_message
        if state in (ExecutionState.COMPLETED, ExecutionState.FAILED, ExecutionState.CANCELLED):
            record.end_time = datetime.now(timezone.utc)
            record.duration_ms = (record.end_time - record.start_time).total_seconds() * 1000.0

        return record

    def record_task_start(self, execution_id: str, task_id: str, task_name: str, inputs: Dict[str, Any]) -> TaskExecutionRecord:
        """Mark task start."""
        record = self.get_execution(execution_id)
        if not record:
            raise WorkflowExecutionException(f"Execution '{execution_id}' not found", execution_id=execution_id)

        task_rec = record.tasks.get(task_id)
        if not task_rec:
            task_rec = TaskExecutionRecord(
                task_id=task_id,
                task_name=task_name,
                status=ExecutionState.RUNNING,
                start_time=datetime.now(timezone.utc),
                inputs=inputs,
                attempts=1,
            )
            record.tasks[task_id] = task_rec
        else:
            task_rec.status = ExecutionState.RUNNING
            task_rec.start_time = datetime.now(timezone.utc)
            task_rec.attempts += 1
            task_rec.inputs = inputs

        return task_rec

    def record_task_complete(
        self,
        execution_id: str,
        task_id: str,
        outputs: Dict[str, Any],
    ) -> TaskExecutionRecord:
        """Mark task complete and checkpoint state."""
        record = self.get_execution(execution_id)
        if not record or task_id not in record.tasks:
            raise WorkflowExecutionException(f"Task '{task_id}' in execution '{execution_id}' not found")

        task_rec = record.tasks[task_id]
        task_rec.status = ExecutionState.COMPLETED
        task_rec.end_time = datetime.now(timezone.utc)
        if task_rec.start_time:
            task_rec.duration_ms = (task_rec.end_time - task_rec.start_time).total_seconds() * 1000.0
        task_rec.outputs = outputs

        # Update execution variables with outputs
        record.context.variables.update(outputs)

        # Create Checkpoint
        completed = [tid for tid, trec in record.tasks.items() if trec.status == ExecutionState.COMPLETED]
        pending = [tid for tid, trec in record.tasks.items() if trec.status != ExecutionState.COMPLETED]
        chk = self.checkpoint_manager.create_checkpoint(
            execution_id=execution_id,
            execution_state=record.status,
            variables=record.context.variables,
            completed_tasks=completed,
            pending_tasks=pending,
        )
        record.current_checkpoint_id = chk.checkpoint_id

        return task_rec

    def record_task_failure(
        self,
        execution_id: str,
        task_id: str,
        error_message: str,
    ) -> TaskExecutionRecord:
        """Mark task failed."""
        record = self.get_execution(execution_id)
        if not record or task_id not in record.tasks:
            raise WorkflowExecutionException(f"Task '{task_id}' in execution '{execution_id}' not found")

        task_rec = record.tasks[task_id]
        task_rec.status = ExecutionState.FAILED
        task_rec.end_time = datetime.now(timezone.utc)
        if task_rec.start_time:
            task_rec.duration_ms = (task_rec.end_time - task_rec.start_time).total_seconds() * 1000.0
        task_rec.error_message = error_message

        return task_rec

    def list_executions(self, workflow_id: Optional[str] = None) -> List[ExecutionRecord]:
        """List all executions, optionally filtered by workflow ID."""
        if workflow_id is None:
            return list(self._executions.values())
        return [e for e in self._executions.values() if e.workflow_id == workflow_id]
