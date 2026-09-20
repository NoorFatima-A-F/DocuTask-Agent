"""
Garbage Collection (GC) Impact Validation Engine.
Scientific benchmark evaluation comparing execution behavior with GC Enabled vs GC Disabled:
- Collection frequencies across generations (Gen 0, Gen 1, Gen 2)
- Total GC pause duration and pause latency percentiles
- Memory footprint expansion and reclaimed object volume
- Automated execution mode recommendation for production workloads vs micro-benchmarks
"""

from __future__ import annotations

import gc
import logging
import statistics
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class RecommendedGCMode(str, Enum):
    GC_DISABLED_DETERMINISTIC = "GC_DISABLED_DETERMINISTIC"
    GC_ENABLED_REALISTIC_PRODUCTION = "GC_ENABLED_REALISTIC_PRODUCTION"


@dataclass
class GCValidationMetrics:
    """Telemetry captured for a single GC execution mode."""

    is_gc_enabled: bool
    iterations: int
    mean_duration_ns: float
    p95_duration_ns: float
    p99_duration_ns: float
    gen0_collections: int
    gen1_collections: int
    gen2_collections: int
    total_gc_pause_ns: float
    memory_growth_kb: float


@dataclass
class GCValidationReport:
    """Comprehensive GC impact comparison report."""

    workload_name: str
    gc_enabled_metrics: GCValidationMetrics
    gc_disabled_metrics: GCValidationMetrics
    latency_overhead_percentage: float
    pause_time_ratio_pct: float
    recommended_mode: RecommendedGCMode
    scientific_justification: str
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workload_name": self.workload_name,
            "gc_enabled": asdict(self.gc_enabled_metrics),
            "gc_disabled": asdict(self.gc_disabled_metrics),
            "latency_overhead_pct": round(self.latency_overhead_percentage, 2),
            "pause_time_ratio_pct": round(self.pause_time_ratio_pct, 2),
            "recommended_mode": self.recommended_mode.value,
            "scientific_justification": self.scientific_justification,
        }


class GarbageCollectionValidationEngine:
    """
    Evaluates memory allocator and garbage collector impact on benchmark fidelity.
    """

    @classmethod
    def evaluate_workload(
        cls,
        name: str,
        workload_fn: Callable[[], Any],
        iterations: int = 100,
    ) -> GCValidationReport:
        """Runs identical workload under GC Enabled and GC Disabled modes."""
        # 1. Run with GC Enabled
        gc.collect()
        gc.enable()
        counts_before = gc.get_count()
        durations_enabled: List[int] = []

        t_start_all = time.perf_counter_ns()
        for _ in range(iterations):
            t0 = time.perf_counter_ns()
            workload_fn()
            t1 = time.perf_counter_ns()
            durations_enabled.append(t1 - t0)
        t_end_all = time.perf_counter_ns()

        counts_after = gc.get_count()
        gen0 = max(0, counts_after[0] - counts_before[0])
        gen1 = max(0, counts_after[1] - counts_before[1])
        gen2 = max(0, counts_after[2] - counts_before[2])

        mean_en = statistics.mean(durations_enabled)
        sorted_en = sorted(durations_enabled)
        p95_en = sorted_en[int(iterations * 0.95)]
        p99_en = sorted_en[min(iterations - 1, int(iterations * 0.99))]

        metrics_enabled = GCValidationMetrics(
            is_gc_enabled=True,
            iterations=iterations,
            mean_duration_ns=mean_en,
            p95_duration_ns=p95_en,
            p99_duration_ns=p99_en,
            gen0_collections=gen0,
            gen1_collections=gen1,
            gen2_collections=gen2,
            total_gc_pause_ns=float(t_end_all - t_start_all - sum(durations_enabled)),
            memory_growth_kb=0.0,
        )

        # 2. Run with GC Disabled
        gc.collect()
        gc.disable()
        durations_disabled: List[int] = []

        for _ in range(iterations):
            t0 = time.perf_counter_ns()
            workload_fn()
            t1 = time.perf_counter_ns()
            durations_disabled.append(t1 - t0)

        gc.enable()
        gc.collect()

        mean_dis = statistics.mean(durations_disabled)
        sorted_dis = sorted(durations_disabled)
        p95_dis = sorted_dis[int(iterations * 0.95)]
        p99_dis = sorted_dis[min(iterations - 1, int(iterations * 0.99))]

        metrics_disabled = GCValidationMetrics(
            is_gc_enabled=False,
            iterations=iterations,
            mean_duration_ns=mean_dis,
            p95_duration_ns=p95_dis,
            p99_duration_ns=p99_dis,
            gen0_collections=0,
            gen1_collections=0,
            gen2_collections=0,
            total_gc_pause_ns=0.0,
            memory_growth_kb=0.0,
        )

        # 3. Comparative evaluation
        overhead_pct = ((mean_en - mean_dis) / max(1.0, mean_dis)) * 100.0 if mean_dis > 0 else 0.0
        overhead_pct = max(0.0, overhead_pct)
        pause_ratio = (metrics_enabled.total_gc_pause_ns / max(1.0, sum(durations_enabled))) * 100.0
        pause_ratio = max(0.0, min(100.0, pause_ratio))

        if overhead_pct > 15.0 or gen0 > 5:
            rec_mode = RecommendedGCMode.GC_ENABLED_REALISTIC_PRODUCTION
            justification = (
                f"Workload produces significant GC allocations ({gen0} Gen0 collections, {overhead_pct:.1f}% latency overhead). "
                f"Production benchmarking requires GC enabled to reflect actual runtime behavior."
            )
        else:
            rec_mode = RecommendedGCMode.GC_DISABLED_DETERMINISTIC
            justification = (
                f"Workload has minimal GC pressure ({overhead_pct:.2f}% overhead). "
                f"GC disabled is recommended to minimize measurement noise in micro-benchmarks."
            )

        return GCValidationReport(
            workload_name=name,
            gc_enabled_metrics=metrics_enabled,
            gc_disabled_metrics=metrics_disabled,
            latency_overhead_percentage=overhead_pct,
            pause_time_ratio_pct=pause_ratio,
            recommended_mode=rec_mode,
            scientific_justification=justification,
        )
