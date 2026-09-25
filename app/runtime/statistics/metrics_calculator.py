"""
Scientific Statistics - Metrics Calculator
Calculates summary percentiles, variance, skewness, kurtosis, and confidence intervals.
"""

from typing import List, Dict
import math


class MetricsCalculator:
    """Calculates defensible descriptive metrics for platform telemetry."""

    @staticmethod
    def compute_summary(values: List[float]) -> Dict[str, float]:
        if not values:
            return {
                "count": 0,
                "mean": 0.0,
                "std": 0.0,
                "min": 0.0,
                "max": 0.0,
                "p50": 0.0,
                "p90": 0.0,
                "p95": 0.0,
                "p99": 0.0,
                "skewness": 0.0,
                "kurtosis": 0.0,
            }

        n = len(values)
        sorted_v = sorted(values)
        mean_v = sum(values) / n
        var = sum((x - mean_v) ** 2 for x in values) / n
        std_v = math.sqrt(var)

        # Skewness
        m3 = sum((x - mean_v) ** 3 for x in values) / n
        skew = m3 / (std_v ** 3 + 1e-9)

        # Kurtosis
        m4 = sum((x - mean_v) ** 4 for x in values) / n
        kurt = (m4 / (std_v ** 4 + 1e-9)) - 3.0

        return {
            "count": n,
            "mean": round(mean_v, 4),
            "std": round(std_v, 4),
            "min": round(sorted_v[0], 4),
            "max": round(sorted_v[-1], 4),
            "p50": round(sorted_v[int(n * 0.50)], 4),
            "p90": round(sorted_v[min(n - 1, int(n * 0.90))], 4),
            "p95": round(sorted_v[min(n - 1, int(n * 0.95))], 4),
            "p99": round(sorted_v[min(n - 1, int(n * 0.99))], 4),
            "skewness": round(skew, 4),
            "kurtosis": round(kurt, 4),
        }
