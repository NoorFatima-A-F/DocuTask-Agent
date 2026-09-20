"""Golden Signals Telemetry & Latency Percentile Aggregators."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class MeshMetricsSummary:
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    error_rate_pct: float = 0.0
    req_per_sec: float = 0.0
    p50_latency_ms: float = 0.0
    p90_latency_ms: float = 0.0
    p95_latency_ms: float = 0.0
    p99_latency_ms: float = 0.0
    max_latency_ms: float = 0.0


class MeshMetricsCollector:
    """Collects golden signals (latency percentiles, traffic, error rates) for service-to-service calls."""

    def __init__(self, max_sample_size: int = 5000):
        self.max_sample_size = max_sample_size
        # key: f"{source}->{target}" or "global"
        self._latencies: Dict[str, List[float]] = {}
        self._status_counts: Dict[str, Dict[int, int]] = {}
        self._first_recorded: Optional[float] = None
        self._last_recorded: Optional[float] = None

    def record_call(
        self,
        source_service: str,
        target_service: str,
        status_code: int,
        duration_ms: float,
    ) -> None:
        """Record a single service-to-service communication event."""
        now = time.time()
        if self._first_recorded is None:
            self._first_recorded = now
        self._last_recorded = now

        key = f"{source_service}->{target_service}"
        for k in [key, "global", f"target:{target_service}"]:
            if k not in self._latencies:
                self._latencies[k] = []
                self._status_counts[k] = {}

            self._latencies[k].append(duration_ms)
            if len(self._latencies[k]) > self.max_sample_size:
                self._latencies[k].pop(0)

            self._status_counts[k][status_code] = self._status_counts[k].get(status_code, 0) + 1

    def get_summary(self, dimension_key: str = "global") -> MeshMetricsSummary:
        """Calculate and return Golden Signals metrics summary for the given key."""
        latencies = self._latencies.get(dimension_key, [])
        status_map = self._status_counts.get(dimension_key, {})

        if not latencies:
            return MeshMetricsSummary()

        total_reqs = len(latencies)
        failed_reqs = sum(cnt for code, cnt in status_map.items() if code >= 400)
        success_reqs = total_reqs - failed_reqs
        error_rate = (failed_reqs / total_reqs) * 100.0

        time_window = max(1.0, (self._last_recorded or time.time()) - (self._first_recorded or time.time()))
        rps = total_reqs / time_window

        sorted_lat = sorted(latencies)
        p50 = self._percentile(sorted_lat, 50)
        p90 = self._percentile(sorted_lat, 90)
        p95 = self._percentile(sorted_lat, 95)
        p99 = self._percentile(sorted_lat, 99)
        max_lat = sorted_lat[-1]

        return MeshMetricsSummary(
            total_requests=total_reqs,
            successful_requests=success_reqs,
            failed_requests=failed_reqs,
            error_rate_pct=round(error_rate, 2),
            req_per_sec=round(rps, 2),
            p50_latency_ms=round(p50, 2),
            p90_latency_ms=round(p90, 2),
            p95_latency_ms=round(p95, 2),
            p99_latency_ms=round(p99, 2),
            max_latency_ms=round(max_lat, 2),
        )

    def _percentile(self, sorted_list: List[float], pct: int) -> float:
        if not sorted_list:
            return 0.0
        idx = int(math.ceil((pct / 100.0) * len(sorted_list))) - 1
        return sorted_list[max(0, min(idx, len(sorted_list) - 1))]
