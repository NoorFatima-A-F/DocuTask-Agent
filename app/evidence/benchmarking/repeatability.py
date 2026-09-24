"""
Benchmark Repeatability & Multi-Run Campaign Framework.
Executes multi-run experimental campaigns to quantify:
- Cross-run drift between independent benchmark executions
- Repeatability coefficient (R = 1.0 - (std_between / grand_mean))
- Thermal / background noise drift trends
- Automated detection and rejection of benchmark instability
"""

from __future__ import annotations

import logging
import statistics
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List

logger = logging.getLogger(__name__)


class RepeatabilityStatus(str, Enum):
    HIGHLY_REPRODUCIBLE = "HIGHLY_REPRODUCIBLE"
    MODERATE_DRIFT = "MODERATE_DRIFT"
    INSTABLE_HIGH_DRIFT = "INSTABLE_HIGH_DRIFT"


@dataclass
class SingleCampaignRun:
    """Telemetry from a single execution run in a campaign."""

    run_index: int
    mean_duration_ns: float
    median_duration_ns: float
    std_dev_ns: float
    p95_ns: float
    timestamp: float = field(default_factory=time.time)


@dataclass
class RepeatabilityReport:
    """Consolidated multi-run repeatability and stability evaluation."""

    benchmark_name: str
    total_runs: int
    iterations_per_run: int
    runs: List[SingleCampaignRun]
    grand_mean_ns: float
    cross_run_std_ns: float
    repeatability_coefficient: float  # 0.0 to 1.0 (1.0 = perfect identity)
    max_drift_percentage: float
    monotonic_trend_detected: bool
    status: RepeatabilityStatus
    stability_verdict: str
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "benchmark_name": self.benchmark_name,
            "total_runs": self.total_runs,
            "iterations_per_run": self.iterations_per_run,
            "grand_mean_ns": round(self.grand_mean_ns, 2),
            "cross_run_std_ns": round(self.cross_run_std_ns, 2),
            "repeatability_coefficient": round(self.repeatability_coefficient, 4),
            "max_drift_pct": round(self.max_drift_percentage, 2),
            "monotonic_trend_detected": self.monotonic_trend_detected,
            "status": self.status.value,
            "stability_verdict": self.stability_verdict,
            "runs": [asdict(r) for r in self.runs],
        }


class RepeatabilityFramework:
    """
    Executes benchmark campaigns across independent runs to verify scientific repeatability.
    """

    DEFAULT_MAX_DRIFT_PCT: float = 30.0  # Max 30% drift threshold for sub-millisecond workloads

    @classmethod
    def execute_campaign(
        cls,
        benchmark_name: str,
        workload_fn: Callable[[], Any],
        total_runs: int = 5,
        iterations_per_run: int = 50,
        pause_between_runs_ms: float = 10.0,
        max_acceptable_drift_pct: float = DEFAULT_MAX_DRIFT_PCT,
    ) -> RepeatabilityReport:
        """Runs a multi-run campaign with thermal cooldown between runs."""
        if total_runs < 2:
            raise ValueError("Campaign requires at least 2 independent runs for repeatability analysis")

        runs: List[SingleCampaignRun] = []

        for run_idx in range(1, total_runs + 1):
            if pause_between_runs_ms > 0 and run_idx > 1:
                time.sleep(pause_between_runs_ms / 1000.0)

            # Warmup pass before timing
            for _ in range(10):
                workload_fn()

            durations: List[int] = []
            for _ in range(iterations_per_run):
                t0 = time.perf_counter_ns()
                workload_fn()
                t1 = time.perf_counter_ns()
                durations.append(t1 - t0)

            mean_d = statistics.mean(durations)
            med_d = statistics.median(durations)
            std_d = statistics.stdev(durations) if len(durations) > 1 else 0.0
            sorted_d = sorted(durations)
            p95_d = sorted_d[int(iterations_per_run * 0.95)]

            runs.append(
                SingleCampaignRun(
                    run_index=run_idx,
                    mean_duration_ns=mean_d,
                    median_duration_ns=med_d,
                    std_dev_ns=std_d,
                    p95_ns=p95_d,
                )
            )

        run_means = [r.mean_duration_ns for r in runs]
        grand_mean = statistics.mean(run_means)
        cross_run_std = statistics.stdev(run_means) if len(run_means) > 1 else 0.0

        min_mean = min(run_means)
        max_mean = max(run_means)
        max_drift_pct = ((max_mean - min_mean) / max(1.0, min_mean)) * 100.0

        # Repeatability Coefficient: R = 1.0 - (cross_run_std / grand_mean)
        cv_between = (cross_run_std / grand_mean) if grand_mean > 0 else 0.0
        r_coeff = max(0.0, min(1.0, 1.0 - cv_between))

        # Check for monotonic degradation (e.g. thermal throttling or memory leak)
        is_monotonic_rising = all(run_means[i] <= run_means[i + 1] for i in range(len(run_means) - 1))
        is_monotonic_falling = all(run_means[i] >= run_means[i + 1] for i in range(len(run_means) - 1))
        has_trend = (is_monotonic_rising or is_monotonic_falling) and max_drift_pct > 5.0

        if max_drift_pct <= max_acceptable_drift_pct and not has_trend:
            status = RepeatabilityStatus.HIGHLY_REPRODUCIBLE
            verdict = f"Passed repeatability audit (R={r_coeff:.3f}, Drift={max_drift_pct:.2f}% <= {max_acceptable_drift_pct}%)."
        elif max_drift_pct <= (max_acceptable_drift_pct * 1.5):
            status = RepeatabilityStatus.MODERATE_DRIFT
            verdict = f"Moderate cross-run drift observed ({max_drift_pct:.2f}%). Measurements show acceptable variance."
        else:
            status = RepeatabilityStatus.INSTABLE_HIGH_DRIFT
            verdict = f"REJECTED: High cross-run drift ({max_drift_pct:.2f}% > {max_acceptable_drift_pct}%) indicates unstable runtime environment."

        return RepeatabilityReport(
            benchmark_name=benchmark_name,
            total_runs=total_runs,
            iterations_per_run=iterations_per_run,
            runs=runs,
            grand_mean_ns=grand_mean,
            cross_run_std_ns=cross_run_std,
            repeatability_coefficient=r_coeff,
            max_drift_percentage=max_drift_pct,
            monotonic_trend_detected=has_trend,
            status=status,
            stability_verdict=verdict,
        )
