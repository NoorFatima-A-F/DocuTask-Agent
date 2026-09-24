"""
Phase 13.18: Autoscaling Engine & Elastic Capacity Orchestration
Evaluates queue pressure, worker CPU/RAM utilization, and SLA deadlines to scale worker nodes up/down.
"""

from __future__ import annotations
import math
from datetime import datetime, timezone
from typing import Dict, List, Any
from app.runtime.distributed.models.schemas import (
    AutoscalingPolicy,
    ScalingAction,
)
from app.runtime.distributed.queue.distributed_queue import QueueManager
from app.runtime.distributed.workers.worker_fleet_manager import WorkerFleetManager


class AutoscalingEngine:
    """Monitors cluster pressure and dynamically scales cloud worker nodes."""

    def __init__(self, fleet_manager: WorkerFleetManager, queue_manager: QueueManager):
        self.fleet_manager = fleet_manager
        self.queue_manager = queue_manager
        self.policy = AutoscalingPolicy()
        self._scaling_history: List[Dict[str, Any]] = []

    def evaluate_scaling(self) -> Dict[str, Any]:
        workers = self.fleet_manager.list_workers(active_only=True)
        active_count = len(workers)
        queue_metrics = self.queue_manager.get_channel("agent_tasks").get_metrics()
        queue_depth = queue_metrics["total_depth"]

        avg_cpu = sum(w.capacity.cpu_utilization_pct for w in workers) / max(1, active_count)
        avg_ram = sum(w.capacity.memory_utilization_pct for w in workers) / max(1, active_count)

        action = ScalingAction.STABLE
        desired = active_count

        # Scale UP conditions: high queue depth or high CPU
        if queue_depth >= self.policy.scale_up_threshold_jobs or avg_cpu > self.policy.target_cpu_utilization_pct:
            # Formula: desired = ceil(queue_depth * avg_duration / target_sla)
            scale_increment = max(1, math.ceil(queue_depth / 5))
            desired = min(self.policy.max_workers, active_count + scale_increment)
            if desired > active_count:
                action = ScalingAction.SCALE_UP

        # Scale DOWN conditions: queue empty and low CPU
        elif queue_depth == 0 and avg_cpu < 25.0 and active_count > self.policy.min_workers:
            desired = max(self.policy.min_workers, active_count - 1)
            if desired < active_count:
                action = ScalingAction.SCALE_DOWN

        self.policy.current_desired_workers = desired
        self.policy.last_scaling_action = action
        self.policy.last_scaled_at = datetime.now(timezone.utc).isoformat()

        decision = {
            "action": action.value,
            "current_workers": active_count,
            "desired_workers": desired,
            "queue_depth": queue_depth,
            "mean_cpu_pct": round(avg_cpu, 1),
            "mean_ram_pct": round(avg_ram, 1),
            "timestamp": self.policy.last_scaled_at,
        }
        self._scaling_history.append(decision)
        return decision

    def get_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        return self._scaling_history[-limit:]
