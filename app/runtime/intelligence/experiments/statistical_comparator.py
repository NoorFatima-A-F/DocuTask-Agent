"""
Statistical Comparator for Phase 10 (AISLCOP).

Implements rigorous two-sample Welch's t-test, p-value calculations, confidence
intervals, and Cohen's d effect sizes for A/B experiment evaluation.
"""

from __future__ import annotations

import math
from typing import List, Tuple

from app.runtime.intelligence.experiments.experiment_model import (
    StatisticalComparisonResult,
)


class StatisticalComparator:
    """
    Computes statistical significance metrics between Control and Candidate distributions.
    """

    @staticmethod
    def _mean_and_var(values: List[float]) -> Tuple[float, float]:
        n = len(values)
        if n == 0:
            return 0.0, 0.0
        mean = sum(values) / n
        if n < 2:
            return mean, 0.0
        variance = sum((x - mean) ** 2 for x in values) / (n - 1)
        return mean, variance

    @classmethod
    def compare_metrics(
        cls,
        metric_name: str,
        control_values: List[float],
        candidate_values: List[float],
        higher_is_better: bool = False,
    ) -> StatisticalComparisonResult:
        n1 = len(control_values)
        n2 = len(candidate_values)

        if n1 == 0 or n2 == 0:
            return StatisticalComparisonResult(
                metric_name=metric_name,
                control_mean=0.0,
                candidate_mean=0.0,
                delta_abs=0.0,
                delta_pct=0.0,
                t_statistic=0.0,
                p_value=1.0,
                is_significant=False,
                cohens_d=0.0,
                ci_lower=0.0,
                ci_upper=0.0,
            )

        m1, v1 = cls._mean_and_var(control_values)
        m2, v2 = cls._mean_and_var(candidate_values)

        delta_abs = m2 - m1
        delta_pct = (delta_abs / max(abs(m1), 1e-9)) * 100.0

        # Standard Error of Difference (Welch's formula)
        se_sq = (v1 / max(n1, 1)) + (v2 / max(n2, 1))
        se = math.sqrt(max(se_sq, 1e-12))

        t_stat = (m2 - m1) / se if se > 0 else 0.0

        # Approximate p-value from t-statistic using normal distribution approximation
        z = abs(t_stat)
        # Accurate standard normal CDF approximation (Abramowitz and Stegun)
        t = 1.0 / (1.0 + 0.2316419 * z)
        poly = t * (0.319381530 + t * (-0.356563782 + t * (1.781477937 + t * (-1.821255978 + 1.330274429 * t))))
        one_tail_prob = (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * z * z) * poly
        p_val = min(1.0, max(1e-6, 2.0 * one_tail_prob))

        # Cohen's d effect size
        pooled_sd = math.sqrt(max(1e-12, ((n1 - 1) * v1 + (n2 - 1) * v2) / max(1, n1 + n2 - 2)))
        cohens_d = (m2 - m1) / pooled_sd if pooled_sd > 0 else 0.0

        # 95% Confidence Interval for the difference
        ci_lower = delta_abs - 1.96 * se
        ci_upper = delta_abs + 1.96 * se

        is_sig = bool(p_val < 0.05)
        # For lower-is-better (e.g. latency, cost, retries), improvement means candidate < control
        if not higher_is_better and delta_abs >= 0:
            is_sig = False
        elif higher_is_better and delta_abs <= 0:
            is_sig = False

        return StatisticalComparisonResult(
            metric_name=metric_name,
            control_mean=round(m1, 4),
            candidate_mean=round(m2, 4),
            delta_abs=round(delta_abs, 4),
            delta_pct=round(delta_pct, 2),
            t_statistic=round(t_stat, 4),
            p_value=round(p_val, 6),
            is_significant=is_sig,
            cohens_d=round(cohens_d, 4),
            ci_lower=round(ci_lower, 4),
            ci_upper=round(ci_upper, 4),
        )
