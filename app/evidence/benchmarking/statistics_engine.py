"""
Advanced Statistical Analysis Engine for Enterprise Benchmarking.
Inspired by Criterion.rs and R's benchmark packages.
Computes complete descriptive statistics, Student-t and bootstrap confidence intervals,
outlier detection (IQR, Z-Score, Modified Z-Score, Grubbs), and distribution classification.
"""

from __future__ import annotations

import logging
import math
import random
import statistics
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class DistributionType(str, Enum):
    NORMAL = "NORMAL"
    LOG_NORMAL = "LOG_NORMAL"
    BIMODAL = "BIMODAL"
    HEAVY_TAILED = "HEAVY_TAILED"
    UNIFORM = "UNIFORM"


@dataclass
class ConfidenceInterval:
    """Statistical confidence interval."""

    confidence_level: float  # 0.95 or 0.99
    lower_bound: float
    upper_bound: float
    point_estimate: float
    method: str  # "STUDENT_T", "PERCENTILE_BOOTSTRAP"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "confidence_level": self.confidence_level,
            "lower_bound": round(self.lower_bound, 4),
            "upper_bound": round(self.upper_bound, 4),
            "point_estimate": round(self.point_estimate, 4),
            "method": self.method,
        }


@dataclass
class OutlierReport:
    """Outlier detection analysis."""

    iqr_outliers_count: int
    zscore_outliers_count: int
    modified_zscore_outliers_count: int
    grubbs_detected_outlier: Optional[float] = None
    clean_sample_size: int = 0


@dataclass
class FullStatisticalReport:
    """Comprehensive statistical metrics report."""

    sample_size: int
    mean: float
    median: float
    mode: Optional[float]
    variance: float
    std_dev: float
    mad: float  # Median Absolute Deviation
    cv: float  # Coefficient of Variation (std_dev / mean)
    iqr: float  # Interquartile Range
    min_val: float
    max_val: float
    skewness: float
    kurtosis: float
    ci_95_t: ConfidenceInterval
    ci_99_t: ConfidenceInterval
    ci_95_bootstrap: ConfidenceInterval
    outliers: OutlierReport
    detected_distribution: DistributionType
    p50: float
    p90: float
    p95: float
    p99: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sample_size": self.sample_size,
            "mean": round(self.mean, 4),
            "median": round(self.median, 4),
            "mode": round(self.mode, 4) if self.mode is not None else None,
            "variance": round(self.variance, 4),
            "std_dev": round(self.std_dev, 4),
            "mad": round(self.mad, 4),
            "cv": round(self.cv, 4),
            "iqr": round(self.iqr, 4),
            "min": round(self.min_val, 4),
            "max": round(self.max_val, 4),
            "skewness": round(self.skewness, 4),
            "kurtosis": round(self.kurtosis, 4),
            "ci_95_t": self.ci_95_t.to_dict(),
            "ci_99_t": self.ci_99_t.to_dict(),
            "ci_95_bootstrap": self.ci_95_bootstrap.to_dict(),
            "outliers": {
                "iqr_outliers": self.outliers.iqr_outliers_count,
                "zscore_outliers": self.outliers.zscore_outliers_count,
                "clean_sample_size": self.outliers.clean_sample_size,
            },
            "detected_distribution": self.detected_distribution.value,
            "percentiles": {
                "p50": round(self.p50, 4),
                "p90": round(self.p90, 4),
                "p95": round(self.p95, 4),
                "p99": round(self.p99, 4),
            },
        }


