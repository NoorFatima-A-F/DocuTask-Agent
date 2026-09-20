"""
Time-Series Health Storage (Part 3H.3.4.2).
Provides in-memory time-series storage, sliding-window retention,
and statistical aggregation (mean, standard deviation, linear slope).
"""
import math
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.platform_verification.predictive_health_intelligence.domain.models import TelemetryItem


class TimeSeriesHealthStore:
    """
    Time-series repository for historical health signals.
    """

    def __init__(self, max_points_per_metric: int = 1000):
        self.max_points = max_points_per_metric
        self._series: Dict[str, List[TelemetryItem]] = {}

    def ingest_point(self, item: TelemetryItem):
        key = f"{item.service}.{item.metric}"
        if key not in self._series:
            self._series[key] = []
        self._series[key].append(item)
        if len(self._series[key]) > self.max_points:
            self._series[key].pop(0)

    def get_points(self, service: str, metric: str) -> List[TelemetryItem]:
        key = f"{service}.{metric}"
        return list(self._series.get(key, []))

    def compute_statistics(self, service: str, metric: str) -> Dict[str, float]:
        points = self.get_points(service, metric)
        if not points:
            return {"count": 0, "mean": 0.0, "std_dev": 0.0, "slope": 0.0, "latest": 0.0}

        values = [p.value for p in points]
        n = len(values)
        mean = sum(values) / float(n)
        variance = sum((x - mean) ** 2 for x in values) / float(n) if n > 1 else 0.0
        std_dev = math.sqrt(variance)

        # Simple linear slope: (latest - first) / n
        slope = (values[-1] - values[0]) / float(n) if n > 1 else 0.0

        return {
            "count": float(n),
            "mean": round(mean, 2),
            "std_dev": round(std_dev, 2),
            "slope": round(slope, 3),
            "latest": round(values[-1], 2),
        }
