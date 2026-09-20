"""
Time-Series Metrics Aggregator & Percentile Calculator.

Calculates rollups, percentiles (p50, p90, p95, p99, p99.9), rates, and moving averages.
"""

from __future__ import annotations

import math
import time
from typing import List, Optional
from app.infrastructure.observability.metrics.types import (
    AggregatedMetricSummary,
    MetricPoint,
    MetricSeries,
)


class TimeWindowAggregator:
    """
    Computes statistical rollups over time-series metric buffers.
    """

    @staticmethod
    def _percentile(sorted_values: List[float], p: float) -> float:
        if not sorted_values:
            return 0.0
        k = (len(sorted_values) - 1) * (p / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return sorted_values[int(k)]
        d0 = sorted_values[int(f)] * (c - k)
        d1 = sorted_values[int(c)] * (k - f)
        return d0 + d1

    @classmethod
    def aggregate(
        cls,
        series: MetricSeries,
        window_seconds: float = 300.0,
        now: Optional[float] = None,
    ) -> AggregatedMetricSummary:
        """Calculate statistical summary for a metric series over the specified lookback window."""
        current_time = now or time.time()
        start_time = current_time - window_seconds

        # Filter points within window
        window_points = [pt for pt in series.points if pt.timestamp >= start_time]
        if not window_points:
            return AggregatedMetricSummary(
                name=series.name,
                count=0,
                sum=0.0,
                min=0.0,
                max=0.0,
                avg=0.0,
                p50=0.0,
                p90=0.0,
                p95=0.0,
                p99=0.0,
                p999=0.0,
                rate_per_sec=0.0,
            )

        values = [pt.value for pt in window_points]
        sorted_vals = sorted(values)
        total = sum(values)
        count = len(values)
        avg = total / count

        time_span = max(1.0, window_points[-1].timestamp - window_points[0].timestamp)
        rate = count / time_span if len(window_points) > 1 else (count / window_seconds)

        return AggregatedMetricSummary(
            name=series.name,
            count=count,
            sum=round(total, 4),
            min=round(min(values), 4),
            max=round(max(values), 4),
            avg=round(avg, 4),
            p50=round(cls._percentile(sorted_vals, 50.0), 4),
            p90=round(cls._percentile(sorted_vals, 90.0), 4),
            p95=round(cls._percentile(sorted_vals, 95.0), 4),
            p99=round(cls._percentile(sorted_vals, 99.0), 4),
            p999=round(cls._percentile(sorted_vals, 99.9), 4),
            rate_per_sec=round(rate, 4),
        )
