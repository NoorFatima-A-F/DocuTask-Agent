"""
Benchmark Evidence Collector for Enterprise AAOS.
Measures latency distribution (P50, P90, P95, P99, Mean, StdDev), throughput (ops/sec),
and resource utilization to produce certified Benchmark EvidenceItems.
"""

from __future__ import annotations

import logging
import statistics
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.evidence.registry.evidence_models import EvidenceItem, EvidenceType, VerificationStatus

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkStats:
    """Statistical summary of benchmark execution."""

    name: str
    iterations: int
    mean_latency_ms: float
    median_latency_ms: float
    p50_latency_ms: float
    p90_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    std_dev_ms: float
    variance: float
    ops_per_second: float
    cpu_percent: float = 0.0
    ram_mb: float = 0.0
    failures: int = 0
    raw_latencies_ms: List[float] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "iterations": self.iterations,
            "mean_latency_ms": round(self.mean_latency_ms, 3),
            "median_latency_ms": round(self.median_latency_ms, 3),
            "p50_latency_ms": round(self.p50_latency_ms, 3),
            "p90_latency_ms": round(self.p90_latency_ms, 3),
            "p95_latency_ms": round(self.p95_latency_ms, 3),
            "p99_latency_ms": round(self.p99_latency_ms, 3),
            "std_dev_ms": round(self.std_dev_ms, 3),
            "variance": round(self.variance, 3),
            "ops_per_second": round(self.ops_per_second, 1),
            "cpu_percent": round(self.cpu_percent, 1),
            "ram_mb": round(self.ram_mb, 1),
            "failures": self.failures,
        }


class BenchmarkEvidenceCollector:
    """Collects and calculates statistical benchmark metrics."""

    @classmethod
    def compute_stats(
        cls,
        name: str,
        latencies_ms: List[float],
        total_time_seconds: float,
        failures: int = 0,
        cpu_pct: float = 0.0,
        ram_mb: float = 0.0,
    ) -> BenchmarkStats:
        """Computes statistical metrics across an array of latency measurements."""
        if not latencies_ms:
            return BenchmarkStats(
                name=name,
                iterations=0,
                mean_latency_ms=0.0,
                median_latency_ms=0.0,
                p50_latency_ms=0.0,
                p90_latency_ms=0.0,
                p95_latency_ms=0.0,
                p99_latency_ms=0.0,
                std_dev_ms=0.0,
                variance=0.0,
                ops_per_second=0.0,
                failures=failures,
            )

        n = len(latencies_ms)
        sorted_lat = sorted(latencies_ms)
        mean_lat = statistics.mean(latencies_ms)
        med_lat = statistics.median(latencies_ms)
        p50 = sorted_lat[int(n * 0.50)]
        p90 = sorted_lat[min(int(n * 0.90), n - 1)]
        p95 = sorted_lat[min(int(n * 0.95), n - 1)]
        p99 = sorted_lat[min(int(n * 0.99), n - 1)]
        std_dev = statistics.stdev(latencies_ms) if n > 1 else 0.0
        var = statistics.variance(latencies_ms) if n > 1 else 0.0
        ops_sec = (n / total_time_seconds) if total_time_seconds > 0 else 0.0

        return BenchmarkStats(
            name=name,
            iterations=n,
            mean_latency_ms=mean_lat,
            median_latency_ms=med_lat,
            p50_latency_ms=p50,
            p90_latency_ms=p90,
            p95_latency_ms=p95,
            p99_latency_ms=p99,
            std_dev_ms=std_dev,
            variance=var,
            ops_per_second=ops_sec,
            cpu_percent=cpu_pct,
            ram_mb=ram_mb,
            failures=failures,
            raw_latencies_ms=latencies_ms,
        )

    @classmethod
    def create_evidence_item(
        cls,
        stats: BenchmarkStats,
        source_module: str,
        artifact_path: Optional[str] = None,
    ) -> EvidenceItem:
        """Creates an EvidenceItem from benchmark statistics."""
        evi_id = f"evi_bench_{stats.name.lower().replace(' ', '_')}_{int(time.time())}"
        payload = stats.to_dict()

        return EvidenceItem(
            evidence_id=evi_id,
            title=f"Benchmark: {stats.name}",
            description=(
                f"Empirical benchmark for {stats.name} ({stats.iterations} iterations): "
                f"P50={stats.p50_latency_ms:.2f}ms, P95={stats.p95_latency_ms:.2f}ms, "
                f"P99={stats.p99_latency_ms:.2f}ms, Throughput={stats.ops_per_second:.1f} ops/s"
            ),
            evidence_type=EvidenceType.BENCHMARK,
            source=source_module,
            generated_by="benchmark_harness",
            artifact_location=artifact_path,
            verification_status=VerificationStatus.VERIFIED if stats.failures == 0 else VerificationStatus.FAILED_VERIFICATION,
            confidence=1.0,
            reproducibility="STATISTICAL",
            raw_payload=payload,
        )
