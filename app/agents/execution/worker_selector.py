"""
Worker Selector.
Selects optimal worker candidate based on capability matching and workload.
"""

from typing import List, Optional
from app.agents.execution.worker import Worker, WorkerStatus


class WorkerSelector:
    """Selects an available worker matching capability requirements."""

    def select_worker(self, candidates: List[Worker], required_capability: Optional[str] = None) -> Optional[Worker]:
        idle_workers = [w for w in candidates if w.status == WorkerStatus.IDLE]
        if not idle_workers:
            return None

        if not required_capability or required_capability == "DEFAULT":
            return idle_workers[0]

        for w in idle_workers:
            if required_capability in w.capabilities or "ALL" in w.capabilities:
                return w

        # Default fallback to first idle worker if compatible
        return idle_workers[0]
