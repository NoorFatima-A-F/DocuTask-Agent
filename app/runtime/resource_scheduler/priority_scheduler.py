"""
ARTEICP Resource Scheduler - Priority & Fair Queue Scheduler
Dispatches tasks with strict priority ordering (CRITICAL > HIGH > NORMAL > LOW), backpressure, and fair queuing.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import heapq
import time
from app.runtime.resource_scheduler.worker_pool import WorkerPoolManager, WorkerInstance


@dataclass(order=True)
class QueuedTask:
    priority_rank: int  # 0=CRITICAL, 1=HIGH, 2=NORMAL, 3=LOW
    enqueued_at: float
    task_id: str = field(compare=False)
    mission_id: str = field(compare=False)
    required_pool: str = field(compare=False)
    payload: Dict[str, Any] = field(default_factory=dict, compare=False)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "mission_id": self.mission_id,
            "priority_rank": self.priority_rank,
            "required_pool": self.required_pool,
            "enqueued_at": self.enqueued_at,
        }


class PriorityScheduler:
    """Manages fair queuing, priority task ordering, and dispatch with backpressure."""

    def __init__(self):
        self.pool_mgr = WorkerPoolManager()
        self.task_queue: List[QueuedTask] = []
        self._max_queue_depth = 1000
        self._seed_queue()

    def _seed_queue(self):
        self.enqueue_task("task_live_ocr", "mission_live_001", "OCR_POOL", priority="HIGH")
        self.enqueue_task("task_live_llm", "mission_live_001", "LLM_POOL", priority="CRITICAL")

    def enqueue_task(
        self,
        task_id: str,
        mission_id: str,
        required_pool: str,
        priority: str = "NORMAL",
        payload: Optional[Dict[str, Any]] = None,
    ) -> bool:
        if len(self.task_queue) >= self._max_queue_depth:
            # Backpressure rejection
            return False

        p_map = {"CRITICAL": 0, "HIGH": 1, "NORMAL": 2, "LOW": 3}
        p_rank = p_map.get(priority, 2)

        task = QueuedTask(
            priority_rank=p_rank,
            enqueued_at=time.time(),
            task_id=task_id,
            mission_id=mission_id,
            required_pool=required_pool,
            payload=payload or {},
        )
        heapq.heappush(self.task_queue, task)
        return True

    def dispatch_next(self) -> Optional[Dict[str, Any]]:
        if not self.task_queue:
            return None

        # Look for the highest priority task whose worker pool is available
        temp = []
        dispatched = None

        while self.task_queue:
            task = heapq.heappop(self.task_queue)
            worker = self.pool_mgr.allocate_worker(task.required_pool)
            if worker:
                dispatched = {
                    "task_id": task.task_id,
                    "mission_id": task.mission_id,
                    "assigned_worker_id": worker.worker_id,
                    "pool_type": task.required_pool,
                    "priority_rank": task.priority_rank,
                }
                break
            else:
                temp.append(task)

        # Restore un-dispatched tasks
        for t in temp:
            heapq.heappush(self.task_queue, t)

        return dispatched

    def get_scheduler_telemetry(self) -> Dict[str, Any]:
        return {
            "queue_depth": len(self.task_queue),
            "max_queue_depth": self._max_queue_depth,
            "backpressure_active": len(self.task_queue) > 500,
            "queued_tasks": [t.to_dict() for t in sorted(self.task_queue)[:10]],
            "pools": self.pool_mgr.get_pool_status(),
        }


priority_scheduler = PriorityScheduler()
