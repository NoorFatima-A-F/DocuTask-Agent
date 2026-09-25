"""
Scientific Knowledge & Empirical Laws Engine for Phase 13.12 (ASD-HGCKEP).
Permanent Scientific Knowledge Base, Causal Laws, Verified Facts, and Semantic Versioning.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.science.events.science_events import (
    ScienceEventBus,
    ScientificDomainEvent,
    ScientificEventType,
    ScientificLawFormulated,
)


@dataclass
class ScientificFact:
    fact_id: str = field(default_factory=lambda: f"fact_{uuid.uuid4().hex[:8]}")
    statement: str = "Vector memory quantization down to 8-bit maintains 99.1% semantic recall."
    domain: str = "performance"
    source_evidence_ids: List[str] = field(default_factory=list)
    hypothesis_id: Optional[str] = None
    confidence: float = 0.98
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fact_id": self.fact_id,
            "statement": self.statement,
            "domain": self.domain,
            "source_evidence_ids": self.source_evidence_ids,
            "hypothesis_id": self.hypothesis_id,
            "confidence": round(self.confidence, 4),
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class ScientificLaw:
    law_id: str = field(default_factory=lambda: f"law_{uuid.uuid4().hex[:8]}")
    title: str = "Principle of Swarm Convergence Latency"
    governing_equation: str = "T_convergence = alpha * (N_agents^0.42) / bandwidth"
    domain: str = "performance"
    supporting_fact_ids: List[str] = field(default_factory=list)
    variables: Dict[str, str] = field(default_factory=dict)
    confidence: float = 0.96
    version: str = "1.0.0"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def name(self) -> str:
        return self.title

    def to_dict(self) -> Dict[str, Any]:
        return {
            "law_id": self.law_id,
            "title": self.title,
            "name": self.name,
            "governing_equation": self.governing_equation,
            "domain": self.domain,
            "supporting_fact_ids": self.supporting_fact_ids,
            "variables": self.variables,
            "confidence": round(self.confidence, 4),
            "version": self.version,
            "created_at": self.created_at.isoformat(),
        }


class KnowledgeEngine:
    """
    Permanent Scientific Knowledge Base and Empirical Law Formulation Engine.
    """

    def __init__(self, event_bus: Optional[ScienceEventBus] = None) -> None:
        self.event_bus = event_bus or ScienceEventBus()
        self.facts: Dict[str, ScientificFact] = {}
        self.laws: Dict[str, ScientificLaw] = {}
        self._initialize_bootstrap_knowledge()

    def _initialize_bootstrap_knowledge(self) -> None:
        f1 = ScientificFact(
            fact_id="fact_seed_01",
            statement="Vector memory quantization down to 8-bit maintains 99.1% semantic recall while reducing memory footprint by 47%.",
            domain="performance",
            source_evidence_ids=["ev_seed_quant_01"],
            confidence=0.98,
        )
        self.facts[f1.fact_id] = f1

        l1 = ScientificLaw(
            law_id="law_seed_01",
            title="Principle of Swarm Convergence Latency",
            governing_equation="T_convergence = alpha * (N_agents^0.42) / bandwidth",
            domain="performance",
            supporting_fact_ids=[f1.fact_id],
            variables={"N_agents": "Number of participating agents", "bandwidth": "Inter-agent bus capacity"},
            confidence=0.96,
        )
        self.laws[l1.law_id] = l1

    def record_fact(
        self,
        statement: str,
        domain: str = "general",
        source_evidence_ids: Optional[List[str]] = None,
        hypothesis_id: Optional[str] = None,
        confidence: float = 0.95,
    ) -> ScientificFact:
        fact_id = f"fact_{uuid.uuid4().hex[:8]}"
        fact = ScientificFact(
            fact_id=fact_id,
            statement=statement,
            domain=domain,
            source_evidence_ids=source_evidence_ids or [],
            hypothesis_id=hypothesis_id,
            confidence=confidence,
        )
        self.facts[fact_id] = fact

        self.event_bus.publish(
            ScientificDomainEvent(
                event_type=ScientificEventType.FACT_RECORDED,
                payload=fact.to_dict(),
            )
        )
        return fact

    def formulate_law(
        self,
        title: str,
        governing_equation: str,
        domain: str = "general",
        supporting_fact_ids: Optional[List[str]] = None,
        variables: Optional[Dict[str, str]] = None,
        confidence: float = 0.90,
    ) -> ScientificLaw:
        law_id = f"law_{uuid.uuid4().hex[:8]}"
        law = ScientificLaw(
            law_id=law_id,
            title=title,
            governing_equation=governing_equation,
            domain=domain,
            supporting_fact_ids=supporting_fact_ids or [],
            variables=variables or {},
            confidence=confidence,
        )
        self.laws[law_id] = law

        self.event_bus.publish(
            ScientificLawFormulated(
                law_id=law_id,
                equation_formula=governing_equation,
                domain=domain,
            )
        )
        return law

    def get_fact(self, fact_id: str) -> Optional[ScientificFact]:
        return self.facts.get(fact_id)

    def get_law(self, law_id: str) -> Optional[ScientificLaw]:
        return self.laws.get(law_id)

    def list_facts(self, domain: Optional[str] = None) -> List[ScientificFact]:
        res = list(self.facts.values())
        if domain:
            res = [f for f in res if f.domain.lower() == domain.lower()]
        return res

    def list_laws(self, domain: Optional[str] = None) -> List[ScientificLaw]:
        res = list(self.laws.values())
        if domain:
            res = [l for l in res if l.domain.lower() == domain.lower()]
        return res
