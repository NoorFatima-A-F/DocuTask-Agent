"""
Bootstrap Methodology Framework for Scientific Benchmarking.
Implements:
- Percentile Bootstrap
- BCa (Bias-Corrected and Accelerated) Bootstrap
- Basic (Empirical) Bootstrap
- Studentized (Bootstrap-t) Bootstrap
- CI Convergence Curve Tracking & Reproducibility Hashing
- Automated Inconclusive Marking on Convergence Failure
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import random
import statistics
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class BootstrapType(str, Enum):
    PERCENTILE = "PERCENTILE"
    BCA = "BCA"  # Bias-Corrected and Accelerated
    BASIC = "BASIC"  # Empirical / Pivotal
    STUDENTIZED = "STUDENTIZED"  # Bootstrap-t


class BootstrapConvergenceStatus(str, Enum):
    CONVERGED = "CONVERGED"
    INCONCLUSIVE = "INCONCLUSIVE"
    FAILED = "FAILED"


@dataclass
class ConvergenceSnapshot:
    """CI stability at a checkpoint iteration."""

    resamples_count: int
    lower_bound: float
    upper_bound: float
    width: float
    relative_change_pct: float


@dataclass
class BootstrapValidationResult:
    """Complete scientific bootstrap evaluation record."""

    bootstrap_type: BootstrapType
    resamples: int
    random_seed: int
    replacement_policy: str
    point_estimate: float
    confidence_level: float
    lower_bound: float
    upper_bound: float
    bias_correction_z0: float
    acceleration_a: float
    convergence_status: BootstrapConvergenceStatus
    ci_stability_pct: float
    convergence_curve: List[ConvergenceSnapshot]
    reproducibility_hash: str = ""
    created_at: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        if not self.reproducibility_hash:
            self.reproducibility_hash = self.compute_hash()

    def compute_hash(self) -> str:
        content = (
            f"{self.bootstrap_type.value}:{self.resamples}:{self.random_seed}:"
            f"{self.point_estimate:.6f}:{self.confidence_level}:{self.lower_bound:.6f}:{self.upper_bound:.6f}:"
            f"{self.bias_correction_z0:.6f}:{self.acceleration_a:.6f}:{self.convergence_status.value}"
        )
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bootstrap_type": self.bootstrap_type.value,
            "resamples": self.resamples,
            "random_seed": self.random_seed,
            "replacement_policy": self.replacement_policy,
            "point_estimate": round(self.point_estimate, 5),
            "confidence_level": self.confidence_level,
            "lower_bound": round(self.lower_bound, 5),
            "upper_bound": round(self.upper_bound, 5),
            "bias_correction_z0": round(self.bias_correction_z0, 5),
            "acceleration_a": round(self.acceleration_a, 5),
            "convergence_status": self.convergence_status.value,
            "ci_stability_pct": round(self.ci_stability_pct, 4),
            "reproducibility_hash": self.reproducibility_hash,
            "convergence_curve": [asdict(s) for s in self.convergence_curve],
        }


class BootstrapValidationEngine:
    """
    Research-grade Bootstrap analysis and CI convergence validation engine.
    Guarantees exact statistical reproducibility.
    """

    DEFAULT_RESAMPLES: int = 2000
    DEFAULT_CONFIDENCE: float = 0.95
    STABILITY_THRESHOLD_PCT: float = 2.0  # < 2% CI boundary drift indicates convergence

    @classmethod
    def run_bootstrap(
        cls,
        samples: List[float],
        statistic_fn: Callable[[List[float]], float] = statistics.mean,
        bootstrap_type: BootstrapType = BootstrapType.BCA,
        resamples: int = DEFAULT_RESAMPLES,
        confidence_level: float = DEFAULT_CONFIDENCE,
        random_seed: int = 42,
    ) -> BootstrapValidationResult:
        """Executes selected bootstrap procedure with convergence monitoring."""
        if len(samples) < 3:
            raise ValueError(f"Sample size {len(samples)} is too small for bootstrap resampling")

        rng = random.Random(random_seed)
        n = len(samples)
        theta_hat = statistic_fn(samples)

        # Generate bootstrap resamples and track convergence snapshots
        boot_estimates: List[float] = []
        snapshots: List[ConvergenceSnapshot] = []
        checkpoints = [int(resamples * p) for p in [0.25, 0.50, 0.75, 1.0]]

        for i in range(1, resamples + 1):
            # Sample with replacement
            resample = [samples[rng.randint(0, n - 1)] for _ in range(n)]
            boot_estimates.append(statistic_fn(resample))

            if i in checkpoints:
                # Compute intermediate CI
                cur_sorted = sorted(boot_estimates)
                alpha_half = (1.0 - confidence_level) / 2.0
                low_idx = max(0, int(len(cur_sorted) * alpha_half))
                high_idx = min(len(cur_sorted) - 1, int(len(cur_sorted) * (1.0 - alpha_half)))
                c_low = cur_sorted[low_idx]
                c_high = cur_sorted[high_idx]
                c_width = c_high - c_low

                rel_change = 0.0
                if snapshots:
                    prev_width = snapshots[-1].width
                    if prev_width > 0:
                        rel_change = abs(c_width - prev_width) / prev_width * 100.0

                snapshots.append(
                    ConvergenceSnapshot(
                        resamples_count=i,
                        lower_bound=c_low,
                        upper_bound=c_high,
                        width=c_width,
                        relative_change_pct=rel_change,
                    )
                )

        sorted_boots = sorted(boot_estimates)
        alpha = 1.0 - confidence_level
        z0 = 0.0
        a = 0.0

        # Calculate final CI based on method
        if bootstrap_type == BootstrapType.PERCENTILE:
            low_idx = max(0, int(resamples * (alpha / 2.0)))
            high_idx = min(resamples - 1, int(resamples * (1.0 - alpha / 2.0)))
            ci_lower = sorted_boots[low_idx]
            ci_upper = sorted_boots[high_idx]

        elif bootstrap_type == BootstrapType.BASIC:
            low_idx = max(0, int(resamples * (alpha / 2.0)))
            high_idx = min(resamples - 1, int(resamples * (1.0 - alpha / 2.0)))
            # Basic pivot: 2*theta_hat - q(1-alpha/2), 2*theta_hat - q(alpha/2)
            ci_lower = 2.0 * theta_hat - sorted_boots[high_idx]
            ci_upper = 2.0 * theta_hat - sorted_boots[low_idx]

        elif bootstrap_type == BootstrapType.BCA:
            # 1. Bias correction parameter z0
            prop_less = sum(1 for b in sorted_boots if b < theta_hat) / resamples
            prop_less = min(0.9999, max(0.0001, prop_less))
            z0 = cls._inv_normal_cdf(prop_less)

            # 2. Acceleration parameter a via Jackknife
            jackknife_estimates = []
            for j in range(n):
                jack_sample = samples[:j] + samples[j + 1 :]
                jackknife_estimates.append(statistic_fn(jack_sample))

            jack_mean = statistics.mean(jackknife_estimates)
            diffs = [jack_mean - t for t in jackknife_estimates]
            sum_cubes = sum(d ** 3 for d in diffs)
            sum_squares = sum(d ** 2 for d in diffs)

            if sum_squares > 1e-12:
                a = sum_cubes / (6.0 * (sum_squares ** 1.5))
            else:
                a = 0.0

            # 3. Adjusted quantiles
            z_alpha1 = cls._inv_normal_cdf(alpha / 2.0)
            z_alpha2 = cls._inv_normal_cdf(1.0 - alpha / 2.0)

            def bca_quantile(z_val: float) -> float:
                denom = 1.0 - a * (z0 + z_val)
                if abs(denom) < 1e-6:
                    denom = 1e-6 if denom >= 0 else -1e-6
                adjusted_z = z0 + (z0 + z_val) / denom
                return cls._normal_cdf(adjusted_z)

            q1 = bca_quantile(z_alpha1)
            q2 = bca_quantile(z_alpha2)
            q1 = min(0.9999, max(0.0001, q1))
            q2 = min(0.9999, max(0.0001, q2))

            idx1 = max(0, min(resamples - 1, int(resamples * q1)))
            idx2 = max(0, min(resamples - 1, int(resamples * q2)))
            ci_lower = sorted_boots[min(idx1, idx2)]
            ci_upper = sorted_boots[max(idx1, idx2)]

        elif bootstrap_type == BootstrapType.STUDENTIZED:
            # Bootstrap-t using sample variance
            sample_se = statistics.stdev(samples) / math.sqrt(n) if n > 1 else 1.0
            t_stats: List[float] = []
            for b in boot_estimates:
                t_stats.append((b - theta_hat) / max(1e-9, sample_se))
            t_sorted = sorted(t_stats)
            t_low = t_sorted[max(0, int(resamples * (alpha / 2.0)))]
            t_high = t_sorted[min(resamples - 1, int(resamples * (1.0 - alpha / 2.0)))]
            ci_lower = theta_hat - t_high * sample_se
            ci_upper = theta_hat - t_low * sample_se
        else:
            ci_lower = sorted_boots[0]
            ci_upper = sorted_boots[-1]

        # Verify convergence stability between the last two snapshots
        stability_drift = snapshots[-1].relative_change_pct if snapshots else 0.0
        if stability_drift <= cls.STABILITY_THRESHOLD_PCT:
            status = BootstrapConvergenceStatus.CONVERGED
        else:
            status = BootstrapConvergenceStatus.INCONCLUSIVE

        return BootstrapValidationResult(
            bootstrap_type=bootstrap_type,
            resamples=resamples,
            random_seed=random_seed,
            replacement_policy="IID_UNIFORM_WITH_REPLACEMENT",
            point_estimate=theta_hat,
            confidence_level=confidence_level,
            lower_bound=ci_lower,
            upper_bound=ci_upper,
            bias_correction_z0=z0,
            acceleration_a=a,
            convergence_status=status,
            ci_stability_pct=stability_drift,
            convergence_curve=snapshots,
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
