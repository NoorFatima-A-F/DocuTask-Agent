"""
Worker Health Monitor.
Tracks worker responsiveness, crash frequency, and hung leases.
"""

from typing import Dict
from pydantic import BaseModel


class WorkerHealthStatus(BaseModel):
    worker_id: str
    is_responsive: bool = True
    consecutive_failures: int = 0
    model_config = {"frozen": True}


class WorkerMonitor:
    """Monitors worker heartbeats and identifies unresponsive worker nodes."""

    def __init__(self):
        self._stats: Dict[str, int] = {}

    def record_worker_failure(self, worker_id: str) -> None:
        self._stats[worker_id] = self._stats.get(worker_id, 0) + 1

    def is_worker_healthy(self, worker_id: str, threshold: int = 3) -> bool:
        return self._stats.get(worker_id, 0) < threshold
