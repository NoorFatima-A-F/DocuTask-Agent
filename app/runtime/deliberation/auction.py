"""Vickrey Second-Price Auction Mechanism for DocuTask ACOS.

Enforces incentive-compatible, truthful bidding for allocating specialized worker nodes to tasks.
The winning agent receives the allocation at the price bid by the second-highest bidder.
"""

from __future__ import annotations

import uuid
from typing import List
from pydantic import BaseModel, Field


class WorkerTaskBid(BaseModel):
    bidder_agent_id: str
    task_id: str
    bid_amount_credits: float
    urgency_multiplier: float = 1.0


class AuctionAllocationResult(BaseModel):
    auction_id: str = Field(default_factory=lambda: f"auc_{uuid.uuid4().hex[:8]}")
    task_id: str
    winning_agent_id: str
    clearing_price_credits: float
    all_bids: List[WorkerTaskBid] = Field(default_factory=list)
    mechanism: str = "VICKREY_SECOND_PRICE_TRUTHFUL"


class VickreyTaskAuctioneer:
    """Executes truthful Vickrey auctions to allocate scarce worker resources."""

    def conduct_task_auction(self, task_id: str, bids: List[WorkerTaskBid]) -> AuctionAllocationResult:
        if not bids:
            return AuctionAllocationResult(
                task_id=task_id,
                winning_agent_id="SYSTEM_DEFAULT",
                clearing_price_credits=0.0,
                all_bids=[],
            )

        # Sort bids descending by bid amount
        sorted_bids = sorted(bids, key=lambda b: b.bid_amount_credits * b.urgency_multiplier, reverse=True)
        winner = sorted_bids[0]

        # Second price clearing (or reserve price if single bidder)
        second_price = (
            (sorted_bids[1].bid_amount_credits * sorted_bids[1].urgency_multiplier)
            if len(sorted_bids) > 1
            else (winner.bid_amount_credits * 0.8)
        )

        return AuctionAllocationResult(
            task_id=task_id,
            winning_agent_id=winner.bidder_agent_id,
            clearing_price_credits=round(second_price, 4),
            all_bids=sorted_bids,
        )
