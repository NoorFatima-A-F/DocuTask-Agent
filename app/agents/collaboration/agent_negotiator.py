"""Agent Negotiation Protocol for Multi-Agent Collaboration.

Implements contract-net style negotiation where agents can delegate, bid,
and reach consensus on task assignment based on SLA, cost, and load capacity.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

from app.agents.collaboration.agent_registry import AgentRegistry

logger = logging.getLogger(__name__)


class NegotiationStatus(str, Enum):
    OPEN = "OPEN"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


@dataclass
class TaskBid:
    """A proposal submitted by an agent for executing a delegated task."""

    bid_id: str = field(default_factory=lambda: f"bid_{uuid.uuid4().hex[:8]}")
    agent_id: str = ""
    cost_bid: float = 0.0
    estimated_latency_ms: float = 0.0
    confidence_bid: float = 0.9
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class NegotiationSession:
    """Tracks a negotiation lifecycle for task delegation."""

    session_id: str = field(default_factory=lambda: f"neg_{uuid.uuid4().hex[:8]}")
    originating_agent_id: str = ""
    task_id: str = ""
    required_capability: str = ""
    max_budget: float = 1.0
    deadline_ms: float = 5000.0
    bids: List[TaskBid] = field(default_factory=list)
    status: NegotiationStatus = NegotiationStatus.OPEN
    awarded_agent_id: Optional[str] = None


class AgentNegotiator:
    """Coordinates negotiation rounds among candidate agents."""

    def __init__(self, registry: AgentRegistry) -> None:
        self.registry = registry
        self._sessions: Dict[str, NegotiationSession] = {}

    def initiate_negotiation(
        self,
        originating_agent_id: str,
        task_id: str,
        required_capability: str,
        max_budget: float = 0.05,
        deadline_ms: float = 1000.0,
    ) -> NegotiationSession:
        """Create a new negotiation session and collect bids from eligible agents."""
        session = NegotiationSession(
            originating_agent_id=originating_agent_id,
            task_id=task_id,
            required_capability=required_capability,
            max_budget=max_budget,
            deadline_ms=deadline_ms,
        )
        self._sessions[session.session_id] = session

        # Solicit bids from all capable agents except originating agent
        candidates = self.registry.find_by_capability(required_capability)
        for cand in candidates:
            if cand.agent_id == originating_agent_id:
                continue
            if cand.can_accept_task():
                # Formulate bid
                bid = TaskBid(
                    agent_id=cand.agent_id,
                    cost_bid=cand.cost_per_call,
                    estimated_latency_ms=cand.latency_p95_ms,
                    confidence_bid=cand.confidence_rating,
                )
                session.bids.append(bid)

        return session

    def evaluate_and_award(self, session_id: str) -> Optional[str]:
        """Evaluate received bids and award task delegation to the winning agent."""
        session = self._sessions.get(session_id)
        if not session or not session.bids:
            if session:
                session.status = NegotiationStatus.REJECTED
            return None

        # Filter out bids exceeding budget or deadline
        valid_bids = [
            b for b in session.bids
            if b.cost_bid <= session.max_budget and b.estimated_latency_ms <= session.deadline_ms
        ]
        if not valid_bids:
            # Fallback to any bid if relaxed
            valid_bids = session.bids

        # Utility = 0.5 * Confidence - 0.3 * Cost - 0.2 * Latency (normalized)
        def utility(bid: TaskBid) -> float:
            u_conf = bid.confidence_bid * 50.0
            u_cost = max(0.0, 30.0 - (bid.cost_bid * 1000.0))
            u_lat = max(0.0, 20.0 - (bid.estimated_latency_ms / 50.0))
            return u_conf + u_cost + u_lat

        winning_bid = max(valid_bids, key=utility)
        session.awarded_agent_id = winning_bid.agent_id
        session.status = NegotiationStatus.ACCEPTED

        logger.info(
            "Negotiation %s: Awarded task %s to agent %s (Utility score winner)",
            session_id,
            session.task_id,
            winning_bid.agent_id,
        )
        return winning_bid.agent_id

    def get_session(self, session_id: str) -> Optional[NegotiationSession]:
        return self._sessions.get(session_id)
