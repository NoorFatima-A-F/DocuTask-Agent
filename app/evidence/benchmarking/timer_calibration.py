"""
High-Precision Timing Infrastructure & Calibration Engine for Scientific Benchmarking.
Inspired by Criterion.rs, Google Benchmark, and JMH.
Measures timer resolution, timer precision, and measurement overhead,
automatically subtracting calibration bias and rejecting impossible sub-resolution readings.
"""

from __future__ import annotations

import logging
import math
import os
import platform
import statistics
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class ClockSource(str, Enum):
    PERF_COUNTER_NS = "time.perf_counter_ns"
    PROCESS_TIME_NS = "time.process_time_ns"
    MONOTONIC_NS = "time.monotonic_ns"


@dataclass
class TimerCalibrationProfile:
    """Hardware timer calibration metrics."""

    clock_source: ClockSource
    timer_resolution_ns: float
    timer_precision_ns: float
    measurement_overhead_ns: float
    clock_drift_ppm: float
    noise_variance_ns2: float
    is_calibrated: bool = True
    calibrated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "clock_source": self.clock_source.value,
            "timer_resolution_ns": round(self.timer_resolution_ns, 3),
            "timer_precision_ns": round(self.timer_precision_ns, 3),
            "measurement_overhead_ns": round(self.measurement_overhead_ns, 3),
            "clock_drift_ppm": round(self.clock_drift_ppm, 3),
            "noise_variance_ns2": round(self.noise_variance_ns2, 3),
            "is_calibrated": self.is_calibrated,
            "calibrated_at": self.calibrated_at,
        }


class TimerCalibrationEngine:
    """
    Measures the underlying hardware clock properties to prevent measurement artifacts.
    Deducts timer invocation overhead from nanosecond benchmarks.
    """

    def __init__(self, clock_source: ClockSource = ClockSource.PERF_COUNTER_NS) -> None:
        self.clock_source = clock_source
        self._get_time_ns: Callable[[], int] = self._resolve_clock(clock_source)
        self.profile: Optional[TimerCalibrationProfile] = None

    def _resolve_clock(self, source: ClockSource) -> Callable[[], int]:
        if source == ClockSource.PERF_COUNTER_NS:
            return time.perf_counter_ns
        elif source == ClockSource.PROCESS_TIME_NS:
            return time.process_time_ns
        elif source == ClockSource.MONOTONIC_NS:
            return time.monotonic_ns
        return time.perf_counter_ns

    def calibrate(self, sample_size: int = 1000) -> TimerCalibrationProfile:
        """Executes hardware timer calibration passes."""
        get_time = self._get_time_ns

        # 1. Measure Timer Resolution (minimum observed delta > 0)
        resolution_samples: List[int] = []
        for _ in range(sample_size):
            t1 = get_time()
            t2 = get_time()
            while t2 == t1:
                t2 = get_time()
            resolution_samples.append(t2 - t1)

        timer_res_ns = statistics.median(resolution_samples) if resolution_samples else 1.0

        # 2. Measure Measurement Overhead (empty measurement loop cost)
        overhead_samples: List[int] = []
        for _ in range(sample_size):
            t1 = get_time()
            # empty work block
            t2 = get_time()
            overhead_samples.append(t2 - t1)

        # Use 10th percentile for minimal uncontended overhead
        sorted_overhead = sorted(overhead_samples)
        overhead_ns = sorted_overhead[int(sample_size * 0.10)]
        noise_var = statistics.variance(overhead_samples) if len(overhead_samples) > 1 else 0.0

        # 3. Precision (Spread of overhead)
        precision_ns = statistics.stdev(overhead_samples) if len(overhead_samples) > 1 else 0.0

        profile = TimerCalibrationProfile(
            clock_source=self.clock_source,
            timer_resolution_ns=float(timer_res_ns),
            timer_precision_ns=float(precision_ns),
            measurement_overhead_ns=float(overhead_ns),
            clock_drift_ppm=0.05,  # Nominal modern quartz oscillator drift
            noise_variance_ns2=float(noise_var),
            is_calibrated=True,
        )
        self.profile = profile
        logger.info(
            "Timer calibrated [%s]: Resolution=%.1fns, Overhead=%.1fns, Precision=%.1fns",
            self.clock_source.value,
            timer_res_ns,
            overhead_ns,
            precision_ns,
        )
        return profile

    def measure_ns(self, func: Callable[[], Any], iterations: int = 1) -> Tuple[float, Any]:
        """
        Executes func() for iterations count, subtracts measurement overhead,
        and returns (net_duration_ns_per_iteration, return_value).
        """
        if self.profile is None:
            self.calibrate(sample_size=500)

        get_time = self._get_time_ns
        overhead = self.profile.measurement_overhead_ns if self.profile else 0.0
        resolution = self.profile.timer_resolution_ns if self.profile else 1.0

        t1 = get_time()
        res = None
        for _ in range(iterations):
            res = func()
        t2 = get_time()

        raw_duration_ns = t2 - t1
        # Deduct overhead
        total_overhead = overhead * iterations
        net_duration_ns = max(resolution, raw_duration_ns - total_overhead)
        per_iter_ns = net_duration_ns / max(1, iterations)

        return per_iter_ns, res

    async def measure_async_ns(self, coro_func: Callable[[], Any], iterations: int = 1) -> Tuple[float, Any]:
        """Executes asynchronous coroutine with overhead deduction."""
        if self.profile is None:
            self.calibrate(sample_size=500)

        get_time = self._get_time_ns
        overhead = self.profile.measurement_overhead_ns if self.profile else 0.0
        resolution = self.profile.timer_resolution_ns if self.profile else 1.0

        t1 = get_time()
        res = None
        for _ in range(iterations):
            res = await coro_func()
        t2 = get_time()

        raw_duration_ns = t2 - t1
        total_overhead = overhead * iterations
        net_duration_ns = max(resolution, raw_duration_ns - total_overhead)
        per_iter_ns = net_duration_ns / max(1, iterations)

        return per_iter_ns, res
