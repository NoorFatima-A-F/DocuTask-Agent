"""
Enterprise Workflow Parallel Execution Engine.
Supports Fan-out, Fan-in, Scatter-Gather, and Barrier Synchronization.
"""

import asyncio
from typing import Any, Callable, Dict, List


class ParallelEngine:
    """Coordinates parallel branch execution and barrier joins."""

    @staticmethod
    async def execute_fan_out(
        branch_tasks: List[Callable[[], Any]],
        concurrency_limit: int = 10,
    ) -> List[Any]:
        """Execute multiple branch tasks concurrently up to concurrency limit."""
        sem = asyncio.Semaphore(concurrency_limit)

        async def run_with_sem(task_fn):
            async with sem:
                if asyncio.iscoroutinefunction(task_fn):
                    return await task_fn()
                else:
                    return task_fn()

        return await asyncio.gather(*(run_with_sem(fn) for fn in branch_tasks), return_exceptions=False)
