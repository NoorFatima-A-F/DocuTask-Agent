"""
Enterprise Observability Metrics Framework.
Provides Counter, Gauge, Histogram, Timer metrics primitives and registry.
"""

from collections import defaultdict
import time
from typing import Any, Dict, List, Optional


class Counter:
    """Monotonically increasing numeric counter."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self._values: Dict[str, float] = defaultdict(float)

    def inc(self, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._format_labels(labels)
        self._values[key] += value

    def get_value(self, labels: Optional[Dict[str, str]] = None) -> float:
        key = self._format_labels(labels)
        return self._values[key]

    def _format_labels(self, labels: Optional[Dict[str, str]]) -> str:
        if not labels:
            return ""
        return ",".join(f"{k}={v}" for k, v in sorted(labels.items()))


class Gauge:
    """Instantaneous numeric gauge."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self._values: Dict[str, float] = defaultdict(float)

    def set(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._format_labels(labels)
        self._values[key] = value

    def inc(self, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._format_labels(labels)
        self._values[key] += value

    def dec(self, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._format_labels(labels)
        self._values[key] -= value

    def get_value(self, labels: Optional[Dict[str, str]] = None) -> float:
        key = self._format_labels(labels)
        return self._values[key]

    def _format_labels(self, labels: Optional[Dict[str, str]]) -> str:
        if not labels:
            return ""
        return ",".join(f"{k}={v}" for k, v in sorted(labels.items()))


class Histogram:
    """Tracks distribution of sampled values (e.g., latency, token count)."""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self._samples: Dict[str, List[float]] = defaultdict(list)

    def observe(self, value: float, labels: Optional[Dict[str, str]] = None) -> None:
        key = self._format_labels(labels)
        self._samples[key].append(value)

    def get_count(self, labels: Optional[Dict[str, str]] = None) -> int:
        key = self._format_labels(labels)
        return len(self._samples[key])

    def get_sum(self, labels: Optional[Dict[str, str]] = None) -> float:
        key = self._format_labels(labels)
        return sum(self._samples[key])

    def get_avg(self, labels: Optional[Dict[str, str]] = None) -> float:
        key = self._format_labels(labels)
        s = self._samples[key]
        return sum(s) / len(s) if s else 0.0

    def _format_labels(self, labels: Optional[Dict[str, str]]) -> str:
        if not labels:
            return ""
        return ",".join(f"{k}={v}" for k, v in sorted(labels.items()))


class Timer:
    """Context manager for timing execution duration."""

    def __init__(self, histogram: Histogram, labels: Optional[Dict[str, str]] = None):
        self.histogram = histogram
        self.labels = labels
        self.start_time: float = 0.0

    def __enter__(self) -> "Timer":
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        duration_ms = (time.perf_counter() - self.start_time) * 1000.0
        self.histogram.observe(duration_ms, labels=self.labels)


class MetricsRegistry:
    """Central registry of platform metrics."""

    def __init__(self):
        self._counters: Dict[str, Counter] = {}
        self._gauges: Dict[str, Gauge] = {}
        self._histograms: Dict[str, Histogram] = {}
        self._init_standard_metrics()

    def counter(self, name: str, description: str = "") -> Counter:
        if name not in self._counters:
            self._counters[name] = Counter(name, description)
        return self._counters[name]

    def gauge(self, name: str, description: str = "") -> Gauge:
        if name not in self._gauges:
            self._gauges[name] = Gauge(name, description)
        return self._gauges[name]

    def histogram(self, name: str, description: str = "") -> Histogram:
        if name not in self._histograms:
            self._histograms[name] = Histogram(name, description)
        return self._histograms[name]

    def timer(self, name: str, labels: Optional[Dict[str, str]] = None) -> Timer:
        hist = self.histogram(name)
        return Timer(hist, labels=labels)

    def _init_standard_metrics(self) -> None:
        """Initialize standard platform, AI, and workflow metrics."""
        self.counter("platform_http_requests_total", "Total incoming HTTP requests")
        self.counter("platform_errors_total", "Total platform errors")
        self.gauge("platform_active_workers", "Currently active workers")
        self.histogram("platform_request_latency_ms", "HTTP request latency in ms")
        self.counter("ai_tokens_consumed_total", "Total LLM tokens consumed")
        self.counter("ai_cost_cents_total", "Total estimated AI cost in cents")
        self.counter("workflow_executions_total", "Total workflow executions")
        self.counter("workflow_failures_total", "Total workflow failures")
        self.histogram("workflow_duration_seconds", "Workflow execution duration")
