"""
Enterprise Workflow Runtime Engine.
The primary execution coordinator for durable, event-driven, fault-tolerant DAG workflows.
"""

import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
from ..domain.models import (
    ExecutionRecord,
    ExecutionState,
    TaskDefinition,
    TaskType,
    WorkflowContext,
    WorkflowDefinition,
)
from ..domain.exceptions import (
    WorkflowExecutionException,
    TaskExecutionException,
    CompensationException,
)
from ..compiler.compiler import WorkflowCompiler
from ..graph.graph import ExecutionGraph
from ..graph.nodes import TaskNode, DecisionNode, ApprovalNode
from ..graph.edges import EdgeType
from ..storage.state_manager import WorkflowStateManager
from ..storage.checkpoint_manager import CheckpointManager
from ..scheduler.scheduler import TaskScheduler
from ..executor.task_executor import TaskExecutor
from ..retry.engine import RetryEngine
from ..timeout.timeout_manager import TimeoutManager
from ..compensation.engine import CompensationEngine
from ..approvals.engine import ApprovalEngine
from ..approvals.models import ApprovalStatus
from ..decision.engine import DecisionEngine
from ..hooks.hooks import WorkflowHooks
from ..audit.auditor import WorkflowAuditor


class WorkflowRuntime:
    """Enterprise Workflow Orchestration Engine Runtime."""

    def __init__(
        self,
        state_manager: Optional[WorkflowStateManager] = None,
        task_executor: Optional[TaskExecutor] = None,
        compensation_engine: Optional[CompensationEngine] = None,
        approval_engine: Optional[ApprovalEngine] = None,
    ):
        self.state_manager = state_manager or WorkflowStateManager()
        self.checkpoint_manager = self.state_manager.checkpoint_manager
        self.task_executor = task_executor or TaskExecutor()
        self.compensation_engine = compensation_engine or CompensationEngine()
        self.approval_engine = approval_engine or ApprovalEngine()
        self.scheduler = TaskScheduler()
        self.hooks = WorkflowHooks()
        self.auditor = WorkflowAuditor()

    async def execute_workflow(
        self,
        definition: WorkflowDefinition,
        initial_variables: Optional[Dict[str, Any]] = None,
        context: Optional[WorkflowContext] = None,
    ) -> ExecutionRecord:
        """Compile and execute a workflow to completion or suspension."""
        graph = WorkflowCompiler.compile(definition)

        exec_id = context.execution_id if (context and context.execution_id) else str(uuid.uuid4())
        ctx = context or WorkflowContext(
            execution_id=exec_id,
            workflow_id=definition.id,
            workflow_version=str(definition.version),
            organization_id=definition.organization_id,
            variables=dict(initial_variables or {}),
        )
        ctx.execution_id = exec_id
        ctx.variables.update(definition.variables)
        if initial_variables:
            ctx.variables.update(initial_variables)

        record = self.state_manager.get_execution(exec_id)
        if not record:
            record = self.state_manager.create_execution(
                execution_id=exec_id,
                workflow_id=definition.id,
                workflow_version=str(definition.version),
                context=ctx,
            )

        self.auditor.record_event(exec_id, "workflow.started", actor=ctx.actor, details={"workflow_id": definition.id})
        self.hooks.trigger_before_start(record)
        self.state_manager.update_execution_state(exec_id, ExecutionState.RUNNING)

        try:
            # Topological execution of DAG nodes
            ordered_nodes = graph.topological_sort()

            for node in ordered_nodes:
                # Check if paused/cancelled
                current_rec = self.state_manager.get_execution(exec_id)
                if current_rec and current_rec.status in (ExecutionState.PAUSED, ExecutionState.SUSPENDED, ExecutionState.CANCELLED):
                    return current_rec

                # Resolve task definition
                task_def: Optional[TaskDefinition] = None
                if isinstance(node, TaskNode) and node.task_def:
                    task_def = node.task_def
                else:
                    # Find in definition
                    matching = [t for t in definition.tasks if t.id == node.node_id]
                    if matching:
                        task_def = matching[0]

                if not task_def:
                    continue

                # Handle Condition / Decision nodes
                if task_def.type == TaskType.CONDITION:
                    cond_expr = task_def.metadata.get("condition", "")
                    cond_result = DecisionEngine.evaluate_condition(cond_expr, ctx.variables)
                    self.state_manager.record_task_start(exec_id, task_def.id, task_def.name, {"condition": cond_expr})
                    self.state_manager.record_task_complete(exec_id, task_def.id, {"condition_met": cond_result})
                    self.auditor.record_event(exec_id, "task.decision_evaluated", details={"task_id": task_def.id, "result": cond_result})
                    continue

                # Handle Human Approval gates
                if task_def.type == TaskType.APPROVAL or task_def.type == TaskType.HUMAN:
                    existing_task_rec = current_rec.tasks.get(task_def.id) if current_rec else None
                    if existing_task_rec and existing_task_rec.status == ExecutionState.COMPLETED:
                        continue

                    # Check for existing requests in approval engine
                    pending_reqs = self.approval_engine.get_pending_for_execution(exec_id)
                    matching_req = [r for r in pending_reqs if r.task_id == task_def.id]
                    if not matching_req:
                        # Check if already approved in engine
                        all_req_ids = self.approval_engine._execution_requests.get(exec_id, [])
                        all_matching = [self.approval_engine._requests[rid] for rid in all_req_ids if self.approval_engine._requests[rid].task_id == task_def.id]
                        if all_matching and all_matching[0].status == ApprovalStatus.APPROVED:
                            req = all_matching[0]
                            self.state_manager.record_task_start(exec_id, task_def.id, task_def.name, task_def.inputs)
                            self.state_manager.record_task_complete(exec_id, task_def.id, {"approved": True, "votes": len(req.votes)})
                            continue

                        # Create approval request and suspend workflow
                        req = self.approval_engine.create_approval_request(
                            execution_id=exec_id,
                            task_id=task_def.id,
                            required_role=task_def.metadata.get("role", "manager"),
                        )
                        self.state_manager.update_execution_state(exec_id, ExecutionState.SUSPENDED)
                        self.auditor.record_event(exec_id, "workflow.suspended_for_approval", details={"request_id": req.request_id, "task_id": task_def.id})
                        return self.state_manager.get_execution(exec_id)
                    else:
                        req = matching_req[0]
                        if req.status == ApprovalStatus.PENDING:
                            self.state_manager.update_execution_state(exec_id, ExecutionState.SUSPENDED)
                            return self.state_manager.get_execution(exec_id)
                        elif req.status == ApprovalStatus.APPROVED:
                            self.state_manager.record_task_start(exec_id, task_def.id, task_def.name, task_def.inputs)
                            self.state_manager.record_task_complete(exec_id, task_def.id, {"approved": True, "votes": len(req.votes)})
                            continue

                # Standard Task Execution with Retry and Timeout
                # Skip if already completed (e.g. on resume)
                existing_task_rec = current_rec.tasks.get(task_def.id) if current_rec else None
                if existing_task_rec and existing_task_rec.status == ExecutionState.COMPLETED:
                    continue

                await self._execute_task_with_retry(exec_id, task_def, ctx)

            # Workflow completed successfully
            self.state_manager.update_execution_state(exec_id, ExecutionState.COMPLETED)
            self.auditor.record_event(exec_id, "workflow.completed")
            self.hooks.trigger_completion(record)

        except Exception as e:
            self.state_manager.update_execution_state(exec_id, ExecutionState.FAILED, error_message=str(e))
            self.auditor.record_event(exec_id, "workflow.failed", details={"error": str(e)})

            # Trigger Saga Rollback if configured
            if definition.compensation_policy.get("enabled", True):
                self.state_manager.update_execution_state(exec_id, ExecutionState.COMPENSATING)
                self.auditor.record_event(exec_id, "workflow.compensation_started")
                try:
                    await self.compensation_engine.execute_rollback(exec_id)
                    self.auditor.record_event(exec_id, "workflow.compensation_completed")
                except Exception as comp_err:
                    self.auditor.record_event(exec_id, "workflow.compensation_failed", details={"error": str(comp_err)})

            return self.state_manager.get_execution(exec_id)

        return self.state_manager.get_execution(exec_id)

    async def _execute_task_with_retry(
        self,
        execution_id: str,
        task_def: TaskDefinition,
        ctx: WorkflowContext,
    ) -> Dict[str, Any]:
        """Execute task with retries, timeout tracking, and compensation recording."""
        self.state_manager.record_task_start(execution_id, task_def.id, task_def.name, task_def.inputs)
        self.auditor.record_event(execution_id, "task.started", details={"task_id": task_def.id})

        max_attempts = task_def.retry_policy.get("max_attempts", 3)
        last_err = None

        for attempt in range(1, max_attempts + 1):
            start_t = datetime.now(timezone.utc)
            try:
                # Enforce task timeout
                TimeoutManager.assert_not_timed_out(start_t, task_def.timeout_seconds, task_id=task_def.id)

                outputs = await self.task_executor.execute_task(task_def, ctx.variables)

                # Record task complete
                task_rec = self.state_manager.record_task_complete(execution_id, task_def.id, outputs)
                self.auditor.record_event(execution_id, "task.completed", details={"task_id": task_def.id, "outputs": outputs})

                # Register Saga compensation action if present
                if task_def.compensation_action:
                    self.compensation_engine.record_completed_task(execution_id, task_def, task_def.inputs)

                self.hooks.trigger_after_task(execution_id, task_rec)
                return outputs

            except Exception as e:
                last_err = e
                if not RetryEngine.is_retryable(e) or attempt == max_attempts:
                    self.state_manager.record_task_failure(execution_id, task_def.id, str(e))
                    self.auditor.record_event(execution_id, "task.failed", details={"task_id": task_def.id, "error": str(e), "attempts": attempt})
                    raise e

                delay = RetryEngine.calculate_delay(attempt, task_def.retry_policy)
                self.auditor.record_event(execution_id, "task.retrying", details={"task_id": task_def.id, "attempt": attempt, "delay": delay})
                await asyncio.sleep(min(0.05, delay))

        raise last_err

    async def resume_execution(
        self,
        execution_id: str,
        definition: WorkflowDefinition,
        resumed_variables: Optional[Dict[str, Any]] = None,
    ) -> ExecutionRecord:
        """Resume a suspended/waiting execution."""
        record = self.state_manager.get_execution(execution_id)
        if not record:
            raise WorkflowExecutionException(f"Execution '{execution_id}' not found", execution_id=execution_id)

        if resumed_variables:
            record.context.variables.update(resumed_variables)

        self.state_manager.update_execution_state(execution_id, ExecutionState.RUNNING)
        self.auditor.record_event(execution_id, "workflow.resumed")

        # Continue execution with updated context
        return await self.execute_workflow(
            definition=definition,
            initial_variables=record.context.variables,
            context=record.context,
        )

    def pause_execution(self, execution_id: str) -> ExecutionRecord:
        """Pause a running execution."""
        self.auditor.record_event(execution_id, "workflow.paused")
        return self.state_manager.update_execution_state(execution_id, ExecutionState.PAUSED)

    def cancel_execution(self, execution_id: str) -> ExecutionRecord:
        """Cancel an execution."""
        self.auditor.record_event(execution_id, "workflow.cancelled")
        return self.state_manager.update_execution_state(execution_id, ExecutionState.CANCELLED)
