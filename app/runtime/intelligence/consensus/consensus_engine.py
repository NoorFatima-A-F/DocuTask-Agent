"""
Consensus Intelligence Engine for Phase 10 (AISLCOP).

Provides evidence-weighted multi-agent consensus computation, disagreement graphing,
and mathematically grounded decision synthesis.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AgentContribution:
    agent_id: str
    department: str
    confidence: float  # [0.0, 1.0]
    recommendation: str  # e.g., "APPROVE", "REJECT", "REROUTE_HIGH_PRECISION"
    risk_score: float  # [0.0, 1.0]
    supporting_evidence_hashes: List[str] = field(default_factory=list)
    rationale: str = ""
    weight_multiplier: float = 1.0


@dataclass
class DisagreementEdge:
    agent_a: str
    agent_b: str
    delta_confidence: float
    conflict_reason: str


@dataclass
class ConsensusResult:
    consensus_id: str
    timestamp: float = field(default_factory=time.time)
    winning_recommendation: str = ""
    agreement_score: float = 0.0  # [0.0, 1.0]
    composite_confidence: float = 0.0
    dominant_evidence_hash: str = ""
    conflict_explanation: str = ""
    final_justification: str = ""
    contributions: List[AgentContribution] = field(default_factory=list)
    disagreements: List[DisagreementEdge] = field(default_factory=list)
    consensus_hash: str = ""

    def __post_init__(self):
        if not self.consensus_hash:
            self.consensus_hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = {
            "consensus_id": self.consensus_id,
            "winning_recommendation": self.winning_recommendation,
            "agreement_score": self.agreement_score,
            "composite_confidence": self.composite_confidence,
            "dominant_evidence_hash": self.dominant_evidence_hash,
            "timestamp": self.timestamp,
        }
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ConsensusEngine:
    """
    Computes evidence-weighted consensus across multi-agent deliberations.
    """

    def evaluate_consensus(
        self,
        contributions: List[AgentContribution],
        consensus_id: Optional[str] = None,
    ) -> ConsensusResult:
        if not contributions:
            return ConsensusResult(
                consensus_id=consensus_id or f"cons_{int(time.time())}",
                winning_recommendation="NONE",
                agreement_score=0.0,
                composite_confidence=0.0,
                final_justification="No agent contributions submitted.",
            )

        cid = consensus_id or f"cons_{int(time.time())}"
        
        # Weighted evidence aggregation by recommendation option
        rec_scores: Dict[str, float] = {}
        rec_weights: Dict[str, float] = {}
        evidence_votes: Dict[str, float] = {}

        for c in contributions:
            # Effective weight = confidence * (1.0 - 0.5 * risk_score) * weight_multiplier * (1 + 0.2 * len(evidence))
            evidence_boost = 1.0 + 0.2 * min(len(c.supporting_evidence_hashes), 3)
            effective_weight = c.confidence * (1.0 - 0.4 * c.risk_score) * c.weight_multiplier * evidence_boost
            
            rec = c.recommendation.upper()
            rec_scores[rec] = rec_scores.get(rec, 0.0) + (effective_weight * c.confidence)
            rec_weights[rec] = rec_weights.get(rec, 0.0) + effective_weight

            for ev in c.supporting_evidence_hashes:
                evidence_votes[ev] = evidence_votes.get(ev, 0.0) + effective_weight

        # Determine winning recommendation
        winning_rec = max(rec_scores.keys(), key=lambda k: rec_scores[k])
        total_weight = sum(rec_weights.values())
        winning_weight = rec_weights[winning_rec]

        # Agreement score: fraction of total weight backing winner
        agreement_score = round(winning_weight / max(total_weight, 1e-9), 4)
        
        # Composite confidence: weighted mean confidence for winning option
        composite_conf = round(rec_scores[winning_rec] / max(winning_weight, 1e-9), 4)

        # Dominant evidence hash
        dominant_evidence = max(evidence_votes.keys(), key=lambda k: evidence_votes[k]) if evidence_votes else ""

        # Compute disagreement graph
        disagreements: List[DisagreementEdge] = []
        n = len(contributions)
        for i in range(n):
            for j in range(i + 1, n):
                a1 = contributions[i]
                a2 = contributions[j]
                if a1.recommendation.upper() != a2.recommendation.upper():
                    disagreements.append(
                        DisagreementEdge(
                            agent_a=a1.agent_id,
                            agent_b=a2.agent_id,
                            delta_confidence=round(abs(a1.confidence - a2.confidence), 4),
                            conflict_reason=f"{a1.agent_id} recommended {a1.recommendation} while {a2.agent_id} recommended {a2.recommendation}.",
                        )
                    )

        conflict_explanation = (
            f"Detected {len(disagreements)} recommendation conflicts resolved via evidence-weighted scoring."
            if disagreements
            else "Full alignment across participating agents."
        )

        final_justification = (
            f"Recommendation '{winning_rec}' selected with agreement score {agreement_score:.2f} "
            f"and composite confidence {composite_conf:.2f} supported by dominant evidence hash {dominant_evidence[:12]}..."
        )

        return ConsensusResult(
            consensus_id=cid,
            timestamp=time.time(),
            winning_recommendation=winning_rec,
            agreement_score=agreement_score,
            composite_confidence=composite_conf,
            dominant_evidence_hash=dominant_evidence,
            conflict_explanation=conflict_explanation,
            final_justification=final_justification,
            contributions=contributions,
            disagreements=disagreements,
        )
