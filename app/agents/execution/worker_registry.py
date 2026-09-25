"""
Worker Registry.
In-memory registry of active workers and capabilities.
"""

from typing import Dict, List, Optional
from app.agents.execution.worker import Worker, WorkerStatus


class WorkerRegistry:
    """Registry maintaining active registered workers."""

    def __init__(self):
        self._workers: Dict[str, Worker] = {}

    def register(self, worker: Worker) -> None:
        self._workers[worker.worker_id] = worker

    def get(self, worker_id: str) -> Optional[Worker]:
        return self._workers.get(worker_id)

    def list_all(self) -> List[Worker]:
        return list(self._workers.values())

    def list_idle(self) -> List[Worker]:
        return [w for w in self._workers.values() if w.status == WorkerStatus.IDLE]
