"""
DocuTask Agent - Worker Read Projection Engine
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, List, Any
import time
from app.runtime.events.models.event import DomainEvent
from app.runtime.events.models.event_types import DomainEventType


class WorkerProjection:
    """
    Read Model Projection for Worker Pool Subsystems.
    Tracks worker concurrency, load distribution, and task throughput.
    """

    def __init__(self):
        self.workers: Dict[str, Dict[str, Any]] = {}
        self.total_tasks_executed: int = 0
        self.total_tokens_consumed: int = 0

    def apply_event(self, event: DomainEvent) -> None:
        """Applies a domain event to update the worker projection."""
        worker_id = event.actor.actor_id if event.actor.actor_type == "WORKER" else event.payload.get("worker_id")
        if not worker_id:
            return

        if worker_id not in self.workers:
            self.workers[worker_id] = {
                "worker_id": worker_id,
                "status": "IDLE",
                "active_tasks": 0,
                "completed_tasks": 0,
                "failed_tasks": 0,
                "cpu_usage_pct": 12.0,
                "memory_mb": 128.0,
                "total_duration_ms": 0.0,
                "last_seen_utc": event.timestamp_utc,
            }

        w_data = self.workers[worker_id]
        w_data["last_seen_utc"] = event.timestamp_utc

        if event.event_type == DomainEventType.TASK_ASSIGNED:
            w_data["status"] = "BUSY"
            w_data["active_tasks"] += 1

        elif event.event_type == DomainEventType.TASK_COMPLETED:
            w_data["completed_tasks"] += 1
            w_data["active_tasks"] = max(0, w_data["active_tasks"] - 1)
            w_data["total_duration_ms"] += event.payload.get("duration_ms", 0.0)
            if w_data["active_tasks"] == 0:
                w_data["status"] = "IDLE"
            self.total_tasks_executed += 1
            self.total_tokens_consumed += event.payload.get("tokens_used", 0)

        elif event.event_type == DomainEventType.TASK_FAILED:
            w_data["failed_tasks"] += 1
            w_data["active_tasks"] = max(0, w_data["active_tasks"] - 1)
            if w_data["active_tasks"] == 0:
                w_data["status"] = "IDLE"

        elif event.event_type == DomainEventType.WORKER_HEARTBEAT:
            w_data["cpu_usage_pct"] = event.payload.get("cpu_usage_pct", 12.0)
            w_data["memory_mb"] = event.payload.get("memory_mb", 128.0)
            w_data["active_tasks"] = event.payload.get("active_tasks", w_data["active_tasks"])

    def get_worker_pool_state(self) -> Dict[str, Any]:
        """Returns aggregated worker pool projection state."""
        return {
            "total_workers": len(self.workers),
            "busy_workers_count": sum(1 for w in self.workers.values() if w["status"] == "BUSY"),
            "idle_workers_count": sum(1 for w in self.workers.values() if w["status"] == "IDLE"),
            "total_tasks_executed": self.total_tasks_executed,
            "total_tokens_consumed": self.total_tokens_consumed,
            "workers": list(self.workers.values()),
            "timestamp_utc": time.time(),
        }


# Global singleton worker projection
worker_projection = WorkerProjection()
