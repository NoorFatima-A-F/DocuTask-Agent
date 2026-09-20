"""
Negotiation Domain Models.
Defines models for bids, offers, counter-offers, and negotiation sessions.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class Bid(BaseModel):
    """Bid submitted by an agent for a task."""
    bid_id: UUID = Field(default_factory=uuid4)
    bidder_agent_id: UUID
    task_id: str
    proposed_cost_usd: float = Field(ge=0.0)
    estimated_duration_ms: float = Field(ge=0.0)
    confidence_score: float = Field(default=0.9, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {"frozen": True}


class NegotiationSession(BaseModel):
    """Negotiation interaction between coordinator and candidate agents."""
    negotiation_id: UUID = Field(default_factory=uuid4)
    task_id: str
    initiator_id: UUID
    bids: List[Bid] = Field(default_factory=list)
    winning_bid: Optional[Bid] = None
    is_closed: bool = False

    def submit_bid(self, bid: Bid) -> "NegotiationSession":
        """Submits a new bid to the session."""
        return self.model_copy(update={"bids": [*self.bids, bid]})

    def award(self, winning_bid: Bid) -> "NegotiationSession":
        """Closes negotiation and selects winning bid."""
        return self.model_copy(update={
            "winning_bid": winning_bid,
            "is_closed": True
        })
