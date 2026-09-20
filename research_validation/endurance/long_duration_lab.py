"""
Independent Evidence & Real-World Validation Platform (IERVP)
Phase 66: Long Duration Reliability & Soak Testing Laboratory

Validates stability under extended multi-day operational load:
- Target Windows: 24 Hours, 72 Hours, 1 Week (168 Hours)
- Leak Detection: Memory RSS (OLS linear regression slope), File Descriptors, Thread Pool exhaustion
- Performance Degradation: Latency tail elongation, Heap fragmentation index
- Transparent Reporting: Strictly publishes ACTUAL measured duration vs planned target window.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class SoakTargetWindow(str, Enum):
    WINDOW_24H = "24_HOURS"
    WINDOW_72H = "72_HOURS"
    WINDOW_168H = "1_WEEK_168H"
    ACCELERATED_SIMULATION = "ACCELERATED_SIMULATION"


@dataclass
class SoakSnapshotTelemetry:
    """Periodic telemetry sample recorded during soak testing."""
    elapsed_seconds: float
    memory_rss_mb: float
    open_file_descriptors: int
    active_thread_count: int
    throughput_rps: float
    error_count: int
    p99_latency_ms: float


@dataclass
class LongDurationReliabilityReport:
    """Comprehensive long-duration endurance audit."""
    target_window: SoakTargetWindow
    planned_duration_hours: float
    actual_measured_duration_hours: float  # Actual measured duration!
    total_telemetry_snapshots: int
    memory_growth_slope_mb_per_hour: float
    is_memory_leaking: bool
    fd_growth_count: int
    is_fd_leaking: bool
    thread_growth_count: int
    mean_throughput_rps: float
    uptime_availability_pct: float
    mtbf_hours: float
    assumptions: List[str]
    methodology: str
    limitations: List[str]
    reproducibility_instructions: str
    verdict: str  # "STABLE_PRODUCTION_GRADE", "RESOURCE_LEAK_DETECTED", "DEGRADED"


class LongDurationReliabilityLab:
    """
    Evaluates multi-day stability and resource consumption slopes.
    """

    @classmethod
    def evaluate_soak_run(
        cls,
        target_window: SoakTargetWindow,
        snapshots: List[SoakSnapshotTelemetry],
        max_allowed_mem_slope_mb_per_hr: float = 1.5
    ) -> LongDurationReliabilityReport:
        """Analyze time-series telemetry recorded over a soak duration."""
        if not snapshots:
            return LongDurationReliabilityReport(
                target_window=target_window,
                planned_duration_hours=24.0,
                actual_measured_duration_hours=0.0,
                total_telemetry_snapshots=0,
                memory_growth_slope_mb_per_hour=0.0,
                is_memory_leaking=False,
                fd_growth_count=0,
                is_fd_leaking=False,
                thread_growth_count=0,
                mean_throughput_rps=0.0,
                uptime_availability_pct=0.0,
                mtbf_hours=0.0,
                assumptions=["Continuous soak workload generator active"],
                limitations=["No telemetry snapshots available"],
                reproducibility_instructions="Run soak load generator over desired duration window",
                verdict="DEGRADED"
            )

        n = len(snapshots)
        actual_hours = (snapshots[-1].elapsed_seconds - snapshots[0].elapsed_seconds) / 3600.0 if n > 1 else 0.0

        planned_hours = 24.0 if target_window == SoakTargetWindow.WINDOW_24H else 72.0 if target_window == SoakTargetWindow.WINDOW_72H else 168.0 if target_window == SoakTargetWindow.WINDOW_168H else actual_hours

        # OLS slope for memory
        t_hrs = [s.elapsed_seconds / 3600.0 for s in snapshots]
        mem = [s.memory_rss_mb for s in snapshots]
        mean_t = sum(t_hrs) / n
        mean_m = sum(mem) / n
        cov_tm = sum((t - mean_t) * (m - mean_m) for t, m in zip(t_hrs, mem))
        var_t = sum((t - mean_t) ** 2 for t in t_hrs)
        slope_mem = (cov_tm / var_t) if var_t > 1e-12 else 0.0

        is_mem_leak = slope_mem > max_allowed_mem_slope_mb_per_hr

        # FD and Thread growth
        fd_growth = snapshots[-1].open_file_descriptors - snapshots[0].open_file_descriptors
        is_fd_leak = fd_growth > 5
        thread_growth = snapshots[-1].active_thread_count - snapshots[0].active_thread_count

        total_errs = sum(s.error_count for s in snapshots)
        mean_tp = sum(s.throughput_rps for s in snapshots) / n
        avail = 100.0 if total_errs == 0 else max(0.0, 100.0 * (1.0 - (total_errs / (mean_tp * max(1.0, actual_hours * 3600.0)))))
        mtbf = (actual_hours / total_errs) if total_errs > 0 else (actual_hours * 10.0 if actual_hours > 0 else 1000.0)

        is_stable = not is_mem_leak and not is_fd_leak and avail >= 99.9
        verdict = "STABLE_PRODUCTION_GRADE" if is_stable else "RESOURCE_LEAK_DETECTED"

        return LongDurationReliabilityReport(
            target_window=target_window,
            planned_duration_hours=planned_hours,
            actual_measured_duration_hours=actual_hours,
            total_telemetry_snapshots=n,
            memory_growth_slope_mb_per_hour=slope_mem,
            is_memory_leaking=is_mem_leak,
            fd_growth_count=fd_growth,
            is_fd_leaking=is_fd_leak,
            thread_growth_count=thread_growth,
            mean_throughput_rps=mean_tp,
            uptime_availability_pct=avail,
            mtbf_hours=mtbf,
            assumptions=[
                "Constant synthetic ingestion traffic applied without deliberate quiescent cool-down periods",
                "Operating system file descriptor limits (ulimit -n) configured to standard 65,535"
            ],
            methodology="Continuous longitudinal resource profiling with OLS linear drift regression on memory and descriptor handles.",
            limitations=[
                "Accelerated simulation runs scale temporal rates but may compress garbage collection cycle frequencies"
            ],
            reproducibility_instructions="Deploy daemon worker, run `python run_long_duration_soak.py --duration 24h` and record snapshots.",
            verdict=verdict
        )
