"""
Phase 13.18: Cloud Worker Fleet Manager & Heartbeat Monitor
Manages worker node registration, health tracking, capacity reporting, and automatic crash failover.
"""

from __future__ import annotations
import random
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from app.runtime.distributed.models.schemas import (
    WorkerNode,
    WorkerStatus,
    WorkerCapacity,
    RegionName,
)
from app.runtime.distributed.models.events import (
    DistributedEvent,
    DistributedEventType,
    DistributedEventBus,
)


class WorkerFleetManager:
    """Orchestrates worker nodes, capacity allocation, draining, and heartbeat timeouts."""

    def __init__(self, event_bus: Optional[DistributedEventBus] = None):
        self.event_bus = event_bus or DistributedEventBus()
        self._workers: Dict[str, WorkerNode] = {}
        self.heartbeat_timeout_sec = 30
        self._seed_workers()

    def _seed_workers(self):
        nodes = [
            ("node_us_east_01", "worker-cloudrun-us-01.internal", RegionName.US_EAST, 15.0, 22.0),
            ("node_us_east_02", "worker-cloudrun-us-02.internal", RegionName.US_EAST, 45.0, 52.0),
            ("node_eu_central_01", "worker-gke-eu-01.internal", RegionName.EU_CENTRAL, 28.0, 34.0),
            ("node_asia_east_01", "worker-gke-asia-01.internal", RegionName.ASIA_EAST, 18.0, 25.0),
            ("node_pk_south_01", "worker-local-pk-01.internal", RegionName.PK_SOUTH, 12.0, 18.0),
        ]
        for wid, host, reg, cpu, ram in nodes:
            cap = WorkerCapacity(
                max_concurrent_jobs=8,
                allocated_jobs=random.randint(0, 3),
                cpu_cores=4,
                memory_mb=8192,
                cpu_utilization_pct=cpu,
                memory_utilization_pct=ram,
            )
            node = WorkerNode(
                worker_id=wid,
                hostname=host,
                region=reg,
                status=WorkerStatus.ONLINE,
                capacity=cap,
                last_heartbeat=datetime.now(timezone.utc).isoformat(),
                total_jobs_completed=random.randint(80, 450),
                historical_avg_latency_ms=round(random.uniform(95.0, 180.0), 2),
            )
            self._workers[wid] = node

    def register_worker(
        self,
        hostname: str,
        region: RegionName = RegionName.US_EAST,
        capabilities: Optional[List[str]] = None,
        cpu_cores: int = 4,
        memory_mb: int = 8192,
    ) -> WorkerNode:
        cap = WorkerCapacity(max_concurrent_jobs=8, cpu_cores=cpu_cores, memory_mb=memory_mb)
        node = WorkerNode(
            hostname=hostname,
            region=region,
            capabilities=capabilities or ["reasoning", "ocr", "planning"],
            capacity=cap,
        )
        self._workers[node.worker_id] = node
        return node

    def record_heartbeat(self, worker_id: str, cpu_pct: Optional[float] = None, memory_pct: Optional[float] = None) -> bool:
        worker = self._workers.get(worker_id)
        if not worker:
            return False

        worker.last_heartbeat = datetime.now(timezone.utc).isoformat()
        if worker.status == WorkerStatus.CRASHED:
            worker.status = WorkerStatus.ONLINE

        if cpu_pct is not None:
            worker.capacity.cpu_utilization_pct = cpu_pct
        if memory_pct is not None:
            worker.capacity.memory_utilization_pct = memory_pct

        return True

    def drain_worker(self, worker_id: str) -> bool:
        worker = self._workers.get(worker_id)
        if not worker:
            return False
        worker.status = WorkerStatus.DRAINING
        return True

    def check_heartbeats(self) -> List[str]:
        """Detects dead workers that missed heartbeats and marks them CRASHED."""
        crashed_ids = []
        now = datetime.now(timezone.utc)
        for wid, worker in self._workers.items():
            if worker.status in (WorkerStatus.OFFLINE, WorkerStatus.DRAINING):
                continue
            try:
                t_last = datetime.fromisoformat(worker.last_heartbeat)
                delta_sec = (now - t_last).total_seconds()
                if delta_sec > self.heartbeat_timeout_sec:
                    worker.status = WorkerStatus.CRASHED
                    crashed_ids.append(wid)
            except Exception:
                pass
        return crashed_ids

    def list_workers(self, region: Optional[RegionName] = None, active_only: bool = False) -> List[WorkerNode]:
        workers = list(self._workers.values())
        if region:
            workers = [w for w in workers if w.region == region]
        if active_only:
            workers = [w for w in workers if w.status in (WorkerStatus.ONLINE, WorkerStatus.BUSY)]
        return workers

    def get_worker(self, worker_id: str) -> Optional[WorkerNode]:
        return self._workers.get(worker_id)
