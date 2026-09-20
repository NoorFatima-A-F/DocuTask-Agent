"""
ARTEICP Observability - Worker Monitor
Tracks CPU/GPU/API worker queue depths, utilization, throughput, and active execution heartbeats.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import time


@dataclass
class WorkerTelemetryInfo:
    worker_id: str
    worker_type: str  # OCR_WORKER | LLM_WORKER | VALIDATION_WORKER | MEMORY_WORKER
    status: str  # IDLE | BUSY | THROTTLED | OFFLINE
    active_tasks_count: int
    queue_depth: int
    utilization_pct: float
    avg_latency_ms: float
    total_processed_tasks: int
    error_rate_pct: float
    last_heartbeat: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class WorkerMonitor:
    """Monitors worker pools, queue depths, and execution load in real time."""

    def __init__(self):
        self.workers: Dict[str, WorkerTelemetryInfo] = {}
        self._seed_workers()

    def _seed_workers(self):
        w1 = WorkerTelemetryInfo(
            worker_id="worker_ocr_1",
            worker_type="OCR_WORKER",
            status="BUSY",
            active_tasks_count=1,
            queue_depth=2,
            utilization_pct=65.0,
            avg_latency_ms=180.0,
            total_processed_tasks=1420,
            error_rate_pct=0.2,
        )
        w2 = WorkerTelemetryInfo(
            worker_id="worker_llm_1",
            worker_type="LLM_WORKER",
            status="BUSY",
            active_tasks_count=1,
            queue_depth=3,
            utilization_pct=82.5,
            avg_latency_ms=450.0,
            total_processed_tasks=3100,
            error_rate_pct=0.1,
        )
        w3 = WorkerTelemetryInfo(
            worker_id="worker_val_1",
            worker_type="VALIDATION_WORKER",
            status="IDLE",
            active_tasks_count=0,
            queue_depth=0,
            utilization_pct=15.0,
            avg_latency_ms=45.0,
            total_processed_tasks=890,
            error_rate_pct=0.0,
        )
        w4 = WorkerTelemetryInfo(
            worker_id="worker_mem_1",
            worker_type="MEMORY_WORKER",
            status="IDLE",
            active_tasks_count=0,
            queue_depth=0,
            utilization_pct=22.0,
            avg_latency_ms=60.0,
            total_processed_tasks=510,
            error_rate_pct=0.0,
        )
        for w in [w1, w2, w3, w4]:
            self.workers[w.worker_id] = w

    def list_workers(self) -> List[Dict[str, Any]]:
        return [w.to_dict() for w in self.workers.values()]

    def record_worker_heartbeat(self, worker_id: str, queue_depth: int, is_busy: bool, latency_ms: float = 0.0):
        if worker_id in self.workers:
            w = self.workers[worker_id]
            w.queue_depth = queue_depth
            w.status = "BUSY" if is_busy else "IDLE"
            w.last_heartbeat = time.time()
            if latency_ms > 0:
                w.avg_latency_ms = round((w.avg_latency_ms * 0.9) + (latency_ms * 0.1), 2)
            w.total_processed_tasks += 1

    def get_cluster_summary(self) -> Dict[str, Any]:
        workers_list = list(self.workers.values())
        total_q = sum(w.queue_depth for w in workers_list)
        busy_count = sum(1 for w in workers_list if w.status == "BUSY")
        avg_util = sum(w.utilization_pct for w in workers_list) / max(1, len(workers_list))

        return {
            "total_workers": len(workers_list),
            "busy_workers": busy_count,
            "total_queued_tasks": total_q,
            "average_cluster_utilization_pct": round(avg_util, 1),
            "cluster_health": "HEALTHY" if total_q < 20 else "QUEUE_CONGESTION",
            "workers": [w.to_dict() for w in workers_list],
        }


worker_monitor = WorkerMonitor()
