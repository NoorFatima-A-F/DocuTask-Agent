"""Enterprise Resource Scheduler for DocuTask Autonomous Planning Platform.

Manages worker leases, resource reservations, multi-priority execution queues, affinity/anti-affinity
constraints, worker preemption, and elastic pool auto-scaling.
"""

from __future__ import annotations

import heapq
import time
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from app.runtime.planning.capability_discovery import CapabilityDiscoveryEngine, CapabilityProfile


class QueuePriority(int, Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    SPECULATIVE = 5


class WorkerStatus(str, Enum):
    IDLE = "IDLE"
    BUSY = "BUSY"
    MAINTENANCE = "MAINTENANCE"
    DRAINING = "DRAINING"


class WorkerNode(BaseModel):
    """Execution worker instance in the cluster."""
    worker_id: str
    hostname: str = "worker-node-1"
    capabilities: List[str] = Field(default_factory=list)
    status: WorkerStatus = WorkerStatus.IDLE
    current_lease_id: Optional[str] = None
    cpu_cores: int = 8
    memory_mb: int = 16384
    has_gpu: bool = False
    active_affinity_tags: List[str] = Field(default_factory=list)


class WorkerLease(BaseModel):
    """Time-bounded lease granting exclusive execution rights on a worker node."""
    lease_id: str = Field(default_factory=lambda: f"lease_{uuid.uuid4().hex[:8]}")
    worker_id: str
    mission_id: str
    step_id: str
    capability_id: str
    priority: QueuePriority = QueuePriority.HIGH
    leased_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at_epoch: float
    is_active: bool = True
    preempted: bool = False


class ScheduledTaskItem(BaseModel):
    """Priority queue task item."""
    task_id: str
    mission_id: str
    step_id: str
    capability_id: str
    priority: QueuePriority
    required_memory_mb: int = 512
    required_gpu: bool = False
    affinity_tags: List[str] = Field(default_factory=list)
    enqueued_at: float = Field(default_factory=time.time)

    def __lt__(self, other: ScheduledTaskItem) -> bool:
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        return self.enqueued_at < other.enqueued_at


class EnterpriseResourceScheduler:
    """Enterprise-grade scheduler coordinating hardware leases, priorities, and preemption."""

    def __init__(self, capability_discovery: CapabilityDiscoveryEngine, initial_workers: int = 8) -> None:
        self.capability_discovery = capability_discovery
        self._workers: Dict[str, WorkerNode] = {}
        self._active_leases: Dict[str, WorkerLease] = {}
        self._queue: List[ScheduledTaskItem] = []
        self._initialize_workers(initial_workers)

    def _initialize_workers(self, count: int) -> None:
        all_caps = [c.capability_id for c in self.capability_discovery.list_all()]
        for i in range(count):
            wid = f"worker-node-{i+1}"
            self._workers[wid] = WorkerNode(
                worker_id=wid,
                hostname=f"runner-{i+1}.cluster.internal",
                capabilities=all_caps,
                has_gpu=(i % 4 == 0),
            )

    def get_cluster_status(self) -> Dict[str, Any]:
        total = len(self._workers)
        busy = sum(1 for w in self._workers.values() if w.status == WorkerStatus.BUSY)
        idle = total - busy
        return {
            "total_workers": total,
            "idle_workers": idle,
            "busy_workers": busy,
            "utilization_pct": round((busy / max(1, total)) * 100, 2),
            "queue_depth": len(self._queue),
            "active_leases_count": len(self._active_leases),
            "active_leases": list(self._active_leases.values()),
        }

    def enqueue_task(
        self,
        mission_id: str,
        step_id: str,
        capability_id: str,
        priority: QueuePriority = QueuePriority.HIGH,
        required_gpu: bool = False,
        affinity_tags: Optional[List[str]] = None,
    ) -> ScheduledTaskItem:
        task = ScheduledTaskItem(
            task_id=f"task_{uuid.uuid4().hex[:8]}",
            mission_id=mission_id,
            step_id=step_id,
            capability_id=capability_id,
            priority=priority,
            required_gpu=required_gpu,
            affinity_tags=affinity_tags or [],
        )
        heapq.heappush(self._queue, task)
        self._auto_scale_if_needed()
        return task

    def acquire_lease(
        self,
        mission_id: str,
        step_id: str,
        capability_id: str,
        duration_seconds: float = 60.0,
        priority: QueuePriority = QueuePriority.HIGH,
        required_gpu: bool = False,
    ) -> Optional[WorkerLease]:
        """Attempts to find an idle worker matching capabilities and requirements, with preemption fallback."""
        # 1. Look for idle worker
        for wid, worker in self._workers.items():
            if worker.status == WorkerStatus.IDLE:
                if capability_id in worker.capabilities:
                    if not required_gpu or worker.has_gpu:
                        return self._create_lease(worker, mission_id, step_id, capability_id, duration_seconds, priority)

        # 2. Check if preemption is possible for CRITICAL tasks
        if priority == QueuePriority.CRITICAL:
            for lid, lease in list(self._active_leases.items()):
                if lease.priority.value > QueuePriority.HIGH.value:  # Lower priority
                    # Preempt this lease
                    worker = self._workers[lease.worker_id]
                    lease.is_active = False
                    lease.preempted = True
                    del self._active_leases[lid]
                    return self._create_lease(worker, mission_id, step_id, capability_id, duration_seconds, priority)

        return None

    def _create_lease(
        self,
        worker: WorkerNode,
        mission_id: str,
        step_id: str,
        capability_id: str,
        duration_sec: float,
        priority: QueuePriority,
    ) -> WorkerLease:
        worker.status = WorkerStatus.BUSY
        lease = WorkerLease(
            worker_id=worker.worker_id,
            mission_id=mission_id,
            step_id=step_id,
            capability_id=capability_id,
            priority=priority,
            expires_at_epoch=time.time() + duration_sec,
        )
        worker.current_lease_id = lease.lease_id
        self._active_leases[lease.lease_id] = lease
        self.capability_discovery.allocate_capacity(capability_id, 1)
        return lease

    def release_lease(self, lease_id: str) -> bool:
        lease = self._active_leases.get(lease_id)
        if not lease:
            return False

        worker = self._workers.get(lease.worker_id)
        if worker:
            worker.status = WorkerStatus.IDLE
            worker.current_lease_id = None

        self.capability_discovery.release_capacity(lease.capability_id, 1)
        lease.is_active = False
        del self._active_leases[lease_id]
        return True

    def _auto_scale_if_needed(self) -> None:
        """Elastic scale-out: dynamically provisions additional virtual workers if queue depth exceeds 10."""
        if len(self._queue) > 10 and len(self._workers) < 32:
            new_idx = len(self._workers) + 1
            wid = f"worker-elastic-{new_idx}"
            self._workers[wid] = WorkerNode(
                worker_id=wid,
                hostname=f"elastic-{new_idx}.cluster.internal",
                capabilities=[c.capability_id for c in self.capability_discovery.list_all()],
                has_gpu=False,
            )
