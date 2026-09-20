"""
Enterprise Execution Engine.
Core driver executing validated PlanGraph DAGs using stateful dependency tracking,
runtime scheduling, worker dispatching, and checkpointing.
"""

from typing import Any, Dict, Optional
from uuid import uuid4
from app.agents.execution.checkpoint_manager import CheckpointManager
from app.agents.execution.context import ExecutionRequest, ExecutionResult
from app.agents.execution.dependency_tracker import DependencyTracker
from app.agents.execution.dispatcher import TaskDispatcher
from app.agents.execution.execution_graph import ExecutionGraph
from app.agents.execution.executor import NodeExecutor
from app.agents.execution.lifecycle import ExecutionLifecycleState
from app.agents.execution.metadata import ExecutionStatistics
from app.agents.execution.parallel_executor import ParallelExecutor
from app.agents.execution.scheduler import RuntimeScheduler
from app.agents.execution.tool_adapter import ExecutionToolAdapter
from app.agents.execution.tool_dispatcher import ToolDispatcher
from app.agents.execution.worker_pool import WorkerPool


class ExecutionEngine:
    """
    Stateful Execution Engine.
    Executes already-approved PlanGraph DAGs with bounded worker concurrency and checkpointing.
    """

    def __init__(
        self,
        worker_pool: Optional[WorkerPool] = None,
        tool_adapter: Optional[ExecutionToolAdapter] = None,
        checkpoint_manager: Optional[CheckpointManager] = None,
        scheduler: Optional[RuntimeScheduler] = None
    ):
        self.worker_pool = worker_pool or WorkerPool(max_workers=4)
        self.tool_adapter = tool_adapter or ExecutionToolAdapter()
        self.checkpoint_manager = checkpoint_manager or CheckpointManager()
        self.scheduler = scheduler or RuntimeScheduler()

        self.tool_dispatcher = ToolDispatcher(adapter=self.tool_adapter)
        self.task_dispatcher = TaskDispatcher(worker_pool=self.worker_pool)
        self.node_executor = NodeExecutor(
            dispatcher=self.task_dispatcher,
            tool_dispatcher=self.tool_dispatcher
        )
        self.parallel_executor = ParallelExecutor(
            node_executor=self.node_executor,
            max_concurrency=self.worker_pool.max_workers
        )

    async def execute(self, request: ExecutionRequest) -> ExecutionResult:
        """Executes a plan graph through topological dependency resolution."""
        execution_id = uuid4()
        plan_graph = request.plan.graph
        exec_graph = ExecutionGraph(plan_graph)
        tracker = DependencyTracker(exec_graph)

        accumulated_outputs: Dict[str, Any] = dict(request.initial_inputs)
        completed_nodes = []
        errors = []

        # Initial checkpoint
        self.checkpoint_manager.create_checkpoint(
            execution_id=execution_id,
            trigger="PRE_EXECUTION",
            node_states={nid: n.state for nid, n in exec_graph.nodes.items()},
            outputs=accumulated_outputs,
            completed_nodes=completed_nodes
        )

        while tracker.has_pending_work():
            runnable = tracker.get_runnable_nodes()
            if not runnable:
                # Check if everything is completed or if there is a deadlock
                if tracker.is_execution_completed():
                    break
                errors.append("Execution deadlock detected: pending nodes exist but no nodes are runnable.")
                break

            # Schedule runnable nodes
            ordered_nodes = self.scheduler.order_runnable_nodes(runnable, exec_graph)

            # Execute batch concurrently
            results = await self.parallel_executor.execute_batch(
                ordered_nodes,
                exec_graph,
                execution_id
            )

            for res in results:
                if res:
                    accumulated_outputs.update(res)

            completed_nodes.extend(ordered_nodes)

            # Post-task checkpoint
            self.checkpoint_manager.create_checkpoint(
                execution_id=execution_id,
                trigger="POST_TASK_BATCH",
                node_states={nid: n.state for nid, n in exec_graph.nodes.items()},
                outputs=accumulated_outputs,
                completed_nodes=completed_nodes
            )

        final_state = ExecutionLifecycleState.COMPLETED if len(errors) == 0 else ExecutionLifecycleState.FAILED

        stats = ExecutionStatistics(
            total_nodes_count=len(exec_graph.nodes),
            completed_nodes_count=len(completed_nodes),
            failed_nodes_count=len(errors)
        )

        return ExecutionResult(
            execution_id=execution_id,
            plan_id=request.plan.identity.plan_id,
            lifecycle_state=final_state,
            outputs=accumulated_outputs,
            statistics=stats,
            errors=errors
        )
