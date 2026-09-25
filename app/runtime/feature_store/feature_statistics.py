"""
Scientific Feature Store - Feature Statistics
Computes population statistics, rolling windows, drift metrics, and covariance matrices.
"""

from typing import Dict, List
import math


class FeatureStatisticsTracker:
    """Tracks running statistics for runtime features to detect distribution shift."""

    def __init__(self, window_size: int = 1000):
        self.window_size = window_size
        self._history: Dict[str, List[float]] = {}

    def record(self, features: Dict[str, float]) -> None:
        """Appends a new observation vector."""
        for k, v in features.items():
            if v is None or math.isnan(v):
                continue
            if k not in self._history:
                self._history[k] = []
            self._history[k].append(float(v))
            if len(self._history[k]) > self.window_size:
                self._history[k].pop(0)

    def get_summary(self, feature_name: str) -> Dict[str, float]:
        """Calculates mean, variance, std_dev, min, max, median, p95 for a feature."""
        vals = self._history.get(feature_name, [])
        if not vals:
            return {
                "count": 0,
                "mean": 0.0,
                "std": 0.0,
                "min": 0.0,
                "max": 0.0,
                "p50": 0.0,
                "p95": 0.0,
                "drift_score": 0.0,
            }

        n = len(vals)
        mean_val = sum(vals) / n
        var = sum((x - mean_val) ** 2 for x in vals) / n if n > 1 else 0.0
        std_val = math.sqrt(var)

        sorted_vals = sorted(vals)
        p50 = sorted_vals[int(n * 0.50)]
        p95 = sorted_vals[min(n - 1, int(n * 0.95))]

        # Simple drift score comparing recent 20% to overall mean
        recent_n = max(1, int(n * 0.2))
        recent_mean = sum(vals[-recent_n:]) / recent_n
        drift = abs(recent_mean - mean_val) / (std_val + 1e-9)

        return {
            "count": n,
            "mean": round(mean_val, 4),
            "std": round(std_val, 4),
            "min": round(sorted_vals[0], 4),
            "max": round(sorted_vals[-1], 4),
            "p50": round(p50, 4),
            "p95": round(p95, 4),
            "drift_score": round(drift, 4),
        }

    def get_all_summaries(self) -> Dict[str, Dict[str, float]]:
        """Returns statistical summary for all tracked features."""
        return {k: self.get_summary(k) for k in self._history.keys()}


feature_statistics_tracker = FeatureStatisticsTracker()
