"""
Autonomous Runtime Monitor (AROL Singleton Coordinator).

The central orchestrator of the Autonomous Runtime Observability Layer.
Unifies EventBus, EventStore, MetricsEngine, ResourceMonitor, AnomalyDetector,
and RuntimeDashboard into an authoritative single source of operational truth.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional
from app.runtime.observability.anomaly_detection import AnomalyDetector
from app.runtime.observability.event_store import EventStore
from app.runtime.observability.event_stream import EventBus
from app.runtime.observability.execution_profiler import ExecutionProfiler
from app.runtime.observability.metrics_engine import MetricsEngine
from app.runtime.observability.metrics_registry import MetricsRegistry
from app.runtime.observability.observability_config import ObservabilityConfig
from app.runtime.observability.resource_monitor import ResourceMonitor
from app.runtime.observability.runtime_dashboard import RuntimeDashboardAggregator
from app.runtime.observability.runtime_health import RuntimeHealthEvaluator
from app.runtime.observability.schemas import (
    BaseRuntimeEvent,
    RuntimeHealthScore,
)
from app.runtime.observability.telemetry_engine import TelemetryEngine

logger = logging.getLogger(__name__)


class RuntimeMonitor:
    """Master runtime observability supervisor for DocuTask Agent."""

    def __init__(self, config: Optional[ObservabilityConfig] = None) -> None:
        self.config = config or ObservabilityConfig()
        self.event_bus = EventBus(max_queue_size=self.config.max_event_queue_size)
        self.event_store = EventStore()
        self.metrics_registry = MetricsRegistry()
        self.metrics_engine = MetricsEngine(self.metrics_registry)
        self.resource_monitor = ResourceMonitor(sample_interval_sec=self.config.resource_sample_interval_sec)
        self.anomaly_detector = AnomalyDetector(z_score_threshold=self.config.anomaly_z_score_threshold)
        self.health_evaluator = RuntimeHealthEvaluator(
            self.metrics_engine, self.resource_monitor, self.anomaly_detector
        )
        self.dashboard_aggregator = RuntimeDashboardAggregator(
            self.event_store,
            self.metrics_engine,
            self.resource_monitor,
            self.health_evaluator,
            self.anomaly_detector,
        )
        self.telemetry_engine = TelemetryEngine(self.metrics_engine, self.event_store)
        self._is_started = False

        # Wire EventBus to internal consumers
        self.event_bus.subscribe_sync(self._on_event_sync)

    def _on_event_sync(self, event: BaseRuntimeEvent) -> None:
        """Internal synchronous pipeline on every published event."""
        # 1. Update Metrics
        self.metrics_engine.handle_event(event)
        # 2. Update Telemetry multi-windows
        self.telemetry_engine.process_event(event)
        # 3. Check for anomalies
        self.anomaly_detector.check_event(event)

    async def start(self) -> None:
        """Boots event bus dispatchers and resource monitor loop."""
        if self._is_started:
            return
        self._is_started = True
        await self.event_bus.start()
        await self.resource_monitor.start(event_bus=self.event_bus)
        logger.info("Autonomous Runtime Observability Layer (AROL) started successfully.")

    async def stop(self) -> None:
        """Gracefully shuts down background monitoring."""
        self._is_started = False
        await self.resource_monitor.stop()
        await self.event_bus.stop()
        logger.info("AROL shut down.")

    async def emit_event(self, event: BaseRuntimeEvent) -> BaseRuntimeEvent:
        """
        Primary asynchronous entry point for emitting events.
        Appends to immutable EventStore with SHA-256 validation and publishes to EventBus.
        """
        signed_event = await self.event_store.append(event)
        await self.event_bus.publish(signed_event)
        return signed_event

    def emit_event_sync(self, event: BaseRuntimeEvent) -> BaseRuntimeEvent:
        """Primary synchronous entry point for emitting events."""
        signed_event = self.event_store.append_sync(event)
        self.event_bus.publish_sync(signed_event)
        return signed_event

    def get_mission_timeline(self, mission_id: str) -> List[Dict[str, Any]]:
        """Reconstructs mission timeline strictly from event store logs."""
        from app.runtime.observability.mission_snapshot import MissionSnapshotGenerator
        events = self.event_store.get_events_for_mission(mission_id)
        snapshot = MissionSnapshotGenerator.generate_snapshot(mission_id, events)
        return [item.model_dump() for item in snapshot.timeline]

    def get_mission_profile(self, mission_id: str) -> Dict[str, Any]:
        """Generates execution flame graph and bottleneck analysis for a mission."""
        events = self.event_store.get_events_for_mission(mission_id)
        span_tree = ExecutionProfiler.build_span_tree(events)
        flame_graph = ExecutionProfiler.generate_flame_graph(span_tree)
        bottlenecks = ExecutionProfiler.find_bottlenecks(events)
        return {
            "mission_id": mission_id,
            "flame_graph": flame_graph.model_dump(),
            "bottlenecks": bottlenecks,
            "total_spans": len(span_tree),
        }

    def get_dashboard_state(self) -> Dict[str, Any]:
        """Returns comprehensive live dashboard state."""
        return self.dashboard_aggregator.get_dashboard_state()

    def get_health(self) -> RuntimeHealthScore:
        """Returns mathematically computed health score."""
        return self.health_evaluator.evaluate_health()

    def clear(self) -> None:
        """Clears memory stores (for testing)."""
        self.event_store.clear()
        self.metrics_registry = MetricsRegistry()
        self.metrics_engine = MetricsEngine(self.metrics_registry)


# Global Singleton Instance
_global_runtime_monitor: Optional[RuntimeMonitor] = None


def get_runtime_monitor() -> RuntimeMonitor:
    """Retrieves or instantiates the global RuntimeMonitor singleton."""
    global _global_runtime_monitor
    if _global_runtime_monitor is None:
        _global_runtime_monitor = RuntimeMonitor()
    return _global_runtime_monitor
