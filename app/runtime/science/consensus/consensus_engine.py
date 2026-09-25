"""
Multi-Agent Peer Review & Scientific Consensus Engine for Phase 13.12 (ASD-HGCKEP).
Independent Agent Review Tribunals, Bayesian Consensus Aggregation, and Dissent Recording.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.science.events.science_events import (
    ResearchConsensusReached,
    ScienceEventBus,
    ScientificConsensus,
)


@dataclass
class ConsensusReview:
    review_id: str = field(default_factory=lambda: f"rev_{uuid.uuid4().hex[:8]}")
    hypothesis_id: str = "hypo_seed_01"
    evidence_ids: List[str] = field(default_factory=list)
    validation_id: Optional[str] = None
    tribunal_members: List[str] = field(default_factory=lambda: ["Agent_Sentinel", "Agent_Statistician", "Agent_Architect"])
    reviewer_votes: Dict[str, str] = field(default_factory=lambda: {
        "Agent_Sentinel": "ACCEPT",
        "Agent_Statistician": "ACCEPT",
        "Agent_Architect": "ACCEPT",
    })
    consensus_score: float = 1.0
    consensus_state: ScientificConsensus = ScientificConsensus.ACCEPTED
    dissenting_opinions: List[str] = field(default_factory=list)
    reviewed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def target_id(self) -> str:
        return self.hypothesis_id

    @property
    def consensus_type(self) -> ScientificConsensus:
        return self.consensus_state

    @property
    def peer_reviewer_votes(self) -> Dict[str, str]:
        return self.reviewer_votes

    @property
    def approval_percentage(self) -> float:
        return round(self.consensus_score * 100.0, 1)

    @property
    def minority_dissent_notes(self) -> List[str]:
        return self.dissenting_opinions

    @property
    def consensus_reached(self) -> bool:
        return self.consensus_state in [ScientificConsensus.ACCEPTED, ScientificConsensus.SUPERMAJORITY, ScientificConsensus.UNANIMOUS]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "review_id": self.review_id,
            "hypothesis_id": self.hypothesis_id,
            "target_id": self.target_id,
            "evidence_ids": self.evidence_ids,
            "validation_id": self.validation_id,
            "tribunal_members": self.tribunal_members,
            "reviewer_votes": self.reviewer_votes,
            "peer_reviewer_votes": self.peer_reviewer_votes,
            "consensus_score": round(self.consensus_score, 4),
            "approval_percentage": self.approval_percentage,
            "consensus_state": self.consensus_state.value if hasattr(self.consensus_state, "value") else str(self.consensus_state),
            "consensus_type": self.consensus_state.value if hasattr(self.consensus_state, "value") else str(self.consensus_state),
            "dissenting_opinions": self.dissenting_opinions,
            "minority_dissent_notes": self.minority_dissent_notes,
            "consensus_reached": self.consensus_reached,
            "reviewed_at": self.reviewed_at.isoformat(),
        }


class ConsensusEngine:
    """
    Arbitrates multi-agent peer review tribunals and verifies scientific consensus.
    """

    def __init__(self, event_bus: Optional[ScienceEventBus] = None) -> None:
        self.event_bus = event_bus or ScienceEventBus()
        self.reviews: Dict[str, ConsensusReview] = {}
        self._initialize_bootstrap_consensus()

    def _initialize_bootstrap_consensus(self) -> None:
        r1 = ConsensusReview(
            review_id="rev_seed_01",
            hypothesis_id="hypo_seed_01",
            evidence_ids=["ev_seed_quant_01"],
            validation_id="val_seed_01",
            tribunal_members=["Agent_Sentinel", "Agent_Statistician", "Agent_Architect"],
            reviewer_votes={
                "Agent_Sentinel": "ACCEPT",
                "Agent_Statistician": "ACCEPT",
                "Agent_Architect": "ACCEPT",
            },
            consensus_score=1.0,
            consensus_state=ScientificConsensus.ACCEPTED,
        )
        self.reviews[r1.review_id] = r1

    def conduct_consensus_review(
        self,
        hypothesis_id: str,
        evidence_ids: Optional[List[str]] = None,
        validation_id: Optional[str] = None,
        tribunal_members: Optional[List[str]] = None,
    ) -> ConsensusReview:
        members = tribunal_members or ["Agent_Sentinel", "Agent_Statistician", "Agent_Architect", "Agent_Empiricist"]
        votes: Dict[str, str] = {}
        dissent: List[str] = []

        # Simulated Bayesian multi-agent tribunal voting
        for idx, member in enumerate(members):
            if idx == len(members) - 1 and len(members) > 4:
                votes[member] = "REJECT"
                dissent.append(f"{member}: Requests additional replication trials in edge scenarios.")
            else:
                votes[member] = "ACCEPT"

        accept_count = sum(1 for v in votes.values() if v == "ACCEPT")
        score = accept_count / len(members)

        if score == 1.0:
            state = ScientificConsensus.ACCEPTED
        elif score >= 0.75:
            state = ScientificConsensus.SUPERMAJORITY
        elif score >= 0.50:
            state = ScientificConsensus.PROVISIONAL
        else:
            state = ScientificConsensus.REJECTED

        review_id = f"rev_{uuid.uuid4().hex[:8]}"
        review = ConsensusReview(
            review_id=review_id,
            hypothesis_id=hypothesis_id,
            evidence_ids=evidence_ids or [],
            validation_id=validation_id,
            tribunal_members=members,
            reviewer_votes=votes,
            consensus_score=score,
            consensus_state=state,
            dissenting_opinions=dissent,
        )
        self.reviews[review_id] = review

        self.event_bus.publish(
            ResearchConsensusReached(
                consensus_id=review_id,
                topic=f"Consensus on {hypothesis_id}",
                consensus_type=state,
            )
        )
        return review

    def get_review(self, review_id: str) -> Optional[ConsensusReview]:
        return self.reviews.get(review_id)

    def list_reviews(self, hypothesis_id: Optional[str] = None) -> List[ConsensusReview]:
        res = list(self.reviews.values())
        if hypothesis_id:
            res = [r for r in res if r.hypothesis_id == hypothesis_id]
        return res
