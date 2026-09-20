"""
Backpressure Controller.
Monitors queue depth and worker utilization to throttle task dispatching.
"""

from app.agents.execution.worker_pool import WorkerPool


class BackpressureController:
    """Detects worker pool congestion and signals throttling."""

    def __init__(self, worker_pool: WorkerPool, congestion_threshold: float = 0.9):
        self.worker_pool = worker_pool
        self.threshold = congestion_threshold

    def is_congested(self) -> bool:
        all_workers = self.worker_pool.registry.list_all()
        if not all_workers:
            return False
        busy = sum(1 for w in all_workers if w.status.value == "BUSY")
        utilization = busy / len(all_workers)
        return utilization >= self.threshold
