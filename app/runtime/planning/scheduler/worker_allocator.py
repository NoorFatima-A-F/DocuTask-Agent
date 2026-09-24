"""
Intelligent Worker Allocation Engine.

Matches execution tasks to heterogeneous worker pools based on capability fit,
availability, queue backlog, historical failure rate, and latency performance.
"""

from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel
from app.runtime.planning.graph.node import DAGNode


class WorkerDescriptor(BaseModel):
    worker_id: str
    name: str
    capabilities: List[str]  # e.g., ["OCR", "VISION", "NLP", "SMT", "REFLECTION"]
    status: str = "IDLE"     # IDLE, BUSY, OFFLINE
    active_tasks: int = 0
    max_concurrency: int = 4
    historical_success_rate: float = 0.98
    average_latency_ms: float = 200.0


class WorkerAllocator:
    """Allocates ready tasks to optimal worker instances."""

    def __init__(self, initial_workers: Optional[List[WorkerDescriptor]] = None) -> None:
        self.workers: Dict[str, WorkerDescriptor] = {}
        if initial_workers:
            for w in initial_workers:
                self.workers[w.worker_id] = w
        else:
            self._init_default_worker_pool()

    def _init_default_worker_pool(self) -> None:
        defaults = [
            WorkerDescriptor(worker_id="worker_ocr_01", name="OCR GPU Worker 1", capabilities=["OCR", "VISION", "GENERAL"]),
            WorkerDescriptor(worker_id="worker_ocr_02", name="OCR GPU Worker 2", capabilities=["OCR", "VISION", "GENERAL"]),
            WorkerDescriptor(worker_id="worker_nlp_01", name="NLP Extraction Worker 1", capabilities=["EXTRACTION", "NLP", "GENERAL"]),
            WorkerDescriptor(worker_id="worker_nlp_02", name="NLP Extraction Worker 2", capabilities=["EXTRACTION", "NLP", "GENERAL"]),
            WorkerDescriptor(worker_id="worker_smt_01", name="Formal SMT Governance Worker", capabilities=["VALIDATION", "GOVERNANCE", "SMT", "GENERAL"]),
            WorkerDescriptor(worker_id="worker_meta_01", name="Meta-Cognitive Reflection Worker", capabilities=["REFLECTION", "MEMORY", "GENERAL"]),
        ]
        for w in defaults:
            self.workers[w.worker_id] = w

    def allocate_worker(self, node: DAGNode) -> Optional[WorkerDescriptor]:
        """
        Finds the highest-utility available worker for the given node:
        Score = w_cap * CapabilityMatch + w_avail * Availability + w_rel * SuccessRate - w_load * (ActiveTasks/MaxConcurrency)
        """
        required_caps = set(node.required_capabilities)
        candidates = []

        for w in self.workers.values():
            if w.status == "OFFLINE":
                continue
            if w.active_tasks >= w.max_concurrency:
                continue

            # Check capabilities
            worker_caps = set(w.capabilities)
            if not required_caps.issubset(worker_caps) and "GENERAL" not in worker_caps:
                continue

            # Match score
            cap_match = len(required_caps.intersection(worker_caps)) / max(1, len(required_caps))
            load_factor = w.active_tasks / max(1, w.max_concurrency)
            score = (
                0.40 * cap_match
                + 0.30 * w.historical_success_rate
                + 0.30 * (1.0 - load_factor)
            )
            candidates.append((score, w))

        if not candidates:
            # Fallback to any worker with lowest load
            idle_workers = sorted(self.workers.values(), key=lambda x: x.active_tasks)
            return idle_workers[0] if idle_workers else None

        candidates.sort(key=lambda x: x[0], reverse=True)
        chosen_worker = candidates[0][1]
        chosen_worker.active_tasks += 1
        chosen_worker.status = "BUSY" if chosen_worker.active_tasks >= chosen_worker.max_concurrency else "IDLE"
        return chosen_worker

    def release_worker(self, worker_id: str) -> None:
        """Releases a worker upon task completion."""
        if worker_id in self.workers:
            w = self.workers[worker_id]
            w.active_tasks = max(0, w.active_tasks - 1)
            w.status = "IDLE"
