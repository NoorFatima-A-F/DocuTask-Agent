"""Metric Types and Thread-Safe Metric Registry."""

from __future__ import annotations

import bisect
import math
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class MetricType(str, Enum):
    COUNTER = "COUNTER"
    GAUGE = "GAUGE"
    HISTOGRAM = "HISTOGRAM"
    SUMMARY = "SUMMARY"


def _format_labels(labels: Optional[Dict[str, str]]) -> str:
    if not labels:
        return ""
    return ",".join(f"{k}={v}" for k, v in sorted(labels.items()))


class Counter:
    """Monotonically increasing cumulative metric."""

    def __init__(self, name: str, description: str = "", labels: Optional[Dict[str, str]] = None):
        self.name = name
        self.description = description
        self.labels = labels or {}
        self._value: float = 0.0
        self._lock = threading.Lock()

    def inc(self, amount: float = 1.0) -> None:
        if amount < 0:
            raise ValueError("Counter increments must be non-negative")
        with self._lock:
            self._value += amount

    @property
    def value(self) -> float:
        with self._lock:
            return self._value


class Gauge:
    """Instantaneous numerical value that can go up or down."""

    def __init__(self, name: str, description: str = "", labels: Optional[Dict[str, str]] = None):
        self.name = name
        self.description = description
        self.labels = labels or {}
        self._value: float = 0.0
        self._lock = threading.Lock()

    def set(self, value: float) -> None:
        with self._lock:
            self._value = value

    def inc(self, amount: float = 1.0) -> None:
        with self._lock:
            self._value += amount

    def dec(self, amount: float = 1.0) -> None:
        with self._lock:
            self._value -= amount

    @property
    def value(self) -> float:
        with self._lock:
            return self._value


class Histogram:
    """Samples observations (usually durations or sizes) into configurable buckets."""

    def __init__(
        self,
        name: str,
        description: str = "",
        buckets: Optional[List[float]] = None,
        labels: Optional[Dict[str, str]] = None,
    ):
        self.name = name
        self.description = description
        self.labels = labels or {}
        self.buckets = sorted(buckets or [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0])
        self._bucket_counts: Dict[float, int] = {b: 0 for b in self.buckets}
        self._bucket_counts[float("inf")] = 0
        self._count: int = 0
        self._sum: float = 0.0
        self._samples: List[float] = []
        self._lock = threading.Lock()

    def observe(self, value: float) -> None:
        with self._lock:
            self._count += 1
            self._sum += value
            self._samples.append(value)
            if len(self._samples) > 2000:
                self._samples.pop(0)

            for b in self.buckets:
                if value <= b:
                    self._bucket_counts[b] += 1
            self._bucket_counts[float("inf")] += 1

    @property
    def count(self) -> int:
        with self._lock:
            return self._count

    @property
    def sum(self) -> float:
        with self._lock:
            return self._sum

    def get_percentile(self, percentile: float) -> float:
        """Compute percentile (e.g. 0.50, 0.90, 0.95, 0.99) from sample window."""
        with self._lock:
            if not self._samples:
                return 0.0
            sorted_samples = sorted(self._samples)
            idx = int(math.ceil(percentile * len(sorted_samples))) - 1
            return sorted_samples[max(0, min(idx, len(sorted_samples) - 1))]


class MetricRegistry:
    """Central registry storing and serving all active metrics."""

    def __init__(self):
        self._counters: Dict[str, Counter] = {}
        self._gauges: Dict[str, Gauge] = {}
        self._histograms: Dict[str, Histogram] = {}
        self._lock = threading.Lock()

    def counter(self, name: str, description: str = "", labels: Optional[Dict[str, str]] = None) -> Counter:
        key = f"{name}:{_format_labels(labels)}"
        with self._lock:
            if key not in self._counters:
                self._counters[key] = Counter(name, description, labels)
            return self._counters[key]

    def gauge(self, name: str, description: str = "", labels: Optional[Dict[str, str]] = None) -> Gauge:
        key = f"{name}:{_format_labels(labels)}"
        with self._lock:
            if key not in self._gauges:
                self._gauges[key] = Gauge(name, description, labels)
            return self._gauges[key]

    def histogram(
        self,
        name: str,
        description: str = "",
        buckets: Optional[List[float]] = None,
        labels: Optional[Dict[str, str]] = None,
    ) -> Histogram:
        key = f"{name}:{_format_labels(labels)}"
        with self._lock:
            if key not in self._histograms:
                self._histograms[key] = Histogram(name, description, buckets, labels)
            return self._histograms[key]

    def dump_snapshot(self) -> Dict[str, Any]:
        """Export all registered metrics into a structured telemetry dictionary."""
        with self._lock:
            return {
                "counters": {k: c.value for k, c in self._counters.items()},
                "gauges": {k: g.value for k, g in self._gauges.items()},
                "histograms": {
                    k: {
                        "count": h.count,
                        "sum": round(h.sum, 4),
                        "p50": round(h.get_percentile(0.50), 4),
                        "p90": round(h.get_percentile(0.90), 4),
                        "p95": round(h.get_percentile(0.95), 4),
                        "p99": round(h.get_percentile(0.99), 4),
                    }
                    for k, h in self._histograms.items()
                },
            }

    def clear(self) -> None:
        with self._lock:
            self._counters.clear()
            self._gauges.clear()
            self._histograms.clear()
