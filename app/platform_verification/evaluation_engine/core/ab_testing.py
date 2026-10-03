"""
A/B Evaluation Framework for comparing models, prompts, architectures, and configs.
"""
from __future__ import annotations
import math
from typing import List, Tuple
from app.platform_verification.evaluation_engine.domain.models import ABComparisonResult
from app.platform_verification.evaluation_engine.domain.interfaces import IABTestingEngine
from app.platform_verification.evaluation_engine.core.statistical_engine import StatisticalEngine


class ABTestingEngine(IABTestingEngine):
    """Executes rigorous A/B comparisons with two-sample significance tests."""

    def __init__(self, stat_engine: Optional[StatisticalEngine] = None) -> None:
        self.stat_engine = stat_engine or StatisticalEngine()

    def compare_variants(
        self,
        variant_a_name: str,
        values_a: List[float],
        variant_b_name: str,
        values_b: List[float],
        metric_name: str = "Accuracy",
    ) -> ABComparisonResult:
        n_a, n_b = len(values_a), len(values_b)
        mean_a = (sum(values_a) / n_a) if n_a > 0 else 0.0
        mean_b = (sum(values_b) / n_b) if n_b > 0 else 0.0

        delta_abs = round(mean_b - mean_a, 4)
        delta_pct = round((delta_abs / mean_a * 100.0), 2) if mean_a != 0 else 0.0

        t_stat, p_val, is_sig = self.stat_engine.test_significance(values_a, values_b)

        if is_sig and delta_abs > 0:
            winner = variant_b_name
            analysis = f"{variant_b_name} statistically outperformed {variant_a_name} (p={p_val:.4f} < 0.05, +{delta_pct}% improvement)."
        elif is_sig and delta_abs < 0:
            winner = variant_a_name
            analysis = f"{variant_a_name} statistically outperformed {variant_b_name} (p={p_val:.4f} < 0.05, {delta_pct}% drop)."
        else:
            winner = "TIE (No statistical difference)"
            analysis = f"No statistically significant difference between variants (p={p_val:.4f} >= 0.05)."

        return ABComparisonResult(
            variant_a=variant_a_name,
            variant_b=variant_b_name,
            metric_name=metric_name,
            value_a=round(mean_a, 2),
            value_b=round(mean_b, 2),
            delta_absolute=delta_abs,
            delta_percentage=delta_pct,
            t_statistic=t_stat,
            p_value=p_val,
            is_significant=is_sig,
            winner=winner,
            analysis=analysis,
        )
