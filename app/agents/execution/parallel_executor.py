"""
Parallel Task Executor.
Executes multiple independent runnable nodes concurrently within a bounded semaphore.
"""

import asyncio
from typing import Any, Dict, List
from app.agents.execution.execution_context import TaskExecutionContext
from app.agents.execution.execution_graph import ExecutionGraph
from app.agents.execution.executor import NodeExecutor


class ParallelExecutor:
    """Executes runnable nodes in parallel using asyncio.gather bounded by concurrency limit."""

    def __init__(self, node_executor: NodeExecutor, max_concurrency: int = 4):
        self.node_executor = node_executor
        self.semaphore = asyncio.Semaphore(max_concurrency)

    async def execute_batch(
        self,
        node_ids: List[str],
        graph: ExecutionGraph,
        execution_id: Any
    ) -> List[Dict[str, Any]]:
        """Executes the given batch of runnable node IDs concurrently."""
        async def _run_single(nid: str) -> Dict[str, Any]:
            async with self.semaphore:
                exec_node = graph.get_node(nid)
                if not exec_node:
                    return {}
                ctx = TaskExecutionContext(
                    execution_id=execution_id,
                    node_id=nid,
                    capability_requirement=exec_node.node.capability_requirement,
                    parameters=exec_node.node.parameters
                )
                return await self.node_executor.execute_node(exec_node, ctx)

        tasks = [_run_single(nid) for nid in node_ids]
        return await asyncio.gather(*tasks)
