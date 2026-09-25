"""
Hypothesis Generation Engine for Phase 13.12 (ASD-HGCKEP).
Automated Knowledge-Gap Detection, Assumption Mining, and Information Gain-driven Hypothesis Generation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import math
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.science.events.science_events import (
    HypothesisStatus,
    ResearchPriority,
    ScienceEventBus,
    ScientificDomainEvent,
    ScientificEventType,
    ScientificHypothesisCreated,
    ScientificHypothesisRejected,
    HypothesisRetired,
)


@dataclass
class KnowledgeGap:
    gap_id: str = field(default_factory=lambda: f"gap_{uuid.uuid4().hex[:8]}")
    domain: str = "performance"
    description: str = "Uncharacterized memory eviction latency during burst ingestion."
    priority: ResearchPriority = ResearchPriority.HIGH
    impact_score: float = 0.85
    identified_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gap_id": self.gap_id,
            "domain": self.domain,
            "description": self.description,
            "priority": self.priority.value if hasattr(self.priority, "value") else str(self.priority),
            "impact_score": round(self.impact_score, 4),
            "identified_at": self.identified_at.isoformat(),
        }


@dataclass
class ScientificHypothesis:
    hypothesis_id: str = field(default_factory=lambda: f"hypo_{uuid.uuid4().hex[:8]}")
    title: str = "Speculative Tensor Eviction Invariant"
    statement: str = "Adaptive cache eviction reduces latency by 25%."
    domain: str = "performance"
    rationale: str = "Observed high entropy in historical replay traces."
    premise: str = "Telemetry reveals high cache contention under burst load."
    predicted_effect: str = "25% reduction in P95 latency."
    variables: List[str] = field(default_factory=lambda: ["cache_ttl", "burst_rate", "latency_ms"])
    expected_information_gain: float = 0.85
    prior_probability: float = 0.50
    status: HypothesisStatus = HypothesisStatus.PROPOSED
    priority: ResearchPriority = ResearchPriority.HIGH
    tags: List[str] = field(default_factory=list)
    knowledge_gap_id: Optional[str] = None
    supporting_evidence_ids: List[str] = field(default_factory=list)
    age_days: int = 1
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hypothesis_id": self.hypothesis_id,
            "title": self.title,
            "statement": self.statement,
            "domain": self.domain,
            "rationale": self.rationale,
            "premise": self.premise,
            "predicted_effect": self.predicted_effect,
            "variables": self.variables,
            "expected_information_gain": round(self.expected_information_gain, 4),
            "prior_probability": round(self.prior_probability, 4),
            "status": self.status.value if hasattr(self.status, "value") else str(self.status),
            "priority": self.priority.value if hasattr(self.priority, "value") else str(self.priority),
            "tags": self.tags,
            "knowledge_gap_id": self.knowledge_gap_id,
            "supporting_evidence_ids": self.supporting_evidence_ids,
            "age_days": self.age_days,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class HypothesisEngine:
    """
    Autonomous Hypothesis Engine. Formulates testable propositions with Bayesian priors and Information Gain.
    """

    def __init__(self, event_bus: Optional[ScienceEventBus] = None) -> None:
        self.event_bus = event_bus or ScienceEventBus()
        self.hypotheses: Dict[str, ScientificHypothesis] = {}
        self.knowledge_gaps: Dict[str, KnowledgeGap] = {}
        self._initialize_bootstrap_science()

    def _initialize_bootstrap_science(self) -> None:
        g1 = KnowledgeGap(
            gap_id="gap_seed_01",
            domain="performance",
            description="Optimal context cache size during distributed swarm operations.",
            priority=ResearchPriority.HIGH,
            impact_score=0.88,
        )
        self.knowledge_gaps[g1.gap_id] = g1

        h1 = ScientificHypothesis(
            hypothesis_id="hypo_seed_01",
            title="Speculative Vector Prewarming Hypothesis",
            statement="Pre-warming embeddings for frequent schema paths reduces reasoning latency by >=20%.",
            domain="performance",
            rationale="Spatial locality in document parsing workloads indicates repeated vector queries.",
            prior_probability=0.75,
            expected_information_gain=0.82,
            tags=["vector_cache", "prewarming", "performance"],
            knowledge_gap_id=g1.gap_id,
        )
        self.hypotheses[h1.hypothesis_id] = h1

    def detect_knowledge_gap(
        self,
        domain: str,
        description: str,
        priority: Any = ResearchPriority.HIGH,
        impact_score: float = 0.75,
    ) -> KnowledgeGap:
        if isinstance(priority, int):
            p_map = {1: ResearchPriority.LOW, 2: ResearchPriority.MEDIUM, 3: ResearchPriority.HIGH}
            priority = p_map.get(priority, ResearchPriority.HIGH)
        elif isinstance(priority, str):
            try:
                priority = ResearchPriority(priority)
            except Exception:
                priority = ResearchPriority.HIGH

        gap_id = f"gap_{uuid.uuid4().hex[:8]}"
        gap = KnowledgeGap(
            gap_id=gap_id,
            domain=domain,
            description=description,
            priority=priority,
            impact_score=impact_score,
        )
        self.knowledge_gaps[gap_id] = gap

        self.event_bus.publish(
            ScientificDomainEvent(
                event_type=ScientificEventType.KNOWLEDGE_GAP_DETECTED,
                payload=gap.to_dict(),
            )
        )
        return gap

    def formulate_hypothesis(
        self,
        title: str,
        statement: str,
        domain: str,
        rationale: str,
        prior_probability: float = 0.50,
        expected_information_gain: float = 0.50,
        tags: Optional[List[str]] = None,
        knowledge_gap_id: Optional[str] = None,
        priority: ResearchPriority = ResearchPriority.HIGH,
    ) -> ScientificHypothesis:
        p = max(0.01, min(0.99, prior_probability))
        entropy = -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
        eig = max(expected_information_gain, entropy * 0.9)

        hypo_id = f"hypo_{uuid.uuid4().hex[:8]}"
        hypo = ScientificHypothesis(
            hypothesis_id=hypo_id,
            title=title,
            statement=statement,
            domain=domain,
            rationale=rationale,
            prior_probability=prior_probability,
            expected_information_gain=eig,
            tags=tags or [],
            knowledge_gap_id=knowledge_gap_id,
            priority=priority,
            status=HypothesisStatus.PROPOSED,
        )
        self.hypotheses[hypo_id] = hypo

        self.event_bus.publish(
            ScientificHypothesisCreated(
                hypothesis_id=hypo_id,
                statement=statement,
                expected_information_gain=eig,
                priority=priority,
            )
        )
        return hypo

    def generate_hypothesis(self, **kwargs: Any) -> ScientificHypothesis:
        """Alias for formulate_hypothesis."""
        title = kwargs.get("title", "Generated Hypothesis")
        statement = kwargs.get("statement", "")
        domain = kwargs.get("domain", "general")
        rationale = kwargs.get("rationale", kwargs.get("premise", ""))
        prior = kwargs.get("prior_probability", 0.5)
        eig = kwargs.get("expected_information_gain", 0.5)
        return self.formulate_hypothesis(
            title=title,
            statement=statement,
            domain=domain,
            rationale=rationale,
            prior_probability=prior,
            expected_information_gain=eig,
        )

    def update_prior(self, hypothesis_id: str, new_prior: float) -> ScientificHypothesis:
        hypo = self.hypotheses.get(hypothesis_id)
        if not hypo:
            raise ValueError(f"Hypothesis {hypothesis_id} not found")
        hypo.prior_probability = max(0.0, min(1.0, new_prior))
        hypo.updated_at = datetime.now(timezone.utc)
        self.event_bus.publish(
            ScientificDomainEvent(
                event_type=ScientificEventType.HYPOTHESIS_UPDATED,
                payload={"hypothesis_id": hypothesis_id, "prior_probability": hypo.prior_probability},
            )
        )
        return hypo

    def confirm_hypothesis(self, hypothesis_id: str) -> ScientificHypothesis:
        hypo = self.hypotheses.get(hypothesis_id)
        if not hypo:
            raise ValueError(f"Hypothesis {hypothesis_id} not found")
        hypo.status = HypothesisStatus.CONFIRMED
        hypo.prior_probability = max(hypo.prior_probability, 0.95)
        hypo.updated_at = datetime.now(timezone.utc)
        self.event_bus.publish(
            ScientificDomainEvent(
                event_type=ScientificEventType.HYPOTHESIS_CONFIRMED,
                payload={"hypothesis_id": hypothesis_id, "status": "CONFIRMED"},
            )
        )
        return hypo

    def falsify_hypothesis(self, hypothesis_id: str, reason: str = "") -> ScientificHypothesis:
        hypo = self.hypotheses.get(hypothesis_id)
        if not hypo:
            raise ValueError(f"Hypothesis {hypothesis_id} not found")
        hypo.status = HypothesisStatus.FALSIFIED
        hypo.updated_at = datetime.now(timezone.utc)
        self.event_bus.publish(
            ScientificHypothesisRejected(
                hypothesis_id=hypothesis_id,
                falsification_reason=reason,
            )
        )
        return hypo

    def retire_hypothesis(self, hypothesis_id: str, reason: str = "Retired due to obsolescence") -> ScientificHypothesis:
        hypo = self.hypotheses.get(hypothesis_id)
        if not hypo:
            raise ValueError(f"Hypothesis {hypothesis_id} not found")
        hypo.status = HypothesisStatus.RETIRED
        hypo.updated_at = datetime.now(timezone.utc)
        self.event_bus.publish(
            HypothesisRetired(
                hypothesis_id=hypothesis_id,
                retirement_reason=reason,
            )
        )
        return hypo

    def get_hypothesis(self, hypothesis_id: str) -> Optional[ScientificHypothesis]:
        return self.hypotheses.get(hypothesis_id)

    def list_hypotheses(
        self,
        domain: Optional[str] = None,
        status: Optional[Any] = None,
    ) -> List[ScientificHypothesis]:
        res = list(self.hypotheses.values())
        if domain:
            res = [h for h in res if h.domain.lower() == domain.lower()]
        if status:
            s_val = status.value if hasattr(status, "value") else str(status).upper()
            res = [h for h in res if (h.status.value if hasattr(h.status, "value") else str(h.status)) == s_val]
        return res

    def list_knowledge_gaps(self, domain: Optional[str] = None) -> List[KnowledgeGap]:
        res = list(self.knowledge_gaps.values())
        if domain:
            res = [g for g in res if g.domain.lower() == domain.lower()]
        return res
