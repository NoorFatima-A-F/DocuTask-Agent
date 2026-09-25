"""
Runtime Metrics Registry.

Thread-safe metrics registry managing time-series counters, gauges, histograms,
exponential moving averages (EMA), and percentiles ($P_{50}, P_{90}, P_{99}$).
All metric values are updated by deterministic event consumers.
"""

from __future__ import annotations

import collections
import math
import threading
from typing import Dict, Optional
from app.runtime.observability.schemas import MetricRecord


class Counter:
    """Monotonically increasing 64-bit integer counter."""

    def __init__(self, name: str, unit: str = "count") -> None:
        self.name = name
        self.unit = unit
        self._value: float = 0.0
        self._lock = threading.Lock()

    def inc(self, amount: float = 1.0) -> float:
        with self._lock:
            self._value += amount
            return self._value

    @property
    def value(self) -> float:
        with self._lock:
            return self._value


class Gauge:
    """Instantaneous numerical value gauge."""

    def __init__(self, name: str, unit: str = "gauge") -> None:
        self.name = name
        self.unit = unit
        self._value: float = 0.0
        self._lock = threading.Lock()

    def set(self, val: float) -> None:
        with self._lock:
            self._value = val

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
    """Reservoir-sampled time-series histogram for latency and distribution metrics."""

    def __init__(self, name: str, unit: str = "ms", max_samples: int = 2048) -> None:
        self.name = name
        self.unit = unit
        self._samples: collections.deque[float] = collections.deque(maxlen=max_samples)
        self._lock = threading.Lock()

    def observe(self, value: float) -> None:
        with self._lock:
            self._samples.append(value)

    def get_percentile(self, p: float) -> float:
        """Returns the p-th percentile (0.0 <= p <= 100.0)."""
        with self._lock:
            if not self._samples:
                return 0.0
            sorted_samples = sorted(self._samples)
            k = (len(sorted_samples) - 1) * (p / 100.0)
            f = math.floor(k)
            c = math.ceil(k)
            if f == c:
                return float(sorted_samples[int(k)])
            d0 = sorted_samples[int(f)] * (c - k)
            d1 = sorted_samples[int(c)] * (k - f)
            return float(d0 + d1)

    def get_mean(self) -> float:
        with self._lock:
            if not self._samples:
                return 0.0
            return sum(self._samples) / len(self._samples)

    def get_stddev(self) -> float:
        with self._lock:
            if len(self._samples) < 2:
                return 0.0
            mean = sum(self._samples) / len(self._samples)
            var = sum((x - mean) ** 2 for x in self._samples) / (len(self._samples) - 1)
            return math.sqrt(var)

    def count(self) -> int:
        with self._lock:
            return len(self._samples)


class ExponentialMovingAverage:
    """Exponential Moving Average (EMA) with smoothing factor alpha."""

    def __init__(self, alpha: float = 0.2) -> None:
        self.alpha = alpha
        self._ema: Optional[float] = None
        self._lock = threading.Lock()

    def update(self, value: float) -> float:
        with self._lock:
            if self._ema is None:
                self._ema = value
            else:
                self._ema = self.alpha * value + (1.0 - self.alpha) * self._ema
            return self._ema

    @property
    def value(self) -> float:
        with self._lock:
            return self._ema if self._ema is not None else 0.0


class MetricsRegistry:
    """Global registry for runtime metrics."""

    def __init__(self) -> None:
        self._counters: Dict[str, Counter] = {}
        self._gauges: Dict[str, Gauge] = {}
        self._histograms: Dict[str, Histogram] = {}
        self._emas: Dict[str, ExponentialMovingAverage] = {}
        self._records_history: collections.deque[MetricRecord] = collections.deque(maxlen=10000)
        self._lock = threading.Lock()

    def counter(self, name: str, unit: str = "count") -> Counter:
        with self._lock:
            if name not in self._counters:
                self._counters[name] = Counter(name, unit)
            return self._counters[name]

    def gauge(self, name: str, unit: str = "gauge") -> Gauge:
        with self._lock:
            if name not in self._gauges:
                self._gauges[name] = Gauge(name, unit)
            return self._gauges[name]

    def histogram(self, name: str, unit: str = "ms") -> Histogram:
        with self._lock:
            if name not in self._histograms:
                self._histograms[name] = Histogram(name, unit)
            return self._histograms[name]

    def ema(self, name: str, alpha: float = 0.2) -> ExponentialMovingAverage:
        with self._lock:
            if name not in self._emas:
                self._emas[name] = ExponentialMovingAverage(alpha)
            return self._emas[name]

    def record_snapshot(self, record: MetricRecord) -> None:
        with self._lock:
            self._records_history.append(record)

    def get_all_metrics_dict(self) -> Dict[str, float]:
        """Returns snapshot dictionary of all registered metrics."""
        result: Dict[str, float] = {}
        with self._lock:
            for k, c in self._counters.items():
                result[k] = c.value
            for k, g in self._gauges.items():
                result[k] = g.value
            for k, h in self._histograms.items():
                result[f"{k}_p50"] = h.get_percentile(50)
                result[f"{k}_p90"] = h.get_percentile(90)
                result[f"{k}_p99"] = h.get_percentile(99)
                result[f"{k}_mean"] = h.get_mean()
            for k, e in self._emas.items():
                result[f"{k}_ema"] = e.value
        return result
