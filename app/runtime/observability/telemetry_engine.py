"""
Autonomous Telemetry Engine.

Coordinates real-time metric streams, windowed aggregations, and telemetry pipelines.
Acts as the central telemetry interface for Replay, Governance, and Benchmark modules.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from app.runtime.observability.aggregation import TimeWindowAggregator
from app.runtime.observability.event_store import EventStore
from app.runtime.observability.metrics_engine import MetricsEngine
from app.runtime.observability.schemas import BaseRuntimeEvent


class TelemetryEngine:
    """Core Telemetry Coordinator managing multiple time horizons."""

    def __init__(self, metrics_engine: MetricsEngine, event_store: EventStore) -> None:
        self.metrics_engine = metrics_engine
        self.event_store = event_store
        self.window_1m = TimeWindowAggregator(window_duration_sec=60.0)
        self.window_5m = TimeWindowAggregator(window_duration_sec=300.0)
        self.window_15m = TimeWindowAggregator(window_duration_sec=900.0)

    def process_event(self, event: BaseRuntimeEvent) -> None:
        """Processes event across all time windows and the metrics engine."""
        self.metrics_engine.handle_event(event)
        self.window_1m.add_event(event)
        self.window_5m.add_event(event)
        self.window_15m.add_event(event)

    def get_telemetry_snapshot(self) -> Dict[str, Any]:
        """Provides consolidated multi-window telemetry snapshot."""
        return {
            "summary": self.metrics_engine.get_summary(),
            "windows": {
                "1m": self.window_1m.get_summary(),
                "5m": self.window_5m.get_summary(),
                "15m": self.window_15m.get_summary(),
            },
        }
