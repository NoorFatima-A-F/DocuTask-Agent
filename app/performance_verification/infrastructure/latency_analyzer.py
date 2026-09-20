"""
High-precision latency analyzer with percentile computation and histogram bucketing.
"""

import math
from typing import List, Dict, Any
from app.performance_verification.domain.models import LatencyDistribution


class LatencyAnalyzer:
    """Calculates percentile latencies (P50, P90, P95, P99, Max, Mean, StdDev)."""

    @staticmethod
    def compute_distribution(
        latencies_ms: List[float],
        sla_target_p95_ms: float = 1000.0,
    ) -> LatencyDistribution:
        """Computes full mathematical distribution from a list of latency samples."""
        if not latencies_ms:
            return LatencyDistribution(
                p50_ms=0.0,
                p90_ms=0.0,
                p95_ms=0.0,
                p99_ms=0.0,
                max_ms=0.0,
                mean_ms=0.0,
                std_dev_ms=0.0,
                sample_count=0,
                sla_target_p95_ms=sla_target_p95_ms,
                sla_met=True,
            )

        sorted_latencies = sorted(latencies_ms)
        n = len(sorted_latencies)

        def get_percentile(p: float) -> float:
            k = (n - 1) * p
            f = math.floor(k)
            c = math.ceil(k)
            if f == c:
                return sorted_latencies[int(k)]
            d0 = sorted_latencies[int(f)] * (c - k)
            d1 = sorted_latencies[int(c)] * (k - f)
            return d0 + d1

        p50 = get_percentile(0.50)
        p90 = get_percentile(0.90)
        p95 = get_percentile(0.95)
        p99 = get_percentile(0.99)
        max_val = sorted_latencies[-1]
        mean_val = sum(sorted_latencies) / n

        variance = sum((x - mean_val) ** 2 for x in sorted_latencies) / n
        std_dev = math.sqrt(variance)

        sla_met = p95 <= sla_target_p95_ms

        return LatencyDistribution(
            p50_ms=p50,
            p90_ms=p90,
            p95_ms=p95,
            p99_ms=p99,
            max_ms=max_val,
            mean_ms=mean_val,
            std_dev_ms=std_dev,
            sample_count=n,
            sla_target_p95_ms=sla_target_p95_ms,
            sla_met=sla_met,
        )

    @staticmethod
    def bucket_histogram(
        latencies_ms: List[float],
        buckets_ms: List[float] = None,
    ) -> Dict[str, int]:
        """Buckets latencies into histogram bins."""
        if buckets_ms is None:
            buckets_ms = [50.0, 100.0, 250.0, 500.0, 1000.0, 2500.0, 5000.0]

        counts = {f"<={b}ms": 0 for b in buckets_ms}
        counts[f">{buckets_ms[-1]}ms"] = 0

        for lat in latencies_ms:
            placed = False
            for b in buckets_ms:
                if lat <= b:
                    counts[f"<={b}ms"] += 1
                    placed = True
                    break
            if not placed:
                counts[f">{buckets_ms[-1]}ms"] += 1

        return counts
