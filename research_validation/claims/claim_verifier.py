"""
Scientific Claim Verification Engine (Phase 76A)
================================================
Parses scientific claims in research reports and validation summaries,
classifies their empirical epistemic status (MEASURED, DERIVED, ESTIMATED,
LITERATURE, SIMULATION, UNKNOWN, UNSUPPORTED), and binds every claim to
underlying Merkle DAG evidence nodes.

Calculates the Claim Groundedness Index (CGI).
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from research_validation.provenance.hashing import hash_canonical_json
from research_validation.provenance.provenance_models import EvidenceNode, EvidenceQualityLevel
from research_validation.provenance.evidence_graph import EvidenceGraph


class ClaimClassification(str, Enum):
    MEASURED = "MEASURED"
    DERIVED = "DERIVED"
    ESTIMATED = "ESTIMATED"
    LITERATURE = "LITERATURE"
    SIMULATION = "SIMULATION"
    UNKNOWN = "UNKNOWN"
    UNSUPPORTED = "UNSUPPORTED"


@dataclass(frozen=True)
class ClaimStatement:
    claim_id: str
    text: str
    classification: ClaimClassification
    backing_evidence_hashes: Tuple[str, ...]
    quality_level: EvidenceQualityLevel
    empirical_confidence: float
    rationale: str
    citations: Tuple[str, ...] = ()


@dataclass(frozen=True)
class ClaimVerificationAudit:
    audit_id: str
    timestamp_utc: str
    total_claims: int
    classification_counts: Dict[str, int]
    claim_groundedness_index: float  # (MEASURED + DERIVED) / Total
    evidence_backed_ratio: float     # Claims with at least one valid Merkle hash / Total
    is_fully_grounded: bool
    claims: Tuple[ClaimStatement, ...]
    unsupported_claims: Tuple[ClaimStatement, ...]
    merkle_claim_root: str


class ScientificClaimVerifier:
    """
    Parses scientific text, extracts empirical assertions, and verifies them
    against the Merkle DAG Evidence Graph.
    """

    # Heuristics for classifying claims when parsing text
    MEASURED_KEYWORDS = {"measured", "observed", "benchmarked", "profiled", "recorded", "telemetry", "hardware clock", "perf_counter"}
    DERIVED_KEYWORDS = {"computed", "calculated", "derived", "wilson ci", "confidence interval", "f1-score", "mean", "median", "p99"}
    ESTIMATED_KEYWORDS = {"estimated", "projected", "extrapolated", "approximated", "expected"}
    LITERATURE_KEYWORDS = {"cited", "according to", "baseline", "prior work", "published by", "et al", "icdar", "cvpr"}
    SIMULATION_KEYWORDS = {"simulated", "synthetic", "chaos injected", "mock", "emulated"}

    def __init__(self, evidence_graph: Optional[EvidenceGraph] = None):
        self.evidence_graph = evidence_graph

    def verify_statement(
        self,
        claim_id: str,
        text: str,
        provided_evidence_nodes: Optional[List[EvidenceNode]] = None,
        explicit_classification: Optional[ClaimClassification] = None,
    ) -> ClaimStatement:
        """Verify an individual claim against available evidence nodes."""
        evidence_nodes = provided_evidence_nodes or []
        if self.evidence_graph and not evidence_nodes:
            # Query graph for matching tags or terms in text
            evidence_nodes = self._find_matching_nodes_in_graph(text)

        # Determine classification
        if explicit_classification is not None:
            classification = explicit_classification
        else:
            classification = self._classify_text(text, evidence_nodes)

        backing_hashes = tuple(n.node_hash for n in evidence_nodes if n.node_hash)

        # Determine quality level and confidence
        if not backing_hashes and classification not in (ClaimClassification.LITERATURE, ClaimClassification.SIMULATION):
            classification = ClaimClassification.UNSUPPORTED

        quality_level = EvidenceQualityLevel.LEVEL_E
        conf = 0.0

        if classification == ClaimClassification.MEASURED:
            quality_level = EvidenceQualityLevel.LEVEL_A if any(n.quality_level == EvidenceQualityLevel.LEVEL_A for n in evidence_nodes) else EvidenceQualityLevel.LEVEL_C
            conf = 0.95
            rationale = f"Claim supported by {len(backing_hashes)} empirical observation node(s)."
        elif classification == ClaimClassification.DERIVED:
            quality_level = EvidenceQualityLevel.LEVEL_B
            conf = 0.90
            rationale = f"Claim mathematically derived from {len(backing_hashes)} evidence node(s)."
        elif classification == ClaimClassification.SIMULATION:
            quality_level = EvidenceQualityLevel.LEVEL_D
            conf = 0.60
            rationale = "Claim supported by synthetic/simulation benchmark."
        elif classification == ClaimClassification.LITERATURE:
            quality_level = EvidenceQualityLevel.LEVEL_B
            conf = 0.80
            rationale = "Claim cites external literature reference."
        elif classification == ClaimClassification.ESTIMATED:
            quality_level = EvidenceQualityLevel.LEVEL_D
            conf = 0.50
            rationale = "Claim represents an extrapolation or estimation."
        elif classification == ClaimClassification.UNSUPPORTED:
            quality_level = EvidenceQualityLevel.LEVEL_E
            conf = 0.0
            rationale = "No backing evidence node or proof found in Merkle provenance graph."
        else:
            quality_level = EvidenceQualityLevel.LEVEL_E
            conf = 0.20
            rationale = "Claim origin could not be definitively verified."

        return ClaimStatement(
            claim_id=claim_id,
            text=text.strip(),
            classification=classification,
            backing_evidence_hashes=backing_hashes,
            quality_level=quality_level,
            empirical_confidence=conf,
            rationale=rationale,
        )

    def audit_document_claims(
        self,
        document_text: str,
        audit_id: Optional[str] = None,
    ) -> ClaimVerificationAudit:
        """Parse document lines/sentences and produce a structured claim verification audit."""
        sentences = self._split_into_sentences(document_text)
        claims: List[ClaimStatement] = []

        for idx, s in enumerate(sentences):
            if not s.strip():
                continue
            cid = f"claim_{idx+1:04d}"
            claims.append(self.verify_statement(cid, s))

        total = len(claims)
        counts: Dict[str, int] = {c.value: 0 for c in ClaimClassification}
        for cl in claims:
            counts[cl.classification.value] += 1

        measured_or_derived = counts[ClaimClassification.MEASURED.value] + counts[ClaimClassification.DERIVED.value]
        cgi = measured_or_derived / total if total > 0 else 0.0
        backed_count = sum(1 for c in claims if c.backing_evidence_hashes)
        backed_ratio = backed_count / total if total > 0 else 0.0

        unsupported = tuple(c for c in claims if c.classification == ClaimClassification.UNSUPPORTED)

        # Merkle claim root
        claim_hashes = [c.backing_evidence_hashes[0] if c.backing_evidence_hashes else c.claim_id for c in claims]
        root_h = hash_canonical_json({"total": total, "cgi": cgi, "claims": claim_hashes})

        return ClaimVerificationAudit(
            audit_id=audit_id or f"audit_claims_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            total_claims=total,
            classification_counts=counts,
            claim_groundedness_index=cgi,
            evidence_backed_ratio=backed_ratio,
            is_fully_grounded=len(unsupported) == 0 and cgi >= 0.70,
            claims=tuple(claims),
            unsupported_claims=unsupported,
            merkle_claim_root=root_h,
        )

    def _classify_text(self, text: str, nodes: List[EvidenceNode]) -> ClaimClassification:
        lower = text.lower()
        if nodes:
            if any("derived" in str(n.stage).lower() for n in nodes):
                return ClaimClassification.DERIVED
            return ClaimClassification.MEASURED

        if any(w in lower for w in self.LITERATURE_KEYWORDS):
            return ClaimClassification.LITERATURE
        if any(w in lower for w in self.SIMULATION_KEYWORDS):
            return ClaimClassification.SIMULATION
        if any(w in lower for w in self.ESTIMATED_KEYWORDS):
            return ClaimClassification.ESTIMATED
        if any(w in lower for w in self.DERIVED_KEYWORDS):
            return ClaimClassification.DERIVED
        if any(w in lower for w in self.MEASURED_KEYWORDS):
            return ClaimClassification.MEASURED
        return ClaimClassification.UNKNOWN

    def _find_matching_nodes_in_graph(self, text: str) -> List[EvidenceNode]:
        if not self.evidence_graph:
            return []
        matches: List[EvidenceNode] = []
        lower = text.lower()
        for node in self.evidence_graph.nodes.values():
            if node.name.lower() in lower or node.stage.value.lower() in lower:
                matches.append(node)
                continue
            tokens = [t.lower() for t in re.split(r'\W+', node.name) if len(t) > 3]
            if any(t in lower for t in tokens):
                matches.append(node)
        return matches



    @staticmethod
    def _split_into_sentences(text: str) -> List[str]:
        # Split on period, newline, or list bullets
        raw_parts = re.split(r'(?:\r?\n|(?<=[.!?])\s+)', text)
        cleaned = [p.strip().lstrip("-*#0123456789. ") for p in raw_parts if p.strip()]
        return [p for p in cleaned if len(p) > 10]
