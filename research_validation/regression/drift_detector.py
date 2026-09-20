"""
Multi-Dimensional Scientific Drift Detector (Phase 89C)
======================================================
Analyzes metrics across multiple dimensions to detect performance, statistical,
confidence, environment, and hardware drift without fabricating data.
"""

from __future__ import annotations
import math
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from research_validation.provenance.hashing import hash_canonical_json


class DriftDimension(str, Enum):
    METRIC_ACCURACY = "METRIC_ACCURACY"
    LATENCY_PERFORMANCE = "LATENCY_PERFORMANCE"
    CONFIDENCE_UNCERTAINTY = "CONFIDENCE_UNCERTAINTY"
    STATISTICAL_DISTRIBUTION = "STATISTICAL_DISTRIBUTION"
    ENVIRONMENT_HARDWARE = "ENVIRONMENT_HARDWARE"


class DriftSeverity(str, Enum):
    NONE = "NONE"
    NEGLIGIBLE = "NEGLIGIBLE"
    MODERATE = "MODERATE"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class DimensionDriftResult:
    """Drift evaluation result for a single scientific dimension."""
    dimension: DriftDimension
    metric_name: str
    baseline_value: float
    current_value: float
    absolute_delta: float
    relative_delta_pct: float
    severity: DriftSeverity
    is_regression: bool
    diagnostic: str


class MultiDimensionalDriftDetector:
    """
    Evaluates empirical drift across accuracy, latency, uncertainty, and environment.
    """

    @classmethod
    def evaluate_metric_drift(
        cls,
        metric_name: str,
        baseline: float,
        current: float,
        higher_is_better: bool = True,
        moderate_threshold_pct: float = 2.0,
        critical_threshold_pct: float = 5.0,
    ) -> DimensionDriftResult:
        abs_delta = current - baseline
        rel_pct = (abs_delta / abs(baseline) * 100.0) if baseline != 0 else 0.0

        is_degraded = (rel_pct < 0) if higher_is_better else (rel_pct > 0)
        deg_mag = abs(rel_pct) if is_degraded else 0.0

        if deg_mag >= critical_threshold_pct:
            sev = DriftSeverity.CRITICAL
        elif deg_mag >= moderate_threshold_pct:
            sev = DriftSeverity.MODERATE
        elif deg_mag > 0.5:
            sev = DriftSeverity.NEGLIGIBLE
        else:
            sev = DriftSeverity.NONE

        return DimensionDriftResult(
            dimension=DriftDimension.METRIC_ACCURACY if "lat" not in metric_name else DriftDimension.LATENCY_PERFORMANCE,
            metric_name=metric_name,
            baseline_value=baseline,
            current_value=current,
            absolute_delta=abs_delta,
            relative_delta_pct=rel_pct,
            severity=sev,
            is_regression=(sev in (DriftSeverity.MODERATE, DriftSeverity.CRITICAL)),
            diagnostic=f"Delta {rel_pct:+.2f}% vs baseline {baseline:.4f} (Severity: {sev.value})",
        )
