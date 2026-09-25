"""
Execution Subsystem Injectable Factory.
Wires ExecutionEngine, RuntimeScheduler, WorkerPool, CheckpointManager,
ExecutionMetricsCollector, ExecutionRepository, and ExecutionCache.
"""

from app.agents.execution.cache import ExecutionCache
from app.agents.execution.checkpoint_manager import CheckpointManager
from app.agents.execution.engine import ExecutionEngine
from app.agents.execution.manager import ExecutionManager
from app.agents.execution.metrics import ExecutionMetricsCollector
from app.agents.execution.repository import ExecutionRepository
from app.agents.execution.runtime import ExecutionRuntime
from app.agents.execution.scheduler import RuntimeScheduler, SchedulingStrategy
from app.agents.execution.tool_adapter import ExecutionToolAdapter
from app.agents.execution.worker_pool import WorkerPool


class ExecutionFactory:
    """Factory container wiring execution runtime components."""

    @staticmethod
    def create_execution_subsystem(
        max_workers: int = 4,
        scheduling_strategy: SchedulingStrategy = SchedulingStrategy.PRIORITY
    ):
        worker_pool = WorkerPool(max_workers=max_workers)
        checkpoint_mgr = CheckpointManager()
        scheduler = RuntimeScheduler(strategy=scheduling_strategy)
        tool_adapter = ExecutionToolAdapter()
        engine = ExecutionEngine(
            worker_pool=worker_pool,
            tool_adapter=tool_adapter,
            checkpoint_manager=checkpoint_mgr,
            scheduler=scheduler
        )
        runtime = ExecutionRuntime(engine=engine)
        manager = ExecutionManager(engine=engine)
        metrics = ExecutionMetricsCollector()
        repo = ExecutionRepository()
        cache = ExecutionCache()

        return manager, runtime, engine, checkpoint_mgr, metrics, repo, cache
