"""
Scientific Evidence Provenance Engine for Phase 13.12 (ASD-HGCKEP).
Telemetry Normalization, Cryptographic SHA-256 Provenance Hashing, and Lineage Verification.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.science.events.science_events import (
    EmpiricalEvidenceRecorded,
    EvidenceStrength,
    ScienceEventBus,
)


@dataclass
class ScientificEvidence:
    evidence_id: str = field(default_factory=lambda: f"ev_{uuid.uuid4().hex[:8]}")
    hypothesis_id: str = "hypo_seed_01"
    experiment_id: Optional[str] = None
    title: str = "Empirical Evidence Record"
    data_payload: Dict[str, Any] = field(default_factory=dict)
    confidence_score: float = 0.90
    empirical_sample_size: int = 50
    provenance: Dict[str, Any] = field(default_factory=dict)
    sha256_provenance_hash: str = ""
    strength: EvidenceStrength = EvidenceStrength.STATISTICALLY_SIGNIFICANT
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        if not self.sha256_provenance_hash:
            content = f"{self.hypothesis_id}:{self.experiment_id}:{json.dumps(self.data_payload, sort_keys=True)}:{self.confidence_score}"
            self.sha256_provenance_hash = hashlib.sha256(content.encode()).hexdigest()

    @property
    def evidence_hash_sha256(self) -> str:
        return self.sha256_provenance_hash

    @property
    def confidence(self) -> float:
        return self.confidence_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "hypothesis_id": self.hypothesis_id,
            "experiment_id": self.experiment_id,
            "title": self.title,
            "data_payload": self.data_payload,
            "confidence_score": round(self.confidence_score, 4),
            "empirical_sample_size": self.empirical_sample_size,
            "provenance": self.provenance,
            "sha256_provenance_hash": self.sha256_provenance_hash,
            "evidence_hash_sha256": self.evidence_hash_sha256,
            "strength": self.strength.value if hasattr(self.strength, "value") else str(self.strength),
            "created_at": self.created_at.isoformat(),
        }


class EvidenceEngine:
    """
    Empirical Evidence Ingestion & Cryptographic Provenance Engine.
    """

    def __init__(self, event_bus: Optional[ScienceEventBus] = None) -> None:
        self.event_bus = event_bus or ScienceEventBus()
        self.evidence_store: Dict[str, ScientificEvidence] = {}
        self._initialize_bootstrap_evidence()

    def _initialize_bootstrap_evidence(self) -> None:
        ev1 = ScientificEvidence(
            evidence_id="ev_seed_quant_01",
            hypothesis_id="hypo_seed_01",
            experiment_id="exp_seed_01",
            title="Bootstrap Vector Quantization Telemetry",
            data_payload={"recall": 0.991, "vram_reduction": 0.47},
            confidence_score=0.98,
            empirical_sample_size=200,
            strength=EvidenceStrength.EMPIRICAL_DEFINITIVE,
        )
        self.evidence_store[ev1.evidence_id] = ev1

    def record_evidence(
        self,
        hypothesis_id: str,
        experiment_id: Optional[str] = None,
        title: str = "Empirical Telemetry Record",
        data_payload: Optional[Dict[str, Any]] = None,
        confidence_score: float = 0.90,
        empirical_sample_size: int = 50,
        provenance: Optional[Dict[str, Any]] = None,
    ) -> ScientificEvidence:
        strength = EvidenceStrength.STATISTICALLY_SIGNIFICANT
        if confidence_score >= 0.95 and empirical_sample_size >= 50:
            strength = EvidenceStrength.EMPIRICAL_DEFINITIVE
        elif confidence_score < 0.70:
            strength = EvidenceStrength.PRELIMINARY

        ev_id = f"ev_{uuid.uuid4().hex[:8]}"
        payload = data_payload or {}
        prov = provenance or {}

        content = f"{hypothesis_id}:{experiment_id}:{json.dumps(payload, sort_keys=True)}:{confidence_score}"
        h = hashlib.sha256(content.encode()).hexdigest()

        evidence = ScientificEvidence(
            evidence_id=ev_id,
            hypothesis_id=hypothesis_id,
            experiment_id=experiment_id,
            title=title,
            data_payload=payload,
            confidence_score=confidence_score,
            empirical_sample_size=empirical_sample_size,
            provenance=prov,
            sha256_provenance_hash=h,
            strength=strength,
        )
        self.evidence_store[ev_id] = evidence

        self.event_bus.publish(
            EmpiricalEvidenceRecorded(
                evidence_id=ev_id,
                hypothesis_id=hypothesis_id,
                strength=strength,
                provenance_hash=h,
            )
        )
        return evidence

    def verify_evidence_integrity(self, evidence_id: str) -> bool:
        ev = self.evidence_store.get(evidence_id)
        if not ev:
            return False
        content = f"{ev.hypothesis_id}:{ev.experiment_id}:{json.dumps(ev.data_payload, sort_keys=True)}:{ev.confidence_score}"
        computed = hashlib.sha256(content.encode()).hexdigest()
        return computed == ev.sha256_provenance_hash

    def get_evidence(self, evidence_id: str) -> Optional[ScientificEvidence]:
        return self.evidence_store.get(evidence_id)

    def list_evidence(
        self,
        hypothesis_id: Optional[str] = None,
        experiment_id: Optional[str] = None,
    ) -> List[ScientificEvidence]:
        res = list(self.evidence_store.values())
        if hypothesis_id:
            res = [e for e in res if e.hypothesis_id == hypothesis_id]
        if experiment_id:
            res = [e for e in res if e.experiment_id == experiment_id]
        return res
