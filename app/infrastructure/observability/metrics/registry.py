"""
Multi-Dimensional Metric Registry.

Provides thread-safe registration, label slicing, and collection of time-series metrics.
"""

from __future__ import annotations

import logging
import threading
from typing import Dict, List, Optional, Tuple
from app.infrastructure.observability.metrics.types import (
    MetricPoint,
    MetricSeries,
    MetricType,
)

logger = logging.getLogger("infrastructure.observability.metrics.registry")


class MetricRegistry:
    """
    Central registry managing multi-dimensional metric series.
    """

    def __init__(self, max_points_per_series: int = 1000) -> None:
        self.max_points_per_series = max_points_per_series
        self._lock = threading.RLock()
        self._series: Dict[str, MetricSeries] = {}  # key -> MetricSeries

    @staticmethod
    def _make_key(name: str, labels: Optional[Dict[str, str]] = None) -> str:
        if not labels:
            return name
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"

    def register_metric(
        self,
        name: str,
        metric_type: MetricType,
        description: str = "",
        unit: str = "",
        labels: Optional[Dict[str, str]] = None,
    ) -> MetricSeries:
        """Register a new metric series."""
        key = self._make_key(name, labels)
        with self._lock:
            if key not in self._series:
                self._series[key] = MetricSeries(
                    name=name,
                    metric_type=metric_type,
                    description=description,
                    unit=unit,
                    labels=labels or {},
                )
            return self._series[key]

    def record(
        self,
        name: str,
        value: float,
        metric_type: MetricType = MetricType.GAUGE,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        """Record a single metric sample point."""
        key = self._make_key(name, labels)
        with self._lock:
            if key not in self._series:
                self._series[key] = MetricSeries(
                    name=name,
                    metric_type=metric_type,
                    labels=labels or {},
                )

            series = self._series[key]
            series.points.append(MetricPoint(value=value, labels=labels or {}))

            if len(series.points) > self.max_points_per_series:
                series.points = series.points[-self.max_points_per_series:]

    def increment(self, name: str, value: float = 1.0, labels: Optional[Dict[str, str]] = None) -> None:
        """Increment a counter metric."""
        key = self._make_key(name, labels)
        with self._lock:
            if key not in self._series:
                self._series[key] = MetricSeries(
                    name=name,
                    metric_type=MetricType.COUNTER,
                    labels=labels or {},
                )
            series = self._series[key]
            current = series.points[-1].value if series.points else 0.0
            new_val = current + value
            series.points.append(MetricPoint(value=new_val, labels=labels or {}))
            if len(series.points) > self.max_points_per_series:
                series.points = series.points[-self.max_points_per_series:]

    def get_series(self, name: str, labels: Optional[Dict[str, str]] = None) -> Optional[MetricSeries]:
        key = self._make_key(name, labels)
        with self._lock:
            return self._series.get(key)

    def list_series(self, prefix: Optional[str] = None) -> List[MetricSeries]:
        with self._lock:
            if prefix:
                return [s for s in self._series.values() if s.name.startswith(prefix)]
            return list(self._series.values())

    def clear(self) -> None:
        with self._lock:
            self._series.clear()
