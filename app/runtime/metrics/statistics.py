"""
Scientific Statistics Engine for DocuTask Agent.
Provides exact mathematical estimators: Mean, Median, Mode, Variance, Standard Deviation,
Percentiles (p50, p90, p95, p99), Moving Average, EWMA, and 95% Confidence Intervals
using Student's t and Normal z distributions.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple


# Precomputed Student's t critical values for two-tailed alpha=0.05 (95% CI) for df=1..30
T_CRITICAL_95: Dict[int, float] = {
    1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
    6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
    11: 2.201, 12: 2.179, 13: 2.160, 14: 2.145, 15: 2.131,
    16: 2.120, 17: 2.110, 18: 2.101, 19: 2.093, 20: 2.086,
    21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064, 25: 2.060,
    26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042,
}
Z_CRITICAL_95: float = 1.959963984540054


@dataclass(frozen=True)
class StatisticalSummary:
    """
    Complete empirical distribution summary for an observable metric sample.
    """
    sample_size: int
    mean: float
    median: float
    mode: Optional[float]
    variance: float
    standard_deviation: float
    standard_error: float
    min_value: float
    max_value: float
    p50: float
    p90: float
    p95: float
    p99: float
    confidence_interval_95: Tuple[float, float]
    margin_of_error_95: float
    distribution_model: str  # "STUDENT_T" or "STANDARD_NORMAL"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_size": self.sample_size,
            "mean": self.mean,
            "median": self.median,
            "mode": self.mode,
            "variance": self.variance,
            "standard_deviation": self.standard_deviation,
            "standard_error": self.standard_error,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "p50": self.p50,
            "p90": self.p90,
            "p95": self.p95,
            "p99": self.p99,
            "confidence_interval_95": list(self.confidence_interval_95),
            "margin_of_error_95": self.margin_of_error_95,
            "distribution_model": self.distribution_model,
        }


class ScientificStatisticsEngine:
    """
    High-precision statistical processor for runtime metrics.
    """

    @staticmethod
    def calculate_percentile(sorted_data: List[float], percentile: float) -> float:
        """
        Calculates percentile using NIST linear interpolation between nearest ranks.
        """
        if not sorted_data:
            return 0.0
        n = len(sorted_data)
        if n == 1:
            return sorted_data[0]
        
        p = max(0.0, min(100.0, percentile)) / 100.0
        rank = p * (n - 1)
        low_idx = int(math.floor(rank))
        high_idx = int(math.ceil(rank))
        fraction = rank - low_idx

        if low_idx == high_idx:
            return sorted_data[low_idx]
        return sorted_data[low_idx] + fraction * (sorted_data[high_idx] - sorted_data[low_idx])

    @classmethod
    def analyze_sample(cls, values: List[float]) -> Optional[StatisticalSummary]:
        """
        Produces complete statistical analysis for a list of observed metric values.
        """
        if not values:
            return None

        n = len(values)
        sorted_vals = sorted(values)
        sample_mean = sum(values) / float(n)
        min_val = sorted_vals[0]
        max_val = sorted_vals[-1]

        # Median
        if n % 2 == 1:
            median_val = sorted_vals[n // 2]
        else:
            median_val = (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2.0

        # Mode (approximate via frequency binning)
        freq: Dict[float, int] = {}
        for v in values:
            rounded = round(v, 4)
            freq[rounded] = freq.get(rounded, 0) + 1
        sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        mode_val = sorted_freq[0][0] if sorted_freq and sorted_freq[0][1] > 1 else None

        # Sample Variance and Standard Deviation (Bessel's correction n - 1 for n > 1)
        if n > 1:
            variance_val = sum((x - sample_mean) ** 2 for x in values) / float(n - 1)
            stdev_val = math.sqrt(variance_val)
        else:
            variance_val = 0.0
            stdev_val = 0.0

        standard_error = stdev_val / math.sqrt(n) if n > 0 else 0.0

        # 95% Confidence Interval calculation
        if n >= 30:
            crit = Z_CRITICAL_95
            model = "STANDARD_NORMAL"
        elif n > 1:
            df = min(30, n - 1)
            crit = T_CRITICAL_95.get(df, 2.042)
            model = "STUDENT_T"
        else:
            crit = 0.0
            model = "SINGLETON_ESTIMATE"

        margin_of_error = crit * standard_error
        ci_lower = sample_mean - margin_of_error
        ci_upper = sample_mean + margin_of_error

        # Percentiles
        p50 = cls.calculate_percentile(sorted_vals, 50.0)
        p90 = cls.calculate_percentile(sorted_vals, 90.0)
        p95 = cls.calculate_percentile(sorted_vals, 95.0)
        p99 = cls.calculate_percentile(sorted_vals, 99.0)

        return StatisticalSummary(
            sample_size=n,
            mean=sample_mean,
            median=median_val,
            mode=mode_val,
            variance=variance_val,
            standard_deviation=stdev_val,
            standard_error=standard_error,
            min_value=min_val,
            max_value=max_val,
            p50=p50,
            p90=p90,
            p95=p95,
            p99=p99,
            confidence_interval_95=(ci_lower, ci_upper),
            margin_of_error_95=margin_of_error,
            distribution_model=model,
        )

    @staticmethod
    def calculate_ewma(values: List[float], alpha: float = 0.3) -> List[float]:
        """
        Calculates Exponentially Weighted Moving Average across a time-series.
        S_t = alpha * Y_t + (1 - alpha) * S_{t-1}
        """
        if not values:
            return []
        alpha = max(0.01, min(1.0, alpha))
        ewma_series: List[float] = [values[0]]
        for val in values[1:]:
            s_prev = ewma_series[-1]
            s_curr = alpha * val + (1.0 - alpha) * s_prev
            ewma_series.append(s_curr)
        return ewma_series
