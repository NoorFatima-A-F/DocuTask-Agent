"""
ARTEICP Resource Scheduler - Heterogeneous Worker Pool
Manages dedicated worker pools: OCR Workers, LLM Reasoning Workers, Validation Workers, Memory Workers.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import time


@dataclass
class WorkerInstance:
    worker_id: str
    pool_type: str  # OCR_POOL | LLM_POOL | VALIDATION_POOL | MEMORY_POOL
    concurrency_limit: int
    active_jobs: int
    is_healthy: bool = True
    total_completed: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class WorkerPoolManager:
    """Manages allocation and capacity of heterogeneous worker pools."""

    def __init__(self):
        self.pools: Dict[str, List[WorkerInstance]] = {
            "OCR_POOL": [
                WorkerInstance("ocr_w_1", "OCR_POOL", concurrency_limit=2, active_jobs=1, total_completed=340),
                WorkerInstance("ocr_w_2", "OCR_POOL", concurrency_limit=2, active_jobs=0, total_completed=290),
            ],
            "LLM_POOL": [
                WorkerInstance("llm_w_1", "LLM_POOL", concurrency_limit=4, active_jobs=2, total_completed=850),
                WorkerInstance("llm_w_2", "LLM_POOL", concurrency_limit=4, active_jobs=1, total_completed=790),
            ],
            "VALIDATION_POOL": [
                WorkerInstance("val_w_1", "VALIDATION_POOL", concurrency_limit=8, active_jobs=0, total_completed=610),
            ],
            "MEMORY_POOL": [
                WorkerInstance("mem_w_1", "MEMORY_POOL", concurrency_limit=4, active_jobs=0, total_completed=420),
            ],
        }

    def allocate_worker(self, pool_type: str) -> Optional[WorkerInstance]:
        pool = self.pools.get(pool_type, [])
        # Least loaded worker
        available = [w for w in pool if w.active_jobs < w.concurrency_limit]
        if not available:
            return None
        selected = min(available, key=lambda w: w.active_jobs)
        selected.active_jobs += 1
        return selected

    def release_worker(self, worker_id: str):
        for pool in self.pools.values():
            for w in pool:
                if w.worker_id == worker_id:
                    w.active_jobs = max(0, w.active_jobs - 1)
                    w.total_completed += 1
                    return

    def get_pool_status(self) -> Dict[str, Any]:
        summary = {}
        for p_name, workers in self.pools.items():
            tot_cap = sum(w.concurrency_limit for w in workers)
            tot_act = sum(w.active_jobs for w in workers)
            summary[p_name] = {
                "worker_count": len(workers),
                "total_capacity": tot_cap,
                "active_jobs": tot_act,
                "utilization_pct": round((tot_act / max(1, tot_cap)) * 100, 1),
                "workers": [w.to_dict() for w in workers],
            }
        return summary
