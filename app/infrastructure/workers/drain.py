"""Worker Graceful Draining and Evacuation Manager."""

import threading
from typing import Dict
from app.infrastructure.workers.models import Worker, WorkerStatus
from app.infrastructure.workers.lifecycle import WorkerLifecycleStateMachine


class WorkerDrainManager:
    """Coordinates graceful draining of workers without interrupting in-flight executions."""

    def __init__(self) -> None:
        self._draining_workers: Dict[str, str] = {}  # worker_id -> reason
        self._lock = threading.RLock()

    def start_drain(self, worker: Worker, reason: str = "Graceful maintenance drain") -> Worker:
        """Mark worker as DRAINING and record drain intent."""
        with self._lock:
            WorkerLifecycleStateMachine.transition(worker, WorkerStatus.DRAINING, reason=reason)
            self._draining_workers[worker.worker_id] = reason
            return worker

    def is_draining(self, worker_id: str) -> bool:
        with self._lock:
            return worker_id in self._draining_workers

    def check_drain_complete(self, worker: Worker) -> bool:
        """Check if all in-flight assignments on draining worker have completed."""
        with self._lock:
            if worker.status == WorkerStatus.DRAINING and len(worker.active_assignments) == 0:
                return True
            return False

    def complete_drain(self, worker: Worker, target_status: WorkerStatus = WorkerStatus.UNAVAILABLE) -> Worker:
        """Finalize drain and transition worker to target status."""
        with self._lock:
            WorkerLifecycleStateMachine.transition(worker, target_status, reason="Drain completed")
            self._draining_workers.pop(worker.worker_id, None)
            return worker
