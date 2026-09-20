"""
Scientific Benchmark Engine - Benchmark Statistics
Calculates empirical win rates, utility improvements, and hypothesis test p-values against baselines.
"""

from typing import Dict, List, Any
import math


class BenchmarkStatistics:
    """Computes rigorous benchmarking differentials and effect sizes."""

    @staticmethod
    def compute_comparative_stats(
        optimizer_scores: List[float],
        baseline_scores: List[float],
    ) -> Dict[str, Any]:
        if not optimizer_scores or not baseline_scores:
            return {}

        n = min(len(optimizer_scores), len(baseline_scores))
        opt_s = optimizer_scores[:n]
        base_s = baseline_scores[:n]

        mean_opt = sum(opt_s) / n
        mean_base = sum(base_s) / n

        # Wins count
        wins = sum(1 for o, b in zip(opt_s, base_s) if o > b)
        win_rate = (wins / n) * 100.0

        # Percent utility gain
        delta = mean_opt - mean_base
        gain_pct = (delta / (mean_base + 1e-6)) * 100.0

        # Paired differences variance for t-test
        diffs = [o - b for o, b in zip(opt_s, base_s)]
        diff_mean = sum(diffs) / n
        diff_var = sum((d - diff_mean) ** 2 for d in diffs) / (n - 1) if n > 1 else 1e-6
        diff_std = math.sqrt(diff_var)

        # Student's t-statistic: t = diff_mean / (std / sqrt(n))
        se = diff_std / math.sqrt(n) if n > 0 else 1.0
        t_stat = diff_mean / (se + 1e-9)

        # Approximate p-value (standard normal for n >= 20)
        # Using complementary error function approx: p ~ 2 * (1 - Phi(|t|))
        z = abs(t_stat)
        p_val = math.erfc(z / math.sqrt(2.0))

        # Cohen's d effect size: delta / pooled_std
        cohens_d = delta / (diff_std + 1e-9)

        return {
            "sample_size": n,
            "optimizer_mean_utility": round(mean_opt, 4),
            "baseline_mean_utility": round(mean_base, 4),
            "utility_gain_percent": round(gain_pct, 2),
            "win_rate_percent": round(win_rate, 2),
            "t_statistic": round(t_stat, 4),
            "p_value": round(p_val, 6),
            "cohens_d": round(cohens_d, 4),
            "is_statistically_significant": p_val < 0.05 and win_rate > 60.0,
        }
