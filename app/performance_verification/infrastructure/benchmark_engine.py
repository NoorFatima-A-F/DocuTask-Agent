"""
Benchmark execution engine supporting synthetic enterprise workloads and concurrency simulation.
"""

import time
import random
from typing import Callable, List, Dict, Any, Optional
from app.performance_verification.infrastructure.latency_analyzer import LatencyAnalyzer
from app.performance_verification.domain.models import LatencyDistribution, PerformanceStatus


class BenchmarkEngine:
    """Simulates multi-threaded or concurrent enterprise AI task execution."""

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def run_workload(
        self,
        name: str,
        iterations: int,
        concurrency: int,
        task_fn: Optional[Callable[[int], float]] = None,
        sla_target_p95_ms: float = 1000.0,
        base_latency_ms: float = 150.0,
        jitter_ms: float = 50.0,
    ) -> Dict[str, Any]:
        """Executes a workload benchmark and returns timing and latency distributions."""
        latencies: List[float] = []
        errors = 0

        start_wall = time.perf_counter()

        for i in range(iterations):
            if task_fn:
                try:
                    t_start = time.perf_counter()
                    task_fn(i)
                    t_end = time.perf_counter()
                    lat = (t_end - t_start) * 1000.0
                except Exception:
                    errors += 1
                    lat = base_latency_ms * 2.0
            else:
                # Deterministic synthetic simulation with concurrency backpressure
                concurrency_penalty = 1.0 + (concurrency / 200.0)
                random_jitter = self.rng.uniform(-jitter_ms, jitter_ms)
                lat = max(5.0, (base_latency_ms + random_jitter) * concurrency_penalty)

            latencies.append(lat)

        duration_sec = time.perf_counter() - start_wall

        distribution = LatencyAnalyzer.compute_distribution(
            latencies, sla_target_p95_ms=sla_target_p95_ms
        )

        error_rate_pct = (errors / iterations * 100.0) if iterations > 0 else 0.0
        status = PerformanceStatus.OPTIMAL
        if not distribution.sla_met:
            status = PerformanceStatus.DEGRADED
        if error_rate_pct > 1.0:
            status = PerformanceStatus.FAILED

        return {
            "workload_name": name,
            "iterations": iterations,
            "concurrency": concurrency,
            "duration_sec": duration_sec,
            "throughput_req_sec": round(iterations / max(0.001, duration_sec), 2),
            "errors": errors,
            "error_rate_pct": error_rate_pct,
            "latency": distribution,
            "status": status,
        }
