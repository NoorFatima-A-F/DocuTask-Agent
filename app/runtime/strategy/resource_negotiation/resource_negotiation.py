"""
Resource Negotiation Engine for Phase 13.11 (ASC-GEEIP).
Multi-Swarm Resource Auction and Nash Bargaining Protocols for GPU, Tokens, and Worker Slots.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import math
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.strategy.events.strategy_events import (
    NegotiationStatus,
    ResourceNegotiationCompleted,
)


@dataclass
class NegotiationProposal:
    proposal_id: str = field(default_factory=lambda: f"prop-{uuid.uuid4().hex[:6]}")
    swarm_id: str = "swarm-extraction-alpha"
    resource_type: str = "GPU_VRAM_GB"  # "GPU_VRAM_GB" | "TOKEN_BUDGET_K" | "WORKER_SLOTS" | "CPU_CORES"
    quantity_requested: float = 16.0
    quantity_allocated: float = 16.0
    bid_utility: float = 0.92
    disagreement_point: float = 0.20
    concession_rate: float = 0.05
    status: NegotiationStatus = NegotiationStatus.PROPOSED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "swarm_id": self.swarm_id,
            "resource_type": self.resource_type,
            "quantity_requested": self.quantity_requested,
            "quantity_allocated": self.quantity_allocated,
            "bid_utility": round(self.bid_utility, 4),
            "disagreement_point": self.disagreement_point,
            "concession_rate": self.concession_rate,
            "status": self.status.value if hasattr(self.status, "value") else str(self.status),
        }


@dataclass
class NegotiationSession:
    session_id: str = field(default_factory=lambda: f"neg-{uuid.uuid4().hex[:8]}")
    resource_type: str = "GPU_VRAM_GB"
    total_capacity: float = 48.0
    proposals: List[NegotiationProposal] = field(default_factory=list)
    converged: bool = True
    nash_product: float = 0.742
    rounds: int = 3
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "resource_type": self.resource_type,
            "total_capacity": self.total_capacity,
            "total_requested": sum(p.quantity_requested for p in self.proposals),
            "total_allocated": sum(p.quantity_allocated for p in self.proposals),
            "proposals": [p.to_dict() for p in self.proposals],
            "converged": self.converged,
            "nash_product": round(self.nash_product, 4),
            "rounds": self.rounds,
            "created_at": self.created_at,
        }


class ResourceNegotiationEngine:
    """
    Simulates and resolves multi-swarm resource auctions using Nash Bargaining heuristics.
    """

    def __init__(self) -> None:
        self.sessions: Dict[str, NegotiationSession] = {}
        self.event_log: List[Any] = []
        self._initialize_bootstrap_negotiations()

    def _initialize_bootstrap_negotiations(self) -> None:
        # Session 1: GPU VRAM Allocation
        s1 = NegotiationSession(
            session_id="neg-gpu-vram-01",
            resource_type="GPU_VRAM_GB",
            total_capacity=48.0,
            rounds=4,
            converged=True,
            nash_product=0.815,
        )
        p1 = NegotiationProposal(
            proposal_id="prop-gpu-01",
            swarm_id="swarm-alpha-extraction",
            resource_type="GPU_VRAM_GB",
            quantity_requested=24.0,
            quantity_allocated=20.0,
            bid_utility=0.94,
            disagreement_point=0.25,
            concession_rate=0.04,
            status=NegotiationStatus.SETTLED,
        )
        p2 = NegotiationProposal(
            proposal_id="prop-gpu-02",
            swarm_id="swarm-beta-classifier",
            resource_type="GPU_VRAM_GB",
            quantity_requested=16.0,
            quantity_allocated=14.0,
            bid_utility=0.88,
            disagreement_point=0.20,
            concession_rate=0.05,
            status=NegotiationStatus.SETTLED,
        )
        p3 = NegotiationProposal(
            proposal_id="prop-gpu-03",
            swarm_id="swarm-gamma-governance",
            resource_type="GPU_VRAM_GB",
            quantity_requested=16.0,
            quantity_allocated=14.0,
            bid_utility=0.91,
            disagreement_point=0.30,
            concession_rate=0.03,
            status=NegotiationStatus.SETTLED,
        )
        s1.proposals = [p1, p2, p3]
        self.sessions[s1.session_id] = s1

        # Session 2: Token Budget Pool
        s2 = NegotiationSession(
            session_id="neg-tokens-pool-02",
            resource_type="TOKEN_BUDGET_K",
            total_capacity=5000.0,
            rounds=2,
            converged=True,
            nash_product=0.892,
        )
        s2.proposals = [
            NegotiationProposal(
                proposal_id="prop-tok-01",
                swarm_id="swarm-alpha-extraction",
                resource_type="TOKEN_BUDGET_K",
                quantity_requested=3000.0,
                quantity_allocated=2800.0,
                bid_utility=0.95,
                status=NegotiationStatus.SETTLED,
            ),
            NegotiationProposal(
                proposal_id="prop-tok-02",
                swarm_id="swarm-delta-reasoning",
                resource_type="TOKEN_BUDGET_K",
                quantity_requested=2500.0,
                quantity_allocated=2200.0,
                bid_utility=0.89,
                status=NegotiationStatus.SETTLED,
            ),
        ]
        self.sessions[s2.session_id] = s2

    def negotiate_resources(
        self,
        resource_type: str,
        total_capacity: float,
        proposals_data: List[Dict[str, Any]],
        max_rounds: int = 5,
    ) -> NegotiationSession:
        proposals: List[NegotiationProposal] = []
        for p in proposals_data:
            prop = NegotiationProposal(
                swarm_id=p.get("swarm_id", "swarm-generic"),
                resource_type=resource_type,
                quantity_requested=float(p.get("quantity_requested", 10.0)),
                bid_utility=float(p.get("bid_utility", 0.8)),
                disagreement_point=float(p.get("disagreement_point", 0.2)),
                concession_rate=float(p.get("concession_rate", 0.05)),
            )
            proposals.append(prop)

        # Proportional-fairness Nash bargaining allocation
        total_requested = sum(p.quantity_requested for p in proposals)
        current_round = 1

        if total_requested <= total_capacity:
            for p in proposals:
                p.quantity_allocated = p.quantity_requested
                p.status = NegotiationStatus.SETTLED
        else:
            # Multi-round concession adjustment
            while current_round <= max_rounds:
                scale = total_capacity / sum(p.quantity_requested for p in proposals)
                for p in proposals:
                    effective_utility = max(p.disagreement_point, p.bid_utility * scale)
                    p.quantity_allocated = round(p.quantity_requested * scale, 2)
                    p.bid_utility = effective_utility
                current_round += 1

            for p in proposals:
                p.status = NegotiationStatus.SETTLED

        # Compute Nash product: Product of (u_i - d_i)
        surpluses = [max(0.01, p.bid_utility - p.disagreement_point) for p in proposals]
        nash_product = math.prod(surpluses) ** (1.0 / max(len(surpluses), 1))

        session = NegotiationSession(
            resource_type=resource_type,
            total_capacity=total_capacity,
            proposals=proposals,
            converged=True,
            nash_product=nash_product,
            rounds=current_round,
        )
        self.sessions[session.session_id] = session

        event = ResourceNegotiationCompleted(
            negotiation_id=session.session_id,
            participating_swarms=[p.swarm_id for p in proposals],
            converged=True,
            nash_product=nash_product,
        )
        self.event_log.append(event)
        return session

    def list_sessions(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self.sessions.values()]

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        s = self.sessions.get(session_id)
        return s.to_dict() if s else None
