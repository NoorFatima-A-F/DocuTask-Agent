"""
Master DAG Execution Scheduler.

Coordinates DAG topological execution, dynamic worker allocation, CPM critical-path tracking,
and real-time event emission integrated with Phase 1 Observability.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, Callable, Coroutine, Dict, List, Optional, Set
from app.runtime.planning.graph.dag import ExecutionDAG
from app.runtime.planning.graph.node import DAGNode, NodeStatus
from app.runtime.planning.scheduler.critical_path import CriticalPathEngine
from app.runtime.planning.scheduler.parallel_scheduler import ParallelScheduler
from app.runtime.planning.scheduler.queue_manager import PriorityQueueManager
from app.runtime.planning.scheduler.worker_allocator import WorkerAllocator


class DAGScheduler:
    """Master Scheduler orchestrating end-to-end execution of an ExecutionDAG."""

    def __init__(
        self,
        allocator: Optional[WorkerAllocator] = None,
        runtime_monitor: Optional[Any] = None,
    ) -> None:
        self.allocator = allocator or WorkerAllocator()
        self.queue_mgr = PriorityQueueManager()
        self.parallel_scheduler = ParallelScheduler(self.allocator)
        self.runtime_monitor = runtime_monitor
        self._completed_node_ids: Set[str] = set()
        self._failed_node_ids: Set[str] = set()

    async def execute_dag(
        self,
        dag: ExecutionDAG,
        executor_func: Optional[Callable[[DAGNode, str], Coroutine[Any, Any, Dict[str, Any]]]] = None,
    ) -> Dict[str, Any]:
        """
        Executes entire DAG to completion or failure, returning execution metrics and node states.
        """
        self._completed_node_ids.clear()
        self._failed_node_ids.clear()

        # Initial CPM calculation
        cpm_results = CriticalPathEngine.analyze(dag)

        # Default executor if none provided
        if executor_func is None:
            async def default_executor(node: DAGNode, worker_id: str) -> Dict[str, Any]:
                await asyncio.sleep(0.01)  # Simulated non-blocking work
                return {"status": "SUCCESS", "extracted_entities": 4, "worker_id": worker_id}
            executor_func = default_executor

        start_time = time.time()
        max_iterations = len(dag.nodes) * 2 + 10
        iteration = 0

        while len(self._completed_node_ids) + len(self._failed_node_ids) < len(dag.nodes) and iteration < max_iterations:
            iteration += 1
            completed_in_wave = await self.parallel_scheduler.schedule_wavefront(
                dag=dag,
                completed_node_ids=self._completed_node_ids,
                executor_func=executor_func,
            )

            for n in completed_in_wave:
                self._completed_node_ids.add(n.node_id)

            # Check for failed nodes
            for n in dag.nodes.values():
                if n.status == NodeStatus.FAILED:
                    self._failed_node_ids.add(n.node_id)

            if not completed_in_wave and len(self._completed_node_ids) + len(self._failed_node_ids) < len(dag.nodes):
                # No ready nodes can proceed -> blocked or deadlock
                break

        total_runtime_ms = max(0.1, (time.time() - start_time) * 1000.0)
        is_success = len(self._completed_node_ids) == len(dag.nodes)

        return {
            "mission_id": dag.mission_id,
            "dag_id": dag.dag_id,
            "status": "COMPLETED" if is_success else "FAILED",
            "total_nodes": len(dag.nodes),
            "completed_nodes_count": len(self._completed_node_ids),
            "failed_nodes_count": len(self._failed_node_ids),
            "actual_runtime_ms": round(total_runtime_ms, 2),
            "cpm": cpm_results,
        }

    def get_status(self, dag: ExecutionDAG) -> Dict[str, Any]:
        """Returns live execution status of DAG."""
        return {
            "mission_id": dag.mission_id,
            "dag_id": dag.dag_id,
            "completed_nodes": list(self._completed_node_ids),
            "failed_nodes": list(self._failed_node_ids),
            "total_nodes": len(dag.nodes),
            "ready_nodes": [n.node_id for n in dag.get_ready_nodes(self._completed_node_ids)],
        }
