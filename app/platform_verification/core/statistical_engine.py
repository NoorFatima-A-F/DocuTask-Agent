"""
Statistical & Distribution Engine for Probabilistic and Deterministic AI Evaluation
"""
import math
from typing import List, Optional
from app.platform_verification.domain.models import ConfidenceInterval

class StatisticalEngine:
    @staticmethod
    def calculate_confidence_interval(
        samples: List[float],
        confidence_level: float = 0.95,
        baseline_comparison: Optional[float] = None
    ) -> ConfidenceInterval:
        n = len(samples)
        if n == 0:
            return ConfidenceInterval(
                lower_bound=0.0,
                upper_bound=0.0,
                confidence_level=confidence_level,
                sample_size=0,
                standard_deviation=0.0
            )
        if n == 1:
            val = samples[0]
            return ConfidenceInterval(
                lower_bound=val,
                upper_bound=val,
                confidence_level=confidence_level,
                sample_size=1,
                standard_deviation=0.0
            )

        mean = sum(samples) / n
        variance = sum((x - mean) ** 2 for x in samples) / (n - 1)
        std_dev = math.sqrt(variance)

        t_crit = 1.96 if n >= 30 else 2.262 if n <= 10 else 2.086
        margin_of_error = t_crit * (std_dev / math.sqrt(n))

        lower = max(0.0, round(mean - margin_of_error, 4))
        upper = min(1.0, round(mean + margin_of_error, 4)) if all(0.0 <= x <= 1.0 for x in samples) else round(mean + margin_of_error, 4)

        p_val = None
        if baseline_comparison is not None and std_dev > 0:
            t_stat = (mean - baseline_comparison) / (std_dev / math.sqrt(n))
            p_val = round(2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(t_stat) / math.sqrt(2)))), 5)

        return ConfidenceInterval(
            lower_bound=lower,
            upper_bound=upper,
            confidence_level=confidence_level,
            sample_size=n,
            standard_deviation=round(std_dev, 4),
            p_value=p_val
        )

    @staticmethod
    def detect_distribution_drift(
        current_samples: List[float],
        baseline_samples: List[float],
        threshold_p_value: float = 0.05
    ) -> bool:
        n1, n2 = len(current_samples), len(baseline_samples)
        if n1 < 2 or n2 < 2:
            return False

        m1, m2 = sum(current_samples) / n1, sum(baseline_samples) / n2
        v1 = sum((x - m1) ** 2 for x in current_samples) / (n1 - 1)
        v2 = sum((x - m2) ** 2 for x in baseline_samples) / (n2 - 1)

        denom = math.sqrt((v1 / n1) + (v2 / n2)) if (v1 + v2) > 0 else 0.0
        if denom == 0:
            return False

        t_stat = abs(m1 - m2) / denom
        p_val = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(t_stat / math.sqrt(2))))
        return p_val < threshold_p_value

statistical_engine = StatisticalEngine()
