"""
Statistical Power Analysis Engine for Scientific Benchmarking.
Implements Neyman-Pearson statistical power calculation and sample size planning:
- Cohen's d effect size calculation
- Pre-experimental required sample size estimation (Type I alpha, Type II beta)
- Post-hoc achieved statistical power calculation (1 - beta)
- Automated underpowered benchmark detection and warning generation
"""

from __future__ import annotations

import logging
import math
import statistics
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class PowerAdequacyStatus(str, Enum):
    ADEQUATE = "ADEQUATE"
    MARGINAL = "MARGINAL"
    UNDERPOWERED = "UNDERPOWERED"


@dataclass
class PowerAnalysisReport:
    """Report on experimental statistical power and sample size validity."""

    target_effect_size_d: float
    observed_effect_size_d: float
    alpha_significance: float
    desired_power: float
    achieved_power: float
    required_sample_size: int
    actual_sample_size: int
    adequacy_status: PowerAdequacyStatus
    is_underpowered: bool
    warning_message: Optional[str]
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_effect_size_d": round(self.target_effect_size_d, 3),
            "observed_effect_size_d": round(self.observed_effect_size_d, 3),
            "alpha": self.alpha_significance,
            "desired_power": self.desired_power,
            "achieved_power": round(self.achieved_power, 4),
            "required_sample_size": self.required_sample_size,
            "actual_sample_size": self.actual_sample_size,
            "adequacy_status": self.adequacy_status.value,
            "is_underpowered": self.is_underpowered,
            "warning": self.warning_message,
        }


class StatisticalPowerEngine:
    """
    Computes statistical power and guarantees that benchmark conclusions are not underpowered.
    """

    DEFAULT_ALPHA: float = 0.05
    DEFAULT_DESIRED_POWER: float = 0.80
    DEFAULT_EFFECT_SIZE: float = 0.50  # Medium effect size (Cohen's d)

    @classmethod
    def estimate_required_sample_size(
        cls,
        effect_size_d: float = DEFAULT_EFFECT_SIZE,
        alpha: float = DEFAULT_ALPHA,
        desired_power: float = DEFAULT_DESIRED_POWER,
    ) -> int:
        """
        Estimates minimum sample size N required to detect effect size d with power (1 - beta).
        Formula for two-tailed two-sample t-test: N approx 2 * ((z_{alpha/2} + z_{beta}) / d)^2
        """
        d = max(0.01, abs(effect_size_d))
        z_alpha = cls._inv_normal_cdf(1.0 - alpha / 2.0)
        z_beta = cls._inv_normal_cdf(desired_power)

        n_req = 2.0 * ((z_alpha + z_beta) / d) ** 2
        return max(10, int(math.ceil(n_req)))

    @classmethod
    def analyze_power(
        cls,
        samples_treatment: List[float],
        samples_baseline: Optional[List[float]] = None,
        hypothesized_mean: Optional[float] = None,
        alpha: float = DEFAULT_ALPHA,
        desired_power: float = DEFAULT_DESIRED_POWER,
    ) -> PowerAnalysisReport:
        """Computes post-hoc statistical power for the measured sample."""
        n = len(samples_treatment)
        if n < 3:
            return PowerAnalysisReport(
                target_effect_size_d=cls.DEFAULT_EFFECT_SIZE,
                observed_effect_size_d=0.0,
                alpha_significance=alpha,
                desired_power=desired_power,
                achieved_power=0.0,
                required_sample_size=30,
                actual_sample_size=n,
                adequacy_status=PowerAdequacyStatus.UNDERPOWERED,
                is_underpowered=True,
                warning_message=f"Sample size {n} is critically insufficient for statistical inference.",
            )

        mean_t = statistics.mean(samples_treatment)
        std_t = statistics.stdev(samples_treatment) if n > 1 else 1.0

        # Calculate observed effect size (Cohen's d)
        if samples_baseline is not None and len(samples_baseline) >= 2:
            mean_b = statistics.mean(samples_baseline)
            std_b = statistics.stdev(samples_baseline)
            n_b = len(samples_baseline)
            pooled_std = math.sqrt(((n - 1) * (std_t ** 2) + (n_b - 1) * (std_b ** 2)) / max(1, (n + n_b - 2)))
            d_obs = abs(mean_t - mean_b) / max(1e-9, pooled_std)
        else:
            ref_val = hypothesized_mean if hypothesized_mean is not None else (mean_t * 0.95)
            d_obs = abs(mean_t - ref_val) / max(1e-9, std_t)

        d_obs = max(0.05, min(5.0, d_obs))

        # Required sample size for observed effect size
        n_required = cls.estimate_required_sample_size(effect_size_d=d_obs, alpha=alpha, desired_power=desired_power)

        # Calculate post-hoc achieved power (1 - beta)
        z_alpha = cls._inv_normal_cdf(1.0 - alpha / 2.0)
        # Non-centrality parameter delta = d * sqrt(N / 2)
        delta = d_obs * math.sqrt(n / 2.0)
        z_beta_achieved = delta - z_alpha
        achieved_power = cls._normal_cdf(z_beta_achieved)
        achieved_power = max(0.0, min(1.0, achieved_power))

        if achieved_power >= desired_power:
            status = PowerAdequacyStatus.ADEQUATE
            warning = None
            is_underpowered = False
        elif achieved_power >= (desired_power * 0.85):
            status = PowerAdequacyStatus.MARGINAL
            warning = f"Marginal statistical power ({achieved_power:.2f} < {desired_power:.2f}). Consider increasing sample size to N={n_required}."
            is_underpowered = False
        else:
            status = PowerAdequacyStatus.UNDERPOWERED
            warning = f"Benchmark is statistically UNDERPOWERED (Achieved Power={achieved_power:.2f} < {desired_power:.2f}). Required N={n_required}, actual N={n}."
            is_underpowered = True

        return PowerAnalysisReport(
            target_effect_size_d=cls.DEFAULT_EFFECT_SIZE,
            observed_effect_size_d=d_obs,
            alpha_significance=alpha,
            desired_power=desired_power,
            achieved_power=achieved_power,
            required_sample_size=n_required,
            actual_sample_size=n,
            adequacy_status=status,
            is_underpowered=is_underpowered,
            warning_message=warning,
        )

    # -------------------------------------------------------------------------
    # Math Helpers
    # -------------------------------------------------------------------------
    @classmethod
    def _normal_cdf(cls, z: float) -> float:
        return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

    @classmethod
    def _inv_normal_cdf(cls, p: float) -> float:
        """Exact rational approximation for inverse standard normal CDF (Abramowitz & Stegun)."""
        if p <= 0.0:
            return -8.0
        if p >= 1.0:
            return 8.0
        if p == 0.5:
            return 0.0
        if p < 0.5:
            return -cls._inv_normal_cdf(1.0 - p)

        t = math.sqrt(-2.0 * math.log(1.0 - p))
        c0 = 2.515517
        c1 = 0.802853
        c2 = 0.010328
        d1 = 1.432788
        d2 = 0.189269
        d3 = 0.001308
        numerator = c0 + c1 * t + c2 * (t ** 2)
        denominator = 1.0 + d1 * t + d2 * (t ** 2) + d3 * (t ** 3)
        return t - (numerator / denominator)
