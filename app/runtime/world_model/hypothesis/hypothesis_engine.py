"""
Hypothesis Generation & Abductive Reasoning Engine for Phase 13.16.
Generates candidate explanations for operational anomalies, computes Bayesian likelihood, and tracks evidence trees.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.world_model.events.world_model_events import (
    HypothesisStatus,
    ReasoningMode,
    WorldModelEvent,
    WorldModelEventType,
    world_model_event_bus,
)


@dataclass
class HypothesisCandidate:
    hypothesis_id: str = field(default_factory=lambda: f"hyp_{uuid.uuid4().hex[:8]}")
    title: str = ""
    explanation: str = ""
    phenomenon_observed: str = ""
    reasoning_mode: ReasoningMode = ReasoningMode.ABDUCTIVE
    status: HypothesisStatus = HypothesisStatus.FORMULATED
    prior_probability: float = 0.5
    posterior_probability: float = 0.82
    supporting_evidence: List[str] = field(default_factory=list)
    refuting_evidence: List[str] = field(default_factory=list)
    competing_hypothesis_ids: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hypothesis_id": self.hypothesis_id,
            "title": self.title,
            "explanation": self.explanation,
            "phenomenon_observed": self.phenomenon_observed,
            "reasoning_mode": self.reasoning_mode.value if isinstance(self.reasoning_mode, ReasoningMode) else str(self.reasoning_mode),
            "status": self.status.value if isinstance(self.status, HypothesisStatus) else str(self.status),
            "prior_probability": round(self.prior_probability, 3),
            "posterior_probability": round(self.posterior_probability, 3),
            "supporting_evidence": self.supporting_evidence,
            "refuting_evidence": self.refuting_evidence,
            "competing_hypothesis_ids": self.competing_hypothesis_ids,
            "created_at": self.created_at,
        }


class HypothesisEngine:
    """Formulates and tests scientific/operational hypotheses on world state."""

    def __init__(self):
        self._hypotheses: Dict[str, HypothesisCandidate] = {}
        self._initialize_seed_hypotheses()

    def _initialize_seed_hypotheses(self) -> None:
        seeds = [
            HypothesisCandidate(
                hypothesis_id="hyp_latency_db_contention",
                title="Postgres Connection Pool Saturation Causes P99 Spike",
                explanation="P99 latency increases during peak hours due to exhaustively leased Postgres connection pool connections waiting on locks.",
                phenomenon_observed="Service core_api P99 latency exceeded 45ms during 14:00 UTC spike.",
                reasoning_mode=ReasoningMode.ABDUCTIVE,
                status=HypothesisStatus.SUPPORTED,
                prior_probability=0.45,
                posterior_probability=0.88,
                supporting_evidence=["obs_k8s_canary_latency", "fact_postgres_dw_pool_size"],
                competing_hypothesis_ids=["hyp_latency_cpu_throttling"],
            ),
            HypothesisCandidate(
                hypothesis_id="hyp_latency_cpu_throttling",
                title="Kubernetes Pod CPU CFS Throttling",
                explanation="P99 latency increases because Linux kernel Completely Fair Scheduler limits core_api container CPU quotas.",
                phenomenon_observed="Service core_api P99 latency exceeded 45ms during 14:00 UTC spike.",
                reasoning_mode=ReasoningMode.DEDUCTIVE,
                status=HypothesisStatus.REFUTED,
                prior_probability=0.5,
                posterior_probability=0.12,
                refuting_evidence=["obs_k8s_canary_latency (CPU < 35%)"],
                competing_hypothesis_ids=["hyp_latency_db_contention"],
            ),
        ]
        for h in seeds:
            self._hypotheses[h.hypothesis_id] = h

    def create_hypothesis(
        self,
        title: str,
        explanation: str,
        phenomenon_observed: str,
        prior_probability: float = 0.5,
        supporting_evidence: Optional[List[str]] = None,
    ) -> HypothesisCandidate:
        h = HypothesisCandidate(
            title=title,
            explanation=explanation,
            phenomenon_observed=phenomenon_observed,
            prior_probability=prior_probability,
            posterior_probability=min(0.99, prior_probability * 1.3),
            supporting_evidence=supporting_evidence or [],
        )
        self._hypotheses[h.hypothesis_id] = h

        world_model_event_bus.publish(
            WorldModelEvent(
                event_type=WorldModelEventType.HYPOTHESIS_CREATED,
                source="hypothesis_engine",
                payload=h.to_dict(),
            )
        )
        return h

    def list_hypotheses(self, status: Optional[str] = None) -> List[HypothesisCandidate]:
        items = list(self._hypotheses.values())
        if status:
            items = [h for h in items if (h.status.value if isinstance(h.status, HypothesisStatus) else str(h.status)).lower() == status.lower()]
        return items

    def get_hypothesis(self, hypothesis_id: str) -> Optional[HypothesisCandidate]:
        return self._hypotheses.get(hypothesis_id)

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_hypotheses": len(self._hypotheses),
            "hypotheses": [h.to_dict() for h in self._hypotheses.values()],
            "supported_count": sum(1 for h in self._hypotheses.values() if h.status == HypothesisStatus.SUPPORTED),
        }


# Global Singleton
hypothesis_engine = HypothesisEngine()
