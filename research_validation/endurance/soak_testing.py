"""
Research Validation & Independent Scientific Verification Framework (RVISF)
Phase 47: Long-Duration Reliability & Endurance Laboratory

Evaluates multi-hour/multi-day soak test stability:
- Memory leak detection (heap growth slope, OOM hazard)
- File descriptor and socket leak tracking
- GC pauses and steady-state latency degradation under sustained load
- MTBF (Mean Time Between Failures) and availability estimation
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class SoakDataPoint:
    """Telemetry measurement snapshot during an endurance soak test."""
    timestamp_sec: float
    memory_rss_mb: float
    open_file_descriptors: int
    active_threads: int
    throughput_req_per_sec: float
    error_count: int
    p99_latency_ms: float


@dataclass
class MemoryLeakAnalysis:
    """Statistical regression analysis for memory leaks."""
    slope_mb_per_hour: float
    r_squared: float
    is_leaking: bool
    estimated_hours_until_oom: Optional[float]


@dataclass
class SoakTestReport:
    """Comprehensive long-duration reliability report."""
    duration_hours: float
    total_data_points: int
    memory_analysis: MemoryLeakAnalysis
    fd_leak_detected: bool
    mean_throughput: float
    availability_percentage: float
    mtbf_hours: float
    status: str  # "PASS", "DEGRADED", "FAIL"
    details: Dict[str, Any] = field(default_factory=dict)


class LongDurationSoakLab:
    """
    Evaluates memory growth trends, file descriptor exhaustion, and sustained reliability.
    """

    @classmethod
    def analyze_memory_growth(
        cls,
        data_points: List[SoakDataPoint],
        max_allowed_slope_mb_per_hour: float = 2.0,
        system_memory_limit_mb: float = 8192.0
    ) -> MemoryLeakAnalysis:
        """
        Ordinary Least Squares regression on memory RSS vs time.
        """
        if len(data_points) < 2:
            return MemoryLeakAnalysis(slope_mb_per_hour=0.0, r_squared=0.0, is_leaking=False, estimated_hours_until_oom=None)

        n = len(data_points)
        t_hours = [p.timestamp_sec / 3600.0 for p in data_points]
        rss = [p.memory_rss_mb for p in data_points]

        mean_t = sum(t_hours) / n
        mean_rss = sum(rss) / n

        cov_t_rss = sum((t - mean_t) * (r - mean_rss) for t, r in zip(t_hours, rss))
        var_t = sum((t - mean_t) ** 2 for t in t_hours)

        slope = (cov_t_rss / var_t) if var_t > 1e-12 else 0.0

        var_rss = sum((r - mean_rss) ** 2 for r in rss)
        r_sq = ((cov_t_rss ** 2) / (var_t * var_rss)) if (var_t * var_rss) > 1e-12 else 0.0

        is_leaking = slope > max_allowed_slope_mb_per_hour and r_sq > 0.50

        # Time until OOM
        last_rss = rss[-1]
        hours_to_oom = ((system_memory_limit_mb - last_rss) / slope) if (is_leaking and slope > 0) else None

        return MemoryLeakAnalysis(
            slope_mb_per_hour=slope,
            r_squared=r_sq,
            is_leaking=is_leaking,
            estimated_hours_until_oom=hours_to_oom
        )

    @classmethod
    def run_soak_audit(
        cls,
        data_points: List[SoakDataPoint],
        system_memory_limit_mb: float = 8192.0
    ) -> SoakTestReport:
        """
        Run complete soak test endurance audit.
        """
        if not data_points:
            return SoakTestReport(
                duration_hours=0.0,
                total_data_points=0,
                memory_analysis=MemoryLeakAnalysis(0.0, 0.0, False, None),
                fd_leak_detected=False,
                mean_throughput=0.0,
                availability_percentage=0.0,
                mtbf_hours=0.0,
                status="INSUFFICIENT_EVIDENCE"
            )

        n = len(data_points)
        duration_hours = (data_points[-1].timestamp_sec - data_points[0].timestamp_sec) / 3600.0 if n > 1 else 0.0

        mem_analysis = cls.analyze_memory_growth(data_points, system_memory_limit_mb=system_memory_limit_mb)

        # FD leak check (difference between last 10% and first 10%)
        k = max(1, n // 10)
        start_fds = sum(p.open_file_descriptors for p in data_points[:k]) / k
        end_fds = sum(p.open_file_descriptors for p in data_points[-k:]) / k
        fd_leak = (end_fds - start_fds) > 10.0

        # Availability and MTBF
        total_errors = sum(p.error_count for p in data_points)
        mean_tp = sum(p.throughput_req_per_sec for p in data_points) / n
        total_requests = sum(p.throughput_req_per_sec * 60.0 for p in data_points)  # approximate

        avail = 100.0 * (1.0 - (total_errors / total_requests)) if total_requests > 0 else 100.0
        mtbf = (duration_hours / total_errors) if total_errors > 0 else (duration_hours * 10.0)

        passed = not mem_analysis.is_leaking and not fd_leak and avail >= 99.9

        return SoakTestReport(
            duration_hours=duration_hours,
            total_data_points=n,
            memory_analysis=mem_analysis,
            fd_leak_detected=fd_leak,
            mean_throughput=mean_tp,
            availability_percentage=avail,
            mtbf_hours=mtbf,
            status="PASS" if passed else "FAIL",
            details={"total_errors": total_errors}
        )
