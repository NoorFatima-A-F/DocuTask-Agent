"""
Worker Load Balancer.

Calculates load balancing distributions across heterogeneous worker pools.
"""

from __future__ import annotations

from typing import Dict, List
from app.runtime.planning.scheduler.worker_allocator import WorkerDescriptor


class LoadBalancer:
    """Computes cluster load variance and recommends distribution adjustments."""

    @staticmethod
    def calculate_utilization(workers: List[WorkerDescriptor]) -> Dict[str, float]:
        """Returns per-worker and cluster-wide utilization rates."""
        if not workers:
            return {"mean_utilization": 0.0, "max_utilization": 0.0}

        utils = [w.active_tasks / max(1, w.max_concurrency) for w in workers]
        mean_u = sum(utils) / len(utils)
        max_u = max(utils)
        return {
            "mean_utilization": round(mean_u, 3),
            "max_utilization": round(max_u, 3),
            "idle_workers_count": float(sum(1 for u in utils if u == 0.0)),
            "busy_workers_count": float(sum(1 for u in utils if u >= 1.0)),
        }
