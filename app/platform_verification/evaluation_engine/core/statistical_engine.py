"""
Statistical Evaluation Engine providing mean, median, variance, std dev, Wilson score confidence intervals,
sample size validation, and significance testing.
"""
from __future__ import annotations
import math
from typing import List, Optional, Tuple
from app.platform_verification.evaluation_engine.domain.models import (
    StatisticalSummary,
    ConfidenceInterval,
)
from app.platform_verification.evaluation_engine.domain.interfaces import IStatisticalEngine


class StatisticalEngine(IStatisticalEngine):
    """Statistical evaluation engine adhering to enterprise statistical validation requirements."""

    def compute_summary(self, values: List[float]) -> StatisticalSummary:
        if not values:
            return StatisticalSummary(
                mean=0.0,
                median=0.0,
                variance=0.0,
                std_dev=0.0,
                min_value=0.0,
                max_value=0.0,
                p50=0.0,
                p90=0.0,
                p95=0.0,
                p99=0.0,
                sample_size=0,
            )

        n = len(values)
        sorted_vals = sorted(values)
        mean_val = sum(values) / n

        # Median & percentiles
        median_val = self._percentile(sorted_vals, 50.0)
        p50 = median_val
        p90 = self._percentile(sorted_vals, 90.0)
        p95 = self._percentile(sorted_vals, 95.0)
        p99 = self._percentile(sorted_vals, 99.0)

        # Variance and Standard Deviation
        if n > 1:
            variance = sum((x - mean_val) ** 2 for x in values) / (n - 1)
            std_dev = math.sqrt(variance)
        else:
            variance = 0.0
            std_dev = 0.0

        # Normal Confidence Interval for continuous variables
        ci: Optional[ConfidenceInterval] = None
        if n >= 2:
            z = 1.96  # 95% confidence
            margin = z * (std_dev / math.sqrt(n))
            ci = ConfidenceInterval(
                metric_name="continuous_mean",
                value=mean_val,
                confidence_level=0.95,
                lower_bound=max(0.0, mean_val - margin),
                upper_bound=mean_val + margin,
                sample_size=n,
                method="normal_distribution",
            )

        return StatisticalSummary(
            mean=round(mean_val, 4),
            median=round(median_val, 4),
            variance=round(variance, 4),
            std_dev=round(std_dev, 4),
            min_value=round(sorted_vals[0], 4),
            max_value=round(sorted_vals[-1], 4),
            p50=round(p50, 4),
            p90=round(p90, 4),
            p95=round(p95, 4),
            p99=round(p99, 4),
            sample_size=n,
            confidence_interval=ci,
        )

    def compute_wilson_confidence_interval(
        self, successes: int, total: int, confidence: float = 0.95
    ) -> ConfidenceInterval:
        """Wilson score interval with continuity correction for proportions/percentages."""
        if total <= 0:
            return ConfidenceInterval(
                metric_name="proportion",
                value=0.0,
                confidence_level=confidence,
                lower_bound=0.0,
                upper_bound=0.0,
                sample_size=0,
                method="wilson_score",
            )

        successes = max(0, min(total, successes))
        p = successes / total
        z = 1.95996 if confidence == 0.95 else (2.57583 if confidence == 0.99 else 1.64485)
        z2 = z * z

        denominator = 1 + z2 / total
        centre_adjusted_probability = p + z2 / (2 * total)
        variance_term = max(0.0, (p * (1 - p) + z2 / (4 * total)) / total)
        adjusted_standard_deviation = math.sqrt(variance_term)

        lower_bound = (centre_adjusted_probability - z * adjusted_standard_deviation) / denominator
        upper_bound = (centre_adjusted_probability + z * adjusted_standard_deviation) / denominator

        lower_pct = max(0.0, min(100.0, lower_bound * 100.0))
        upper_pct = max(0.0, min(100.0, upper_bound * 100.0))
        value_pct = p * 100.0

        return ConfidenceInterval(
            metric_name="proportion",
            value=round(value_pct, 2),
            confidence_level=confidence,
            lower_bound=round(lower_pct, 2),
            upper_bound=round(upper_pct, 2),
            sample_size=total,
            method="wilson_score",
        )

    def validate_sample_size(self, sample_size: int, min_required: int = 30) -> bool:
        """Validates whether sample size meets statistical power requirements."""
        return sample_size >= min_required

    def test_significance(
        self, baseline_values: List[float], candidate_values: List[float]
    ) -> Tuple[float, float, bool]:
        """Performs two-sample independent Welch's t-test approximation."""
        n1, n2 = len(baseline_values), len(candidate_values)
        if n1 < 2 or n2 < 2:
            return 0.0, 1.0, False

        m1 = sum(baseline_values) / n1
        m2 = sum(candidate_values) / n2

        v1 = sum((x - m1) ** 2 for x in baseline_values) / (n1 - 1)
        v2 = sum((x - m2) ** 2 for x in candidate_values) / (n2 - 1)

        denom = math.sqrt((v1 / n1) + (v2 / n2))
        if denom == 0:
            return 0.0, 1.0, False

        t_stat = (m2 - m1) / denom
        # Approximation of two-tailed p-value
        p_val = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(t_stat) / math.sqrt(2))))
        is_significant = p_val < 0.05
        return round(t_stat, 4), round(p_val, 4), is_significant

    def _percentile(self, sorted_vals: List[float], percentile: float) -> float:
        if not sorted_vals:
            return 0.0
        k = (len(sorted_vals) - 1) * (percentile / 100.0)
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return sorted_vals[int(k)]
        d0 = sorted_vals[int(f)] * (c - k)
        d1 = sorted_vals[int(c)] * (k - f)
        return d0 + d1
