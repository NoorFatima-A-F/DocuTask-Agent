"""
Workflow Orchestrator.
Orchestrates multi-stage DAG workflows across task execution, sagas, branching, human approvals, and child workflows.
"""

import logging
import time
from typing import List, Optional
from app.agents.workflow.approval_workflow import ApprovalWorkflowEngine
from app.agents.workflow.child_workflow import ChildWorkflowManager
from app.agents.workflow.conditional_workflow import ConditionalWorkflowEngine
from app.agents.workflow.context import WorkflowResult
from app.agents.workflow.lifecycle import WorkflowLifecycleState
from app.agents.workflow.metadata import WorkflowStatistics
from app.agents.workflow.parallel_workflow import ParallelWorkflowEngine
from app.agents.workflow.saga import SagaOrchestrator
from app.agents.workflow.timer_manager import TimerManager
from app.agents.workflow.workflow_definition import WorkflowDefinition
from app.agents.workflow.workflow_dispatcher import WorkflowDispatcher
from app.agents.workflow.workflow_instance import WorkflowInstance
from app.agents.workflow.workflow_node import WorkflowNodeType

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    """Orchestrates end-to-end DAG execution across heterogeneous node typologies."""

    def __init__(
        self,
        dispatcher: Optional[WorkflowDispatcher] = None,
        saga_orchestrator: Optional[SagaOrchestrator] = None,
        parallel_engine: Optional[ParallelWorkflowEngine] = None,
        conditional_engine: Optional[ConditionalWorkflowEngine] = None,
        approval_engine: Optional[ApprovalWorkflowEngine] = None,
        child_manager: Optional[ChildWorkflowManager] = None,
        timer_manager: Optional[TimerManager] = None,
    ) -> None:
        self.dispatcher = dispatcher or WorkflowDispatcher()
        self.saga = saga_orchestrator or SagaOrchestrator()
        self.parallel = parallel_engine or ParallelWorkflowEngine()
        self.conditional = conditional_engine or ConditionalWorkflowEngine()
        self.approval = approval_engine or ApprovalWorkflowEngine()
        self.child_manager = child_manager or ChildWorkflowManager()
        self.timer_manager = timer_manager or TimerManager()

    async def orchestrate(
        self,
        definition: WorkflowDefinition,
        instance: WorkflowInstance,
    ) -> WorkflowResult:
        """Executes a workflow definition instance to completion or failure."""
        start_time = time.perf_counter()
        current_instance = instance.transition_to(WorkflowLifecycleState.RUNNING)
        order = definition.graph.get_topological_order()
        errors: List[str] = []

        try:
            for node_id in order:
                node = definition.graph.nodes[node_id]
                node_type = node.node_type
                state_vars = current_instance.workflow_state.variables

                logger.info(f"Orchestrating node '{node_id}' ({node_type}) for workflow {instance.instance_id}")

                if node_type == WorkflowNodeType.TASK:
                    output = await self.dispatcher.dispatch_node(node, state_vars)
                elif node_type == WorkflowNodeType.SAGA_TRANSACTION:
                    output = await self.saga.execute_saga_step(
                        workflow_id=instance.instance_id,
                        node=node,
                        input_data=state_vars,
                    )
                elif node_type == WorkflowNodeType.TIMER:
                    delay = node.parameters.get("delay_seconds", 0.0)
                    timer = self.timer_manager.register_timer(instance.instance_id, node_id, delay)
                    # Advance time simulation or check
                    output = {"timer_id": str(timer.timer_id), "status": "FIRED"}
                elif node_type == WorkflowNodeType.HUMAN_APPROVAL:
                    task = self.approval.create_human_task(
                        workflow_id=instance.instance_id,
                        node_id=node_id,
                        title=node.name,
                        approvers=node.parameters.get("approvers", ["admin"]),
                    )
                    output = {"task_id": str(task.task_id), "status": task.status.value}
                else:
                    output = await self.dispatcher.dispatch_node(node, state_vars)

                new_state = current_instance.workflow_state.record_node_completion(node_id, output=output)
                current_instance = current_instance.model_copy(update={"workflow_state": new_state})

            current_instance = current_instance.transition_to(WorkflowLifecycleState.COMPLETED)
            final_lifecycle = WorkflowLifecycleState.COMPLETED

        except Exception as exc:
            logger.error(f"Workflow {instance.instance_id} failed during orchestration: {exc}")
            errors.append(str(exc))
            try:
                current_instance = current_instance.transition_to(WorkflowLifecycleState.FAILED)
            except Exception:
                pass
            final_lifecycle = WorkflowLifecycleState.FAILED

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        stats = WorkflowStatistics(
            total_nodes_executed=len(current_instance.workflow_state.completed_nodes),
            duration_ms=elapsed_ms,
        )

        return WorkflowResult(
            identity=current_instance.identity,
            lifecycle_state=final_lifecycle,
            outputs=current_instance.workflow_state.variables,
            statistics=stats,
            errors=errors,
        )
