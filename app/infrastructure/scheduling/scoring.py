"""Placement Scoring Engine for Candidate Ranking."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.executions.workload import WorkloadRequest
from app.infrastructure.workers.models import Worker
from app.infrastructure.workers.capabilities import WorkerCapabilityRegistry
from app.infrastructure.scheduling.affinity import AffinityEngine
from app.infrastructure.scheduling.fairness import FairnessScheduler


class ScoreBreakdown(BaseModel):
    """Detailed components of a worker's placement score."""

    worker_id: str
    total_score: float
    resource_fit_score: float = 0.0
    capability_score: float = 0.0
    affinity_score: float = 0.0
    load_score: float = 0.0
    fairness_penalty: float = 0.0


class PlacementScoringEngine:
    """Computes weighted multi-factor scores to select the optimal worker candidate."""

    def __init__(
        self,
        capability_registry: Optional[WorkerCapabilityRegistry] = None,
        affinity_engine: Optional[AffinityEngine] = None,
        fairness_scheduler: Optional[FairnessScheduler] = None,
        resource_weight: float = 1.0,
        capability_weight: float = 1.0,
        affinity_weight: float = 1.0,
        load_weight: float = 0.5,
    ) -> None:
        self.capability_registry = capability_registry or WorkerCapabilityRegistry()
        self.affinity_engine = affinity_engine or AffinityEngine()
        self.fairness_scheduler = fairness_scheduler or FairnessScheduler()
        self.resource_weight = resource_weight
        self.capability_weight = capability_weight
        self.affinity_weight = affinity_weight
        self.load_weight = load_weight

    def score_candidate(self, worker: Worker, workload: WorkloadRequest) -> ScoreBreakdown:
        """Compute composite placement score for a single candidate worker."""
        # 1. Resource fit: available CPU & memory headroom
        avail = worker.resource_available
        req = workload.resource_requirements
        cpu_headroom = max(0.0, avail.cpu_cores - req.cpu_cores)
        mem_headroom = max(0.0, avail.memory_gb - req.memory_gb)
        resource_score = (cpu_headroom * 2.0) + (mem_headroom * 0.5)

        # 2. Capability score
        cap_score = self.capability_registry.calculate_capability_match_score(
            worker.worker_id, workload.required_capabilities, workload.optional_capabilities
        ) * 10.0

        # 3. Affinity & Locality score
        aff_score = self.affinity_engine.calculate_affinity_score(worker, workload)

        # 4. Load score: higher free slots = higher score
        load_score = float(avail.worker_slots) * 2.0

        # 5. Fairness penalty
        fairness_pen = self.fairness_scheduler.calculate_fairness_penalty(workload.tenant_id) * 20.0

        total = (
            (resource_score * self.resource_weight)
            + (cap_score * self.capability_weight)
            + (aff_score * self.affinity_weight)
            + (load_score * self.load_weight)
            - fairness_pen
        )

        return ScoreBreakdown(
            worker_id=worker.worker_id,
            total_score=total,
            resource_fit_score=resource_score,
            capability_score=cap_score,
            affinity_score=aff_score,
            load_score=load_score,
            fairness_penalty=fairness_pen,
        )

    def rank_candidates(
        self, workers: List[Worker], workload: WorkloadRequest
    ) -> List[ScoreBreakdown]:
        """Score and sort worker candidates descending by total score."""
        scored = [self.score_candidate(w, workload) for w in workers]
        return sorted(scored, key=lambda s: s.total_score, reverse=True)
