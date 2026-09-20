"""
Runtime Live Dashboard State Aggregator.

Aggregates real-time state across EventStore, MetricsEngine, ResourceMonitor,
and HealthEvaluator into a comprehensive payload for the dashboard UI and API.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List
from app.runtime.observability.anomaly_detection import AnomalyDetector
from app.runtime.observability.event_store import EventStore
from app.runtime.observability.metrics_engine import MetricsEngine
from app.runtime.observability.resource_monitor import ResourceMonitor
from app.runtime.observability.runtime_health import RuntimeHealthEvaluator


class RuntimeDashboardAggregator:
    """Combines all live observability streams into a coherent operational dashboard view."""

    def __init__(
        self,
        event_store: EventStore,
        metrics_engine: MetricsEngine,
        resource_monitor: ResourceMonitor,
        health_evaluator: RuntimeHealthEvaluator,
        anomaly_detector: AnomalyDetector,
    ) -> None:
        self.event_store = event_store
        self.metrics_engine = metrics_engine
        self.resource_monitor = resource_monitor
        self.health_evaluator = health_evaluator
        self.anomaly_detector = anomaly_detector

    def get_dashboard_state(self) -> Dict[str, Any]:
        """Returns comprehensive live runtime telemetry."""
        summary = self.metrics_engine.get_summary()
        res_sample = self.resource_monitor.get_latest_sample()
        health = self.health_evaluator.evaluate_health()
        recent_events = self.event_store.query(limit=25)
        recent_anomalies = self.anomaly_detector.get_recent_anomalies(limit=10)

        # Worker distribution
        workers = {}
        for evt in recent_events:
            if evt.worker_id and evt.worker_id not in workers:
                workers[evt.worker_id] = {
                    "worker_id": evt.worker_id,
                    "status": "BUSY" if evt.status == "RUNNING" else "IDLE",
                    "last_stage": evt.stage,
                    "last_seen": evt.timestamp,
                }

        return {
            "timestamp": time.time(),
            "health": health.model_dump(),
            "resources": res_sample,
            "metrics": summary["metrics"],
            "derived": summary["derived"],
            "active_workers": list(workers.values()),
            "recent_events": [e.model_dump() for e in recent_events],
            "anomalies": [a.model_dump() for a in recent_anomalies],
            "total_events_stored": self.event_store.total_count(),
        }