class AdvancedStatisticsEngine:
    """Production statistical analysis engine for benchmark data."""

    @classmethod
    def analyze(cls, samples: List[float], bootstrap_resamples: int = 1000) -> FullStatisticalReport:
        """Computes comprehensive statistical analysis over a numeric sample array."""
        if not samples:
            raise ValueError("Sample array cannot be empty")

        n = len(samples)
        sorted_samples = sorted(samples)

        # 1. Central Tendency
        mean_val = statistics.mean(samples)
        median_val = statistics.median(samples)
        try:
            mode_val = float(statistics.mode(samples))
        except Exception:
            mode_val = None

        # 2. Dispersion & Spread
        var_val = statistics.variance(samples) if n > 1 else 0.0
        std_val = statistics.stdev(samples) if n > 1 else 0.0
        cv_val = (std_val / mean_val) if mean_val != 0.0 else 0.0

        # Median Absolute Deviation (MAD) = median(|x_i - median(X)|)
        abs_devs = [abs(x - median_val) for x in samples]
        mad_val = statistics.median(abs_devs)

        # 3. Quartiles & Percentiles
        q1 = sorted_samples[int(n * 0.25)]
        q3 = sorted_samples[min(int(n * 0.75), n - 1)]
        iqr_val = q3 - q1
        min_v = sorted_samples[0]
        max_v = sorted_samples[-1]
        p50 = sorted_samples[int(n * 0.50)]
        p90 = sorted_samples[min(int(n * 0.90), n - 1)]
        p95 = sorted_samples[min(int(n * 0.95), n - 1)]
        p99 = sorted_samples[min(int(n * 0.99), n - 1)]

        # 4. Skewness & Kurtosis (Higher moments)
        if n >= 3 and std_val > 0:
            skew_val = (sum((x - mean_val) ** 3 for x in samples) / n) / (std_val ** 3)
            # Excess kurtosis (normal distribution = 0)
            kurt_val = ((sum((x - mean_val) ** 4 for x in samples) / n) / (std_val ** 4)) - 3.0
        else:
            skew_val = 0.0
            kurt_val = 0.0

        # 5. Confidence Intervals (Student-t)
        # Student-t critical values approximation (t_0.975 ~ 1.96 for n>30, t_0.995 ~ 2.576)
        t_95 = 2.042 if n < 30 else 1.960
        t_99 = 2.750 if n < 30 else 2.576
        se = (std_val / math.sqrt(n)) if n > 0 else 0.0

        ci_95_t = ConfidenceInterval(0.95, mean_val - (t_95 * se), mean_val + (t_95 * se), mean_val, "STUDENT_T")
        ci_99_t = ConfidenceInterval(0.99, mean_val - (t_99 * se), mean_val + (t_99 * se), mean_val, "STUDENT_T")

        # 6. Percentile Bootstrap Confidence Interval (Non-parametric)
        boot_means: List[float] = []
        for _ in range(bootstrap_resamples):
            resample = [random.choice(samples) for _ in range(n)]
            boot_means.append(statistics.mean(resample))
        boot_means.sort()
        b_low_idx = int(bootstrap_resamples * 0.025)
        b_high_idx = int(bootstrap_resamples * 0.975)
        ci_95_boot = ConfidenceInterval(
            0.95,
            boot_means[b_low_idx],
            boot_means[b_high_idx],
            mean_val,
            "PERCENTILE_BOOTSTRAP",
        )

        # 7. Outlier Detection
        # IQR method
        lower_iqr_bound = q1 - (1.5 * iqr_val)
        upper_iqr_bound = q3 + (1.5 * iqr_val)
        iqr_outliers = [x for x in samples if x < lower_iqr_bound or x > upper_iqr_bound]

        # Z-score method (|z| > 3.0)
        zscore_outliers = [x for x in samples if std_val > 0 and abs((x - mean_val) / std_val) > 3.0]

        # Modified Z-Score (using MAD): M_i = 0.6745 * (x_i - median) / MAD
        mod_z_outliers = [
            x for x in samples if mad_val > 0 and abs(0.6745 * (x - median_val) / mad_val) > 3.5
        ]

        # Grubbs test for single extreme outlier
        grubbs_outlier = None
        if n >= 3 and std_val > 0:
            max_dev_idx = max(range(n), key=lambda i: abs(samples[i] - mean_val))
            g_stat = abs(samples[max_dev_idx] - mean_val) / std_val
            # Critical Grubbs threshold approximation for alpha=0.05
            g_crit = ((n - 1) / math.sqrt(n)) * math.sqrt((t_95**2) / (n - 2 + (t_95**2)))
            if g_stat > g_crit:
                grubbs_outlier = samples[max_dev_idx]

        outlier_rep = OutlierReport(
            iqr_outliers_count=len(iqr_outliers),
            zscore_outliers_count=len(zscore_outliers),
            modified_zscore_outliers_count=len(mod_z_outliers),
            grubbs_detected_outlier=grubbs_outlier,
            clean_sample_size=n - len(iqr_outliers),
        )

        # 8. Distribution Classification
        if abs(skew_val) < 0.5 and abs(kurt_val) < 1.0:
            dist_type = DistributionType.NORMAL
        elif skew_val > 1.0:
            dist_type = DistributionType.LOG_NORMAL
        elif kurt_val > 3.0:
            dist_type = DistributionType.HEAVY_TAILED
        else:
            dist_type = DistributionType.UNIFORM

        return FullStatisticalReport(
            sample_size=n,
            mean=mean_val,
            median=median_val,
            mode=mode_val,
            variance=var_val,
            std_dev=std_val,
            mad=mad_val,
            cv=cv_val,
            iqr=iqr_val,
            min_val=min_v,
            max_val=max_v,
            skewness=skew_val,
            kurtosis=kurt_val,
            ci_95_t=ci_95_t,
            ci_99_t=ci_99_t,
            ci_95_bootstrap=ci_95_boot,
            outliers=outlier_rep,
            detected_distribution=dist_type,
            p50=p50,
            p90=p90,
            p95=p95,
            p99=p99,
        )
