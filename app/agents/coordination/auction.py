"""
Auction Allocation Engine.
Implements First-Price Reverse Auctions and Vickrey-style second-price auctions for agent resource allocation.
"""

from typing import List, Optional
from uuid import UUID
from app.agents.coordination.negotiation import Bid, NegotiationSession


class AuctionEngine:
    """Executes auctions for allocating tasks to lowest-cost / highest-efficiency bidders."""

    def run_first_price_reverse_auction(self, session: NegotiationSession) -> Optional[Bid]:
        """Winning agent is the lowest proposed price; paid their bid price."""
        if not session.bids:
            return None
        return min(session.bids, key=lambda b: (b.proposed_cost_usd, b.estimated_duration_ms))

    def run_vickrey_reverse_auction(self, session: NegotiationSession) -> Optional[Bid]:
        """Lowest bidder wins, but paid the second-lowest bidder's price."""
        if not session.bids:
            return None
        if len(session.bids) == 1:
            return session.bids[0]

        sorted_bids = sorted(session.bids, key=lambda b: b.proposed_cost_usd)
        winner = sorted_bids[0]
        # In a real payment ledger, winner receives sorted_bids[1].proposed_cost_usd
        return winner
