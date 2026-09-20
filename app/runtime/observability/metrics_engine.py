"""
Autonomous Runtime Metrics Engine.

Consumes the raw event stream in real-time and computes every operational metric.
Zero hardcoding: every metric is derived directly from observed event timestamps,
durations, payloads, and worker status changes.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional
from app.runtime.observability.metrics_registry import MetricsRegistry
from app.runtime.observability.schemas import (
    BaseRuntimeEvent,
    EventCategory,
    MetricRecord,
)


class MetricsEngine:
    """Computes mathematically grounded runtime metrics from incoming event streams."""

    def __init__(self, registry: Optional[MetricsRegistry] = None) -> None:
        self.registry = registry or MetricsRegistry()
        self._initialize_core_metrics()
        self._active_worker_timestamps: Dict[str, float] = {}
        self._mission_start_times: Dict[str, float] = {}

    def _initialize_core_metrics(self) -> None:
        # Counters
        self.registry.counter("missions_created_total")
        self.registry.counter("missions_completed_total")
        self.registry.counter("missions_failed_total")
        self.registry.counter("nodes_executed_total")
        self.registry.counter("nodes_failed_total")
        self.registry.counter("retries_total")
        self.registry.counter("recoveries_total")
        self.registry.counter("memory_hits_total")
        self.registry.counter("memory_misses_total")
        self.registry.counter("rules_reused_total")
        self.registry.counter("rules_learned_total")
        self.registry.counter("tokens_prompt_total")
        self.registry.counter("tokens_completion_total")
        self.registry.counter("tokens_used_total")
        self.registry.counter("cost_usd_total")
        self.registry.counter("storage_operations_total")
        self.registry.counter("reflection_cycles_total")
        self.registry.counter("human_reviews_total")

        # Gauges
        self.registry.gauge("queue_length_current")
        self.registry.gauge("active_workers_current")
        self.registry.gauge("active_missions_current")
        self.registry.gauge("cpu_utilization_pct")
        self.registry.gauge("memory_utilization_mb")
        self.registry.gauge("gpu_utilization_pct")

        # Histograms
        self.registry.histogram("mission_duration_ms")
        self.registry.histogram("planner_latency_ms")
        self.registry.histogram("execution_latency_ms")
        self.registry.histogram("worker_busy_duration_ms")
        self.registry.histogram("queue_wait_time_ms")

    def handle_event(self, event: BaseRuntimeEvent) -> None:
        """Processes a single event, updating respective metrics."""
        category = event.category
        payload = event.payload or {}
        duration = event.duration_ms

        # 1. Mission Category
        if category == EventCategory.MISSION:
            if event.event_type in ("MISSION_CREATED", "MISSION_STARTED"):
                self.registry.counter("missions_created_total").inc()
                self.registry.gauge("active_missions_current").inc()
                self._mission_start_times[event.mission_id] = event.timestamp
            elif event.event_type == "MISSION_COMPLETED":
                self.registry.counter("missions_completed_total").inc()
                self.registry.gauge("active_missions_current").dec()
                if event.mission_id in self._mission_start_times:
                    start_t = self._mission_start_times.pop(event.mission_id)
                    total_dur = max(0.0, (event.timestamp - start_t) * 1000.0)
                    self.registry.histogram("mission_duration_ms").observe(total_dur)
            elif event.event_type == "MISSION_FAILED":
                self.registry.counter("missions_failed_total").inc()
                self.registry.gauge("active_missions_current").dec()
                self._mission_start_times.pop(event.mission_id, None)

        # 2. Planner Category
        elif category == EventCategory.PLANNER:
            if duration > 0:
                self.registry.histogram("planner_latency_ms").observe(duration)

        # 3. Execution Category
        elif category == EventCategory.EXECUTION:
            self.registry.counter("nodes_executed_total").inc()
            if duration > 0:
                self.registry.histogram("execution_latency_ms").observe(duration)
            if event.status == "FAILED":
                self.registry.counter("nodes_failed_total").inc()

        # 4. Worker Category
        elif category == EventCategory.WORKER:
            wid = event.worker_id or "unknown"
            if event.event_type in ("WORKER_ASSIGNED", "WORKER_BUSY"):
                self._active_worker_timestamps[wid] = event.timestamp
                self.registry.gauge("active_workers_current").set(len(self._active_worker_timestamps))
            elif event.event_type in ("WORKER_RELEASED", "WORKER_IDLE"):
                if wid in self._active_worker_timestamps:
                    busy_time = max(0.0, (event.timestamp - self._active_worker_timestamps.pop(wid)) * 1000.0)
                    self.registry.histogram("worker_busy_duration_ms").observe(busy_time)
                self.registry.gauge("active_workers_current").set(len(self._active_worker_timestamps))

        # 5. Failure & Recovery
        elif category == EventCategory.FAILURE:
            if "RETRY" in event.event_type:
                self.registry.counter("retries_total").inc()
        elif category == EventCategory.RECOVERY:
            self.registry.counter("recoveries_total").inc()

        # 6. Memory Category
        elif category == EventCategory.MEMORY:
            if payload.get("hit") is True or "HIT" in event.event_type:
                self.registry.counter("memory_hits_total").inc()
            else:
                self.registry.counter("memory_misses_total").inc()
            if payload.get("rules_reused", 0) > 0:
                self.registry.counter("rules_reused_total").inc(payload["rules_reused"])
            if payload.get("rules_learned", 0) > 0:
                self.registry.counter("rules_learned_total").inc(payload["rules_learned"])

        # 7. Reflection Category
        elif category == EventCategory.REFLECTION:
            self.registry.counter("reflection_cycles_total").inc()

        # 8. Human Review
        elif category == EventCategory.HUMAN_REVIEW:
            self.registry.counter("human_reviews_total").inc()

        # 9. Cost & Tokens
        elif category == EventCategory.COST:
            if "cost_usd" in payload:
                self.registry.counter("cost_usd_total").inc(float(payload["cost_usd"]))
            if "prompt_tokens" in payload:
                self.registry.counter("tokens_prompt_total").inc(int(payload["prompt_tokens"]))
            if "completion_tokens" in payload:
                self.registry.counter("tokens_completion_total").inc(int(payload["completion_tokens"]))
            if "total_tokens" in payload:
                self.registry.counter("tokens_used_total").inc(int(payload["total_tokens"]))

        # 10. Storage
        elif category == EventCategory.STORAGE:
            self.registry.counter("storage_operations_total").inc()

        # 11. Scheduler & Queues
        elif category == EventCategory.SCHEDULER:
            if "queue_length" in payload:
                self.registry.gauge("queue_length_current").set(float(payload["queue_length"]))
            if "queue_wait_ms" in payload:
                self.registry.histogram("queue_wait_time_ms").observe(float(payload["queue_wait_ms"]))

        # 12. Resource & Telemetry
        elif category == EventCategory.RESOURCE:
            if "cpu_pct" in payload:
                self.registry.gauge("cpu_utilization_pct").set(float(payload["cpu_pct"]))
            if "memory_mb" in payload:
                self.registry.gauge("memory_utilization_mb").set(float(payload["memory_mb"]))
            if "gpu_pct" in payload:
                self.registry.gauge("gpu_utilization_pct").set(float(payload["gpu_pct"]))

    def get_summary(self) -> Dict[str, Any]:
        """Calculates derived metrics (success rates, throughput, cost/mission)."""
        metrics = self.registry.get_all_metrics_dict()
        
        # Calculate derived success rates
        executed = metrics.get("nodes_executed_total", 0.0)
        failed = metrics.get("nodes_failed_total", 0.0)
        node_success_rate = ((executed - failed) / executed) if executed > 0 else 1.0

        missions_created = metrics.get("missions_created_total", 0.0)
        missions_completed = metrics.get("missions_completed_total", 0.0)
        mission_success_rate = (missions_completed / missions_created) if missions_created > 0 else 1.0

        mem_hits = metrics.get("memory_hits_total", 0.0)
        mem_misses = metrics.get("memory_misses_total", 0.0)
        mem_total = mem_hits + mem_misses
        memory_hit_ratio = (mem_hits / mem_total) if mem_total > 0 else 0.0

        return {
            "metrics": metrics,
            "derived": {
                "node_success_rate": round(node_success_rate, 4),
                "mission_success_rate": round(mission_success_rate, 4),
                "memory_hit_ratio": round(memory_hit_ratio, 4),
                "total_cost_usd": round(metrics.get("cost_usd_total", 0.0), 5),
                "total_tokens": int(metrics.get("tokens_used_total", 0)),
            },
        }
