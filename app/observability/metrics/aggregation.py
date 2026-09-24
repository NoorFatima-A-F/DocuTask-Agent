"""Rolling Window Metric Aggregations, Percentiles, and Rate Calculations."""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class AggregatedWindow:
    count: int = 0
    sum_val: float = 0.0
    min_val: float = float("inf")
    max_val: float = float("-inf")
    avg_val: float = 0.0
    rate_per_sec: float = 0.0
    p50: float = 0.0
    p90: float = 0.0
    p95: float = 0.0
    p99: float = 0.0


class RollingAggregationEngine:
    """Calculates time-windowed metric rollups and percentiles over streaming samples."""

    def __init__(self, window_seconds: float = 60.0):
        self.window_seconds = window_seconds
        # key -> list of (timestamp, value)
        self._samples: Dict[str, List[Tuple[float, float]]] = {}

    def record(self, metric_name: str, value: float, timestamp: Optional[float] = None) -> None:
        ts = timestamp or time.time()
        if metric_name not in self._samples:
            self._samples[metric_name] = []
        self._samples[metric_name].append((ts, value))

    def _prune(self, metric_name: str, current_time: float) -> None:
        if metric_name not in self._samples:
            return
        cutoff = current_time - self.window_seconds
        self._samples[metric_name] = [
            (ts, val) for ts, val in self._samples[metric_name] if ts >= cutoff
        ]

    def aggregate(self, metric_name: str, current_time: Optional[float] = None) -> AggregatedWindow:
        now = current_time or time.time()
        self._prune(metric_name, now)

        samples = [val for _, val in self._samples.get(metric_name, [])]
        if not samples:
            return AggregatedWindow(min_val=0.0, max_val=0.0)

        count = len(samples)
        total = sum(samples)
        min_v = min(samples)
        max_v = max(samples)
        avg_v = total / count
        rate = count / max(1.0, self.window_seconds)

        sorted_s = sorted(samples)
        p50 = self._pct(sorted_s, 0.50)
        p90 = self._pct(sorted_s, 0.90)
        p95 = self._pct(sorted_s, 0.95)
        p99 = self._pct(sorted_s, 0.99)

        return AggregatedWindow(
            count=count,
            sum_val=round(total, 4),
            min_val=round(min_v, 4),
            max_val=round(max_v, 4),
            avg_val=round(avg_v, 4),
            rate_per_sec=round(rate, 4),
            p50=round(p50, 4),
            p90=round(p90, 4),
            p95=round(p95, 4),
            p99=round(p99, 4),
        )

    def _pct(self, sorted_list: List[float], percentile: float) -> float:
        if not sorted_list:
            return 0.0
        idx = int(math.ceil(percentile * len(sorted_list))) - 1
        return sorted_list[max(0, min(idx, len(sorted_list) - 1))]
