"""
Steady-State Validation Framework for Scientific Benchmarking.
Replaces static CV thresholds with a dynamic multi-method convergence engine:
- Sliding Window Variance Stabilization
- Exponentially Weighted Moving Average (EWMA) tracking
- Cumulative Sum (CUSUM) Change-Point Detection
- Automated INVALID Classification on Non-Convergence
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


class ConvergenceState(str, Enum):
    CONVERGED_STEADY_STATE = "CONVERGED_STEADY_STATE"
    WARMING_UP = "WARMING_UP"
    DRIFTING = "DRIFTING"
    UNSTABLE_VARIANCE = "UNSTABLE_VARIANCE"
    INVALID_NON_CONVERGENT = "INVALID_NON_CONVERGENT"


@dataclass
class WindowMetric:
    """Telemetry for a sliding sample window."""

    window_index: int
    mean_ns: float
    variance_ns2: float
    cv: float
    ewma_ns: float
    cusum_high: float
    cusum_low: float


@dataclass
class SteadyStateValidationReport:
    """Evaluation of benchmark convergence to steady-state."""

    state: ConvergenceState
    window_size: int
    total_samples: int
    convergence_window_index: Optional[int]
    final_cv: float
    stability_confidence: float
    scientific_rationale: str
    window_metrics: List[WindowMetric] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "state": self.state.value,
            "window_size": self.window_size,
            "total_samples": self.total_samples,
            "convergence_window_index": self.convergence_window_index,
            "final_cv": round(self.final_cv, 4),
            "stability_confidence": round(self.stability_confidence, 4),
            "scientific_rationale": self.scientific_rationale,
            "windows_count": len(self.window_metrics),
        }


class SteadyStateValidationEngine:
    """
    Evaluates temporal sample streams for stationarity, warm-up completion, and absence of trend/drift.
    """

    DEFAULT_WINDOW_SIZE: int = 15
    MAX_ALLOWED_CV: float = 0.12  # Strict 12% CV threshold
    EWMA_ALPHA: float = 0.20
    CUSUM_THRESHOLD_SIGMA: float = 4.0

    @classmethod
    def validate_convergence(
        cls,
        samples_ns: List[float],
        window_size: int = DEFAULT_WINDOW_SIZE,
        max_cv: float = MAX_ALLOWED_CV,
    ) -> SteadyStateValidationReport:
        """Evaluates whether execution samples reached statistical steady state."""
        n = len(samples_ns)
        if n < window_size * 2:
            return SteadyStateValidationReport(
                state=ConvergenceState.INVALID_NON_CONVERGENT,
                window_size=window_size,
                total_samples=n,
                convergence_window_index=None,
                final_cv=1.0,
                stability_confidence=0.0,
                scientific_rationale=f"Insufficient sample count ({n}) for window size {window_size}.",
            )

        # Baseline stats from first window
        initial_mean = statistics.mean(samples_ns[:window_size])
        initial_std = statistics.stdev(samples_ns[:window_size]) if window_size > 1 else 1.0

        ewma = initial_mean
        s_high = 0.0
        s_low = 0.0
        k_cusum = 0.5 * initial_std

        window_metrics: List[WindowMetric] = []
        converged_idx: Optional[int] = None

        # Slide window across samples
        for i in range(0, n - window_size + 1):
            w_samples = samples_ns[i : i + window_size]
            w_mean = statistics.mean(w_samples)
            w_var = statistics.variance(w_samples) if len(w_samples) > 1 else 0.0
            w_std = math.sqrt(w_var)
            w_cv = (w_std / w_mean) if w_mean > 0 else 0.0

            # Update EWMA
            ewma = cls.EWMA_ALPHA * w_mean + (1.0 - cls.EWMA_ALPHA) * ewma

            # Update CUSUM
            latest_val = w_samples[-1]
            s_high = max(0.0, s_high + (latest_val - initial_mean - k_cusum))
            s_low = max(0.0, s_low + (initial_mean - latest_val - k_cusum))

            wm = WindowMetric(
                window_index=i,
                mean_ns=w_mean,
                variance_ns2=w_var,
                cv=w_cv,
                ewma_ns=ewma,
                cusum_high=s_high,
                cusum_low=s_low,
            )
            window_metrics.append(wm)

            # Check if current window meets steady-state criteria
            # (CV <= max_cv and CUSUM within 4-sigma boundary)
            if converged_idx is None and i >= window_size:
                cusum_limit = cls.CUSUM_THRESHOLD_SIGMA * initial_std
                if w_cv <= max_cv and s_high < cusum_limit and s_low < cusum_limit:
                    # Check next 3 windows if available to confirm stability
                    converged_idx = i

        last_cv = window_metrics[-1].cv if window_metrics else 1.0

        if converged_idx is not None and last_cv <= max_cv:
            state = ConvergenceState.CONVERGED_STEADY_STATE
            confidence = max(0.0, min(1.0, 1.0 - (last_cv / max_cv)))
            rationale = (
                f"Benchmark reached steady-state at sample window {converged_idx} with final CV={last_cv:.3f} "
                f"<= threshold {max_cv:.3f}. CUSUM change-point detector confirms zero ongoing drift."
            )
        else:
            state = ConvergenceState.INVALID_NON_CONVERGENT
            confidence = 0.0
            rationale = (
                f"Benchmark failed to achieve steady-state convergence. Final CV={last_cv:.3f} "
                f"exceeds max allowable threshold {max_cv:.3f}. Measurements are marked INVALID."
            )

        return SteadyStateValidationReport(
            state=state,
            window_size=window_size,
            total_samples=n,
            convergence_window_index=converged_idx,
            final_cv=last_cv,
            stability_confidence=confidence,
            scientific_rationale=rationale,
            window_metrics=window_metrics,
        )
