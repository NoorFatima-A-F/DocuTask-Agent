"""
Contract Net Protocol (CNP) Engine.
Implements the classic FIPA-compliant Contract Net Protocol:
Call For Proposals (CFP) -> Bids -> Evaluation -> Award / Rejection.
"""

from typing import Optional
from uuid import UUID, uuid4
from app.agents.coordination.negotiation import Bid, NegotiationSession


class ContractNetEngine:
    """Orchestrates Contract Net Protocol rounds for competitive agent task allocation."""

    def issue_call_for_proposals(
        self,
        initiator_id: UUID,
        task_id: str
    ) -> NegotiationSession:
        """Issues a new CFP for a task."""
        return NegotiationSession(
            negotiation_id=uuid4(),
            task_id=task_id,
            initiator_id=initiator_id
        )

    def evaluate_proposals(
        self,
        session: NegotiationSession,
        cost_weight: float = 0.5,
        latency_weight: float = 0.3,
        confidence_weight: float = 0.2
    ) -> Optional[Bid]:
        """Evaluates submitted bids and selects the highest scoring proposal."""
        if not session.bids:
            return None

        # Lower cost and latency are better; higher confidence is better.
        def _score_bid(b: Bid) -> float:
            cost_norm = 1.0 / (1.0 + b.proposed_cost_usd)
            lat_norm = 1.0 / (1.0 + (b.estimated_duration_ms / 1000.0))
            return (
                cost_weight * cost_norm
                + latency_weight * lat_norm
                + confidence_weight * b.confidence_score
            )

        best_bid = max(session.bids, key=_score_bid)
        return best_bid
