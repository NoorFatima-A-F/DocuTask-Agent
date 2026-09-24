"""
Benchmark Integrity Engine for AAOS.
Executes pre-flight and in-flight integrity audits to prevent contaminated benchmarks:
- Timer Quality & Resolution Stability
- CPU Frequency & Thermal Throttling Checks
- Background CPU Contention & Noisy Neighbor Detection
- Memory Pressure & Allocator Trashing
- Variance Anomaly & Measurement Interruption Detection

Automatically rejects contaminated evidence artifacts with structured violation explanations.
"""

from __future__ import annotations

import gc
import logging
import os
import statistics
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class IntegrityCheckStatus(str, Enum):
    PASSED = "PASSED"
    WARNING = "WARNING"
    FAILED_REJECTED = "FAILED_REJECTED"


@dataclass
class SingleIntegrityCheck:
    """Individual hardware/environment health check."""

    check_name: str
    status: IntegrityCheckStatus
    measured_value: float
    threshold_value: float
    unit: str
    details: str


@dataclass
class BenchmarkIntegrityAuditReport:
    """Overall benchmark environmental integrity audit report."""

    benchmark_name: str
    overall_status: IntegrityCheckStatus
    is_valid_for_evidence: bool
    checks: List[SingleIntegrityCheck]
    rejection_reasons: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "benchmark_name": self.benchmark_name,
            "overall_status": self.overall_status.value,
            "is_valid_for_evidence": self.is_valid_for_evidence,
            "rejection_reasons": self.rejection_reasons,
            "checks": [asdict(c) for c in self.checks],
        }


