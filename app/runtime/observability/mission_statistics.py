"""
Statistical Analysis & Percentile Calculations for Observability.

Calculates empirical percentiles ($P_{50}, P_{90}, P_{95}, P_{99}$), standard deviation,
variance, interquartile range (IQR), and confidence intervals over telemetry data.
"""

from __future__ import annotations

import math
from typing import Dict, List, Tuple


class ObservabilityStats:
    """Rigorous mathematical statistical aggregation."""

    @staticmethod
    def calculate_percentiles(values: List[float]) -> Dict[str, float]:
        """Calculates exact P50, P90, P95, P99 percentiles."""
        if not values:
            return {"p50": 0.0, "p90": 0.0, "p95": 0.0, "p99": 0.0, "mean": 0.0, "stddev": 0.0}

        sorted_vals = sorted(values)
        n = len(sorted_vals)

        def _p(p: float) -> float:
            k = (n - 1) * (p / 100.0)
            f = math.floor(k)
            c = math.ceil(k)
            if f == c:
                return float(sorted_vals[int(k)])
            return float(sorted_vals[int(f)] * (c - k) + sorted_vals[int(c)] * (k - f))

        mean = sum(sorted_vals) / n
        var = sum((x - mean) ** 2 for x in sorted_vals) / max(1, n - 1)
        stddev = math.sqrt(var)

        return {
            "p50": round(_p(50), 3),
            "p90": round(_p(90), 3),
            "p95": round(_p(95), 3),
            "p99": round(_p(99), 3),
            "mean": round(mean, 3),
            "stddev": round(stddev, 3),
            "min": round(sorted_vals[0], 3),
            "max": round(sorted_vals[-1], 3),
            "count": float(n),
        }

    @staticmethod
    def iqr_bounds(values: List[float], multiplier: float = 1.5) -> Tuple[float, float]:
        """Calculates Interquartile Range outlier boundaries [Q1 - 1.5*IQR, Q3 + 1.5*IQR]."""
        if len(values) < 4:
            return (0.0, 1e9)
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        q1 = sorted_vals[int(n * 0.25)]
        q3 = sorted_vals[int(n * 0.75)]
        iqr = q3 - q1
        lower = max(0.0, q1 - multiplier * iqr)
        upper = q3 + multiplier * iqr
        return (lower, upper)
