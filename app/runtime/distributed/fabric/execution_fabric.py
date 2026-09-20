"""
Phase 13.18: Execution Fabric & Intelligent Load Balancer
Capacity-weighted worker selection and remote execution dispatcher.
"""

from __future__ import annotations
import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from app.runtime.distributed.models.schemas import (
    WorkerNode,
    WorkerStatus,
    ScheduledJob,
    JobState,
    RegionName,
)
from app.runtime.distributed.workers.worker_fleet_manager import WorkerFleetManager


class IntelligentLoadBalancer:
    """Selects optimal worker node using multi-dimensional capacity weighting."""

    @staticmethod
    def calculate_worker_capacity_score(worker: WorkerNode) -> float:
        """Higher score = more available capacity and better candidate."""
        if worker.status != WorkerStatus.ONLINE:
            return -1.0

        cap = worker.capacity
        if cap.allocated_jobs >= cap.max_concurrent_jobs:
            return 0.0

        # Utilization penalty
        cpu_penalty = (cap.cpu_utilization_pct / 100.0) * 0.35
        ram_penalty = (cap.memory_utilization_pct / 100.0) * 0.30
        job_penalty = (cap.allocated_jobs / max(1, cap.max_concurrent_jobs)) * 0.20
        lat_penalty = min(0.15, (worker.historical_avg_latency_ms / 1000.0) * 0.15)

        total_penalty = cpu_penalty + ram_penalty + job_penalty + lat_penalty
        return max(0.01, round(1.0 - total_penalty, 4))

    @classmethod
    def select_best_worker(
        cls,
        workers: List[WorkerNode],
        required_capabilities: Optional[List[str]] = None,
        preferred_region: Optional[RegionName] = None,
    ) -> Optional[WorkerNode]:
        candidates = []
        for w in workers:
            if w.status != WorkerStatus.ONLINE:
                continue
            if required_capabilities:
                if not all(c in w.capabilities for c in required_capabilities):
                    continue

            score = cls.calculate_worker_capacity_score(w)
            if score <= 0:
                continue

            # Bonus for matching preferred region
            if preferred_region and w.region == preferred_region:
                score += 0.25

            candidates.append((w, score))

        if not candidates:
            return None

        candidates.sort(key=lambda c: c[1], reverse=True)
        return candidates[0][0]


class ExecutionFabric:
    """Orchestrates job routing, remote execution simulation, and result collection."""

    def __init__(self, fleet_manager: WorkerFleetManager):
        self.fleet_manager = fleet_manager
        self.load_balancer = IntelligentLoadBalancer()

    async def dispatch_job(self, job: ScheduledJob) -> bool:
        workers = self.fleet_manager.list_workers(active_only=True)
        best_worker = self.load_balancer.select_best_worker(
            workers=workers,
            preferred_region=job.target_region,
        )
        if not best_worker:
            return False

        job.assigned_worker_id = best_worker.worker_id
        job.state = JobState.RUNNING
        job.started_at = datetime.now(timezone.utc).isoformat()
        best_worker.capacity.allocated_jobs += 1
        return True
