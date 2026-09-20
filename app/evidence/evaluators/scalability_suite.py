"""
Scalability Validation Suite for Enterprise AAOS.
Simulates concurrent worker loads across exponential scales:
1, 10, 100, 500, 1,000, 5,000, 10,000 concurrent virtual agents.
Measures throughput (ops/sec), p50/p95/p99 latency, queue depth, and contention rates.
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.evidence.collectors.benchmark_collector import BenchmarkEvidenceCollector
from app.evidence.registry.evidence_models import EvidenceItem, EvidenceType, VerificationStatus
from app.evidence.registry.evidence_registry import EvidenceRegistry

from app.agents.runtime.distributed.distributed_lock import DistributedLockManager, DistributedWorkflowStateManager

logger = logging.getLogger(__name__)


@dataclass
class ScalabilityTierResult:
    """Performance metrics for a specific concurrent worker tier."""

    worker_count: int
    total_operations: int
    successful_ops: int
    failed_ops: int
    duration_seconds: float
    throughput_ops_sec: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    max_queue_depth: int
    contention_rate_pct: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "worker_count": self.worker_count,
            "total_operations": self.total_operations,
            "successful_ops": self.successful_ops,
            "failed_ops": self.failed_ops,
            "duration_seconds": round(self.duration_seconds, 3),
            "throughput_ops_sec": round(self.throughput_ops_sec, 1),
            "p50_latency_ms": round(self.p50_latency_ms, 2),
            "p95_latency_ms": round(self.p95_latency_ms, 2),
            "p99_latency_ms": round(self.p99_latency_ms, 2),
            "max_queue_depth": self.max_queue_depth,
            "contention_rate_pct": round(self.contention_rate_pct, 2),
        }


class ScalabilityValidationLaboratory:
    """Simulates high-density distributed agent concurrency loads."""

    def __init__(self, registry: Optional[EvidenceRegistry] = None) -> None:
        self.registry = registry or EvidenceRegistry()
        self.tier_results: Dict[int, ScalabilityTierResult] = {}

    async def run_scalability_matrix(
        self,
        worker_tiers: Optional[List[int]] = None,
    ) -> List[EvidenceItem]:
        """Runs scalability tests across worker tiers and records evidence items."""
        tiers = worker_tiers or [1, 10, 100, 500, 1000]
        evidence_items: List[EvidenceItem] = []

        for count in tiers:
            res = await self.simulate_worker_tier(worker_count=count, ops_per_worker=2)
            self.tier_results[count] = res

            evi = EvidenceItem(
                evidence_id=f"evi_scale_w{count}_{int(time.time())}",
                title=f"Scalability Benchmark: {count} Concurrent Workers",
                description=(
                    f"Scalability test for {count} workers: Throughput={res.throughput_ops_sec:.1f} ops/s, "
                    f"P95={res.p95_latency_ms:.2f}ms, Success Rate={(res.successful_ops/res.total_operations)*100:.1f}%"
                ),
                evidence_type=EvidenceType.STRESS_TEST if count >= 500 else EvidenceType.LOAD_TEST,
                source="app.evidence.evaluators.scalability_suite",
                generated_by="scalability_laboratory",
                verification_status=VerificationStatus.VERIFIED if res.failed_ops == 0 else VerificationStatus.FAILED_VERIFICATION,
                confidence=1.0,
                reproducibility="STATISTICAL",
                raw_payload=res.to_dict(),
            )
            self.registry.register(evi)
            evidence_items.append(evi)

        return evidence_items

    async def simulate_worker_tier(self, worker_count: int, ops_per_worker: int = 2) -> ScalabilityTierResult:
        """Simulates concurrent workers acquiring distributed locks and committing state."""
        lock_mgr = DistributedLockManager(default_ttl_seconds=5.0)
        state_mgr = DistributedWorkflowStateManager()

        total_ops = worker_count * ops_per_worker
        latencies: List[float] = []
        failures = 0
        successes = 0
        active_workers = 0
        max_active = 0
        queue_lock = asyncio.Lock()

        async def worker_task(worker_id: int) -> None:
            nonlocal active_workers, max_active, successes, failures
            async with queue_lock:
                active_workers += 1
                if active_workers > max_active:
                    max_active = active_workers

            for op_idx in range(ops_per_worker):
                res_id = f"doc_resource_{(worker_id + op_idx) % max(1, worker_count // 5)}"
                s = time.perf_counter()
                try:
                    lease = await lock_mgr.acquire_lock(res_id, f"worker_{worker_id}", ttl_seconds=1.0, timeout_seconds=2.0)
                    if lease:
                        # Commit state under lock
                        await state_mgr.commit_state(f"sess_{worker_id}", {"w": worker_id, "op": op_idx}, expected_version=op_idx)
                        await lock_mgr.release_lock(lease)
                        successes += 1
                    else:
                        failures += 1
                except Exception:
                    failures += 1

                latencies.append((time.perf_counter() - s) * 1000.0)

            async with queue_lock:
                active_workers -= 1

        t0 = time.perf_counter()
        tasks = [worker_task(i) for i in range(worker_count)]
        await asyncio.gather(*tasks)
        duration = max(0.001, time.perf_counter() - t0)

        sorted_lat = sorted(latencies) if latencies else [0.0]
        n = len(sorted_lat)
        p50 = sorted_lat[int(n * 0.50)]
        p95 = sorted_lat[min(int(n * 0.95), n - 1)]
        p99 = sorted_lat[min(int(n * 0.99), n - 1)]
        throughput = total_ops / duration
        contention_pct = (lock_mgr.contention_count / max(1, lock_mgr.acquisition_count + lock_mgr.contention_count)) * 100.0

        return ScalabilityTierResult(
            worker_count=worker_count,
            total_operations=total_ops,
            successful_ops=successes,
            failed_ops=failures,
            duration_seconds=duration,
            throughput_ops_sec=throughput,
            p50_latency_ms=p50,
            p95_latency_ms=p95,
            p99_latency_ms=p99,
            max_queue_depth=max_active,
            contention_rate_pct=contention_pct,
        )
