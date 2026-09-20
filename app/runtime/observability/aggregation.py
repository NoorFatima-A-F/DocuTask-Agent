"""
Telemetry Aggregation Layer.

Provides rolling time-window aggregations (1m, 5m, 15m, 1h) and multidimensional slices
per mission, per worker, per agent, per planner version, and per document type.
"""

from __future__ import annotations

import collections
import time
from typing import Any, Dict, List, Optional
from app.runtime.observability.mission_statistics import ObservabilityStats
from app.runtime.observability.schemas import BaseRuntimeEvent


class TimeWindowAggregator:
    """Rolling time window aggregator for streaming telemetry metrics."""

    def __init__(self, window_duration_sec: float = 60.0) -> None:
        self.window_duration_sec = window_duration_sec
        self._events: collections.deque[BaseRuntimeEvent] = collections.deque()

    def add_event(self, event: BaseRuntimeEvent) -> None:
        self._events.append(event)
        self._evict_expired(event.timestamp)

    def _evict_expired(self, current_time: Optional[float] = None) -> None:
        now = current_time or time.time()
        cutoff = now - self.window_duration_sec
        while self._events and self._events[0].timestamp < cutoff:
            self._events.popleft()

    def get_summary(self) -> Dict[str, Any]:
        self._evict_expired()
        durations = [e.duration_ms for e in self._events if e.duration_ms > 0]
        stats = ObservabilityStats.calculate_percentiles(durations)
        
        errors_count = sum(1 for e in self._events if e.status == "FAILED" or e.severity.value in ("ERROR", "CRITICAL"))
        total_count = len(self._events)
        error_rate = (errors_count / total_count) if total_count > 0 else 0.0

        return {
            "window_duration_sec": self.window_duration_sec,
            "event_count": total_count,
            "error_count": errors_count,
            "error_rate": round(error_rate, 4),
            "latency_stats": stats,
            "throughput_eps": round(total_count / max(1.0, self.window_duration_sec), 2),
        }
