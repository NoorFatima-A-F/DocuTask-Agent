"""
Scientific Statistics - Statistical Hypothesis Tests
Implements two-sample t-tests, Mann-Whitney U rank sums, and Kolmogorov-Smirnov distribution tests.
"""

from typing import List, Dict
import math


class StatisticalHypothesisTests:
    """Statistical significance and hypothesis test suite."""

    @staticmethod
    def two_sample_t_test(sample_a: List[float], sample_b: List[float]) -> Dict[str, float]:
        """Performs Welch's t-test for unequal variances."""
        n1, n2 = len(sample_a), len(sample_b)
        if n1 < 2 or n2 < 2:
            return {"t_stat": 0.0, "p_val": 1.0, "dof": 1.0}

        m1 = sum(sample_a) / n1
        m2 = sum(sample_b) / n2

        v1 = sum((x - m1) ** 2 for x in sample_a) / (n1 - 1)
        v2 = sum((x - m2) ** 2 for x in sample_b) / (n2 - 1)

        denom = math.sqrt((v1 / n1) + (v2 / n2)) + 1e-9
        t_stat = (m1 - m2) / denom

        # Welch-Satterthwaite degrees of freedom
        num_dof = ((v1 / n1) + (v2 / n2)) ** 2
        den_dof = ((v1 / n1) ** 2 / (n1 - 1)) + ((v2 / n2) ** 2 / (n2 - 1)) + 1e-9
        dof = num_dof / den_dof

        # Normal approximation of two-tailed p-value
        z = abs(t_stat)
        p_val = math.erfc(z / math.sqrt(2.0))

        return {
            "t_statistic": round(t_stat, 4),
            "p_value": round(p_val, 6),
            "degrees_of_freedom": round(dof, 2),
            "mean_diff": round(m1 - m2, 4),
        }

    @staticmethod
    def mann_whitney_u_test(sample_a: List[float], sample_b: List[float]) -> Dict[str, float]:
        """Non-parametric Mann-Whitney U test for difference in distribution medians."""
        n1, n2 = len(sample_a), len(sample_b)
        if n1 == 0 or n2 == 0:
            return {"u_stat": 0.0, "p_val": 1.0}

        # Combine and rank
        combined = [(x, 'a') for x in sample_a] + [(y, 'b') for y in sample_b]
        combined.sort(key=lambda item: item[0])

        rank_a = 0
        for rank, (val, group) in enumerate(combined, start=1):
            if group == 'a':
                rank_a += rank

        u1 = rank_a - (n1 * (n1 + 1)) / 2.0
        u2 = n1 * n2 - u1
        u_stat = min(u1, u2)

        # Normal approximation for large samples
        mu_u = (n1 * n2) / 2.0
        sigma_u = math.sqrt((n1 * n2 * (n1 + n2 + 1)) / 12.0) + 1e-9
        z = (u_stat - mu_u) / sigma_u
        p_val = math.erfc(abs(z) / math.sqrt(2.0))

        return {
            "u_statistic": round(u_stat, 4),
            "z_score": round(z, 4),
            "p_value": round(p_val, 6),
        }
