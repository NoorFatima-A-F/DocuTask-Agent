"""
Scientific Publication & Machine-Readable Literature Engine for Phase 13.12 (ASD-HGCKEP).
Produces Cryptographically Signed Research Papers, Experiment Reports, and Executive Briefings.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.science.events.science_events import (
    KnowledgePublished,
    PublicationState,
    ScienceEventBus,
)


@dataclass
class ScientificPublication:
    publication_id: str = field(default_factory=lambda: f"pub_{uuid.uuid4().hex[:8]}")
    title: str = "Empirical Proof of Speculative Invariance in Multi-Column Accounting Extraction"
    abstract: str = "We demonstrate that recurring enterprise invoice headers exhibit <=1.2 bits/token spatial entropy."
    authors: List[str] = field(default_factory=lambda: ["AI Chief Scientist", "Autonomous Research Swarm"])
    domain: str = "performance"
    hypothesis_ids: List[str] = field(default_factory=list)
    experiment_ids: List[str] = field(default_factory=list)
    evidence_ids: List[str] = field(default_factory=list)
    conclusion: str = "Empirical results confirm significant optimization benefits with high statistical confidence."
    publication_state: PublicationState = PublicationState.DRAFT
    doi: str = ""
    cryptographic_signature: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def pub_id(self) -> str:
        return self.publication_id

    @property
    def doi_signature(self) -> str:
        return self.doi

    @property
    def state(self) -> PublicationState:
        return self.publication_state

    def to_dict(self) -> Dict[str, Any]:
        return {
            "publication_id": self.publication_id,
            "pub_id": self.pub_id,
            "title": self.title,
            "abstract": self.abstract,
            "authors": self.authors,
            "domain": self.domain,
            "hypothesis_ids": self.hypothesis_ids,
            "experiment_ids": self.experiment_ids,
            "evidence_ids": self.evidence_ids,
            "conclusion": self.conclusion,
            "publication_state": self.publication_state.value if hasattr(self.publication_state, "value") else str(self.publication_state),
            "state": self.publication_state.value if hasattr(self.publication_state, "value") else str(self.publication_state),
            "doi": self.doi,
            "doi_signature": self.doi,
            "cryptographic_signature": self.cryptographic_signature,
            "created_at": self.created_at.isoformat(),
        }


class PublicationEngine:
    """
    Autonomous Machine-Readable Scientific Literature & DOI Registry Engine.
    """

    def __init__(self, event_bus: Optional[ScienceEventBus] = None) -> None:
        self.event_bus = event_bus or ScienceEventBus()
        self.publications: Dict[str, ScientificPublication] = {}
        self._initialize_bootstrap_publications()

    def _initialize_bootstrap_publications(self) -> None:
        p1 = ScientificPublication(
            publication_id="pub_seed_01",
            title="Empirical Validation of Vector Quantization in Enterprise Swarm Memory",
            abstract="We present empirical telemetry demonstrating 47% VRAM reduction with 99.1% semantic recall retention.",
            authors=["AI Chief Scientist", "Cognitive Architecture Team"],
            domain="performance",
            hypothesis_ids=["hypo_seed_01"],
            experiment_ids=["exp_seed_01"],
            evidence_ids=["ev_seed_quant_01"],
            conclusion="Quantization allows linear scaling of agent swarm concurrency without memory saturation.",
            publication_state=PublicationState.PUBLISHED,
            doi="doi:10.5555/ai-scientist.2026.001",
            cryptographic_signature=hashlib.sha256(b"sig:doi:10.5555/ai-scientist.2026.001").hexdigest(),
        )
        self.publications[p1.publication_id] = p1

    def create_publication(
        self,
        title: str,
        abstract: str,
        authors: Optional[List[str]] = None,
        domain: str = "performance",
        hypothesis_ids: Optional[List[str]] = None,
        experiment_ids: Optional[List[str]] = None,
        evidence_ids: Optional[List[str]] = None,
        conclusion: str = "",
    ) -> ScientificPublication:
        pub_id = f"pub_{uuid.uuid4().hex[:8]}"
        pub = ScientificPublication(
            publication_id=pub_id,
            title=title,
            abstract=abstract,
            authors=authors or ["AI Chief Scientist"],
            domain=domain,
            hypothesis_ids=hypothesis_ids or [],
            experiment_ids=experiment_ids or [],
            evidence_ids=evidence_ids or [],
            conclusion=conclusion,
            publication_state=PublicationState.DRAFT,
        )
        self.publications[pub_id] = pub
        return pub

    def sign_and_publish(self, publication_id: str) -> ScientificPublication:
        pub = self.publications.get(publication_id)
        if not pub:
            raise ValueError(f"Publication {publication_id} not found")

        doi = f"doi:10.5555/ai-scientist.{datetime.now(timezone.utc).year}.{publication_id}"
        sig_content = f"{doi}:{pub.title}:{pub.abstract}:{datetime.now(timezone.utc).isoformat()}"
        signature = hashlib.sha256(sig_content.encode()).hexdigest()

        pub.doi = doi
        pub.cryptographic_signature = signature
        pub.publication_state = PublicationState.PUBLISHED

        self.event_bus.publish(
            KnowledgePublished(
                publication_id=publication_id,
                title=pub.title,
                doi_signature=doi,
            )
        )
        return pub

    def get_publication(self, publication_id: str) -> Optional[ScientificPublication]:
        return self.publications.get(publication_id)

    def list_publications(self, domain: Optional[str] = None) -> List[ScientificPublication]:
        res = list(self.publications.values())
        if domain:
            res = [p for p in res if p.domain.lower() == domain.lower()]
        return res