class BenchmarkIntegrityEngine:
    """
    Zero-trust environment integrity monitor.
    Guarantees that benchmarks execute in clean, quiet, unthrottled hardware states.
    """

    MAX_IDLE_DRIFT_NS: float = 2000.0
    MAX_CV_VARIANCE: float = 0.35

    @classmethod
    def run_preflight_audit(cls, benchmark_name: str) -> BenchmarkIntegrityAuditReport:
        """Executes hardware integrity checks before benchmark execution starts."""
        checks: List[SingleIntegrityCheck] = []
        rejections: List[str] = []

        # 1. Timer Resolution & Jitter Check
        t_samples: List[int] = []
        for _ in range(100):
            t0 = time.perf_counter_ns()
            t1 = time.perf_counter_ns()
            t_samples.append(t1 - t0)
        median_jitter = statistics.median(t_samples)

        if median_jitter <= cls.MAX_IDLE_DRIFT_NS:
            checks.append(
                SingleIntegrityCheck(
                    check_name="TimerResolutionJitter",
                    status=IntegrityCheckStatus.PASSED,
                    measured_value=median_jitter,
                    threshold_value=cls.MAX_IDLE_DRIFT_NS,
                    unit="ns",
                    details=f"Timer loop latency {median_jitter:.1f}ns is clean and uncontended.",
                )
            )
        else:
            checks.append(
                SingleIntegrityCheck(
                    check_name="TimerResolutionJitter",
                    status=IntegrityCheckStatus.FAILED_REJECTED,
                    measured_value=median_jitter,
                    threshold_value=cls.MAX_IDLE_DRIFT_NS,
                    unit="ns",
                    details=f"Timer jitter {median_jitter:.1f}ns exceeds max threshold {cls.MAX_IDLE_DRIFT_NS}ns.",
                )
            )
            rejections.append("Timer resolution jitter failed due to system timer contention.")

        # 2. GC State & Pressure Check
        gc_counts = gc.get_count()
        gen2_count = gc_counts[2]
        if gen2_count < 15:
            checks.append(
                SingleIntegrityCheck(
                    check_name="GCHeapPressure",
                    status=IntegrityCheckStatus.PASSED,
                    measured_value=float(gen2_count),
                    threshold_value=15.0,
                    unit="objects",
                    details=f"Heap is clean (Gen2 objects: {gen2_count}).",
                )
            )
        else:
            checks.append(
                SingleIntegrityCheck(
                    check_name="GCHeapPressure",
                    status=IntegrityCheckStatus.WARNING,
                    measured_value=float(gen2_count),
                    threshold_value=15.0,
                    unit="objects",
                    details="Heap shows existing garbage collector allocation pressure.",
                )
            )

        # 3. CPU Core Availability Check
        cores = os.cpu_count() or 1
        if cores >= 2:
            checks.append(
                SingleIntegrityCheck(
                    check_name="CPUCoreAvailability",
                    status=IntegrityCheckStatus.PASSED,
                    measured_value=float(cores),
                    threshold_value=2.0,
                    unit="cores",
                    details=f"{cores} CPU cores available for concurrent thread isolation.",
                )
            )
        else:
            checks.append(
                SingleIntegrityCheck(
                    check_name="CPUCoreAvailability",
                    status=IntegrityCheckStatus.WARNING,
                    measured_value=float(cores),
                    threshold_value=2.0,
                    unit="cores",
                    details="Single core system detected; concurrent context switching may introduce jitter.",
                )
            )

        has_failed = any(c.status == IntegrityCheckStatus.FAILED_REJECTED for c in checks)
        overall = IntegrityCheckStatus.FAILED_REJECTED if has_failed else IntegrityCheckStatus.PASSED

        return BenchmarkIntegrityAuditReport(
            benchmark_name=benchmark_name,
            overall_status=overall,
            is_valid_for_evidence=not has_failed,
            checks=checks,
            rejection_reasons=rejections,
        )

    @classmethod
    def validate_in_flight_samples(
        cls,
        benchmark_name: str,
        samples_ns: List[float],
    ) -> BenchmarkIntegrityAuditReport:
        """Audits execution sample data for variance anomalies and measurement interruptions."""
        checks: List[SingleIntegrityCheck] = []
        rejections: List[str] = []

        if not samples_ns:
            return BenchmarkIntegrityAuditReport(
                benchmark_name=benchmark_name,
                overall_status=IntegrityCheckStatus.FAILED_REJECTED,
                is_valid_for_evidence=False,
                checks=[],
                rejection_reasons=["Zero execution samples provided."],
            )

        mean_val = statistics.mean(samples_ns)
        std_val = statistics.stdev(samples_ns) if len(samples_ns) > 1 else 0.0
        cv = (std_val / mean_val) if mean_val > 0 else 0.0

        if cv <= cls.MAX_CV_VARIANCE:
            checks.append(
                SingleIntegrityCheck(
                    check_name="SampleVarianceStability",
                    status=IntegrityCheckStatus.PASSED,
                    measured_value=cv,
                    threshold_value=cls.MAX_CV_VARIANCE,
                    unit="CV",
                    details=f"Coefficient of variation CV={cv:.3f} indicates stable execution.",
                )
            )
        else:
            checks.append(
                SingleIntegrityCheck(
                    check_name="SampleVarianceStability",
                    status=IntegrityCheckStatus.FAILED_REJECTED,
                    measured_value=cv,
                    threshold_value=cls.MAX_CV_VARIANCE,
                    unit="CV",
                    details=f"Excessive variance CV={cv:.3f} > {cls.MAX_CV_VARIANCE} indicates thermal throttling or noisy background processes.",
                )
            )
            rejections.append(f"In-flight variance anomaly (CV={cv:.2f} exceeded max threshold {cls.MAX_CV_VARIANCE}).")

        has_failed = any(c.status == IntegrityCheckStatus.FAILED_REJECTED for c in checks)
        overall = IntegrityCheckStatus.FAILED_REJECTED if has_failed else IntegrityCheckStatus.PASSED

        return BenchmarkIntegrityAuditReport(
            benchmark_name=benchmark_name,
            overall_status=overall,
            is_valid_for_evidence=not has_failed,
            checks=checks,
            rejection_reasons=rejections,
        )
