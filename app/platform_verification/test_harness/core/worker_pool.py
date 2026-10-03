"""
Distributed Worker Pool managing node registration, heartbeats, and task allocation.
"""
from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from app.platform_verification.test_harness.domain.models import (
    WorkerNode,
    WorkerStatus,
    TestCategory,
)
from app.platform_verification.test_harness.domain.interfaces import IWorkerPool


class WorkerPool(IWorkerPool):
    """Manages worker cluster nodes and dispatches tasks based on capabilities."""

    def __init__(self) -> None:
        self._workers: Dict[str, WorkerNode] = {}
        self._load_default_workers()

    def register_worker(self, worker_id: str, capabilities: List[TestCategory]) -> WorkerNode:
        worker = WorkerNode(
            worker_id=worker_id,
            hostname=f"node-{worker_id}.verification.local",
            capabilities=capabilities,
            status=WorkerStatus.IDLE,
        )
        self._workers[worker_id] = worker
        return worker

    def heartbeat(self, worker_id: str) -> bool:
        if worker_id in self._workers:
            self._workers[worker_id].last_heartbeat = datetime.now(timezone.utc).isoformat()
            if self._workers[worker_id].status == WorkerStatus.OFFLINE:
                self._workers[worker_id].status = WorkerStatus.IDLE
            return True
        return False

    def allocate_worker(self, category: TestCategory) -> Optional[WorkerNode]:
        for worker in self._workers.values():
            if worker.status == WorkerStatus.IDLE and category in worker.capabilities:
                worker.status = WorkerStatus.BUSY
                return worker
        return None

    def release_worker(self, worker_id: str) -> None:
        if worker_id in self._workers:
            self._workers[worker_id].status = WorkerStatus.IDLE
            self._workers[worker_id].active_job_id = None

    def list_workers(self) -> List[WorkerNode]:
        return list(self._workers.values())

    def _load_default_workers(self) -> None:
        all_caps = list(TestCategory)
        self.register_worker("worker_core_01", all_caps)
        self.register_worker("worker_ai_01", [TestCategory.AI_QUALITY, TestCategory.FUNCTIONAL])
        self.register_worker("worker_sec_01", [TestCategory.SECURITY, TestCategory.CHAOS])
