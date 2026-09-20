"""
Parallel Wavefront Task Scheduler.

Maximizes concurrency by advancing ready nodes in parallel batches, respecting
resource limits and maximum concurrent worker thresholds.
"""

from __future__ import annotations

import asyncio
from typing import Any, Callable, Coroutine, Dict, List, Set
from app.runtime.planning.graph.dag import ExecutionDAG
from app.runtime.planning.graph.node import DAGNode, NodeStatus
from app.runtime.planning.scheduler.worker_allocator import WorkerAllocator


class ParallelScheduler:
    """Dispatches ready nodes concurrently across available worker pools."""

    def __init__(self, allocator: WorkerAllocator) -> None:
        self.allocator = allocator

    async def schedule_wavefront(
        self,
        dag: ExecutionDAG,
        completed_node_ids: Set[str],
        executor_func: Callable[[DAGNode, str], Coroutine[Any, Any, Dict[str, Any]]],
    ) -> List[DAGNode]:
        """
        Identifies all ready nodes in the DAG, allocates workers, and executes them concurrently.
        Returns list of newly completed nodes in this wavefront.
        """
        ready_nodes = dag.get_ready_nodes(completed_node_ids)
        if not ready_nodes:
            return []

        tasks = []
        for node in ready_nodes:
            worker = self.allocator.allocate_worker(node)
            wid = worker.worker_id if worker else "worker_default"
            node.mark_running(wid)

            async def _run(n: DAGNode, w: str):
                try:
                    res = await executor_func(n, w)
                    n.mark_completed(res)
                except Exception as ex:
                    n.mark_failed(str(ex))
                finally:
                    self.allocator.release_worker(w)
                return n

            tasks.append(_run(node, wid))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        completed = [r for r in results if isinstance(r, DAGNode) and r.status == NodeStatus.COMPLETED]
        return completed
