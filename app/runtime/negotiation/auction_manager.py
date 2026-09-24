"""
AMAEOP Pillar 3 - Vickrey Auction Manager
Implements second-price sealed-bid auctions for scarce shared compute (GPU acceleration, LLM high-rate quota, memory slots).
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict, field
import time
import uuid


@dataclass
class AuctionBid:
    bidder_department_id: str
    bid_amount_credits: float
    requested_units: int
    utility_weight: float
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AuctionResult:
    auction_id: str
    resource_type: str  # GPU_OCR_SLOT | GEMINI_PRO_QUOTA | HIGH_SPEED_VECTOR_INDEX
    total_units_available: int
    winning_department_id: str
    winning_bid_amount: float
    clearing_price_credits: float  # Second price in Vickrey auction
    bids: List[AuctionBid]
    settled_at: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class VickreyAuctionManager:
    """Executes second-price sealed-bid auctions ensuring truthful bidding and Pareto optimal resource distribution."""

    def __init__(self):
        self.auction_history: List[AuctionResult] = []
        self._seed_auctions()

    def _seed_auctions(self):
        bids1 = [
            AuctionBid("dept_extraction", 85.0, 4, 0.95),
            AuctionBid("dept_ocr", 62.0, 4, 0.80),
            AuctionBid("dept_research", 45.0, 4, 0.65),
        ]
        # In Vickrey auction: winner is dept_extraction (bid 85.0), pays second price (62.0)
        res1 = AuctionResult(
            auction_id="auc_gpu_2026_01",
            resource_type="GPU_OCR_SLOT",
            total_units_available=4,
            winning_department_id="dept_extraction",
            winning_bid_amount=85.0,
            clearing_price_credits=62.0,
            bids=bids1,
            settled_at=time.time() - 30.0,
        )
        self.auction_history.append(res1)

    def run_auction(
        self,
        resource_type: str,
        units_available: int,
        bids: List[AuctionBid],
    ) -> AuctionResult:
        if not bids:
            raise ValueError("Cannot run auction with zero bids.")

        # Sort descending by bid amount
        sorted_bids = sorted(bids, key=lambda b: b.bid_amount_credits, reverse=True)
        winner = sorted_bids[0]
        # Second price (or winner's price if only 1 bidder)
        second_price = sorted_bids[1].bid_amount_credits if len(sorted_bids) > 1 else winner.bid_amount_credits

        auction_id = f"auc_{uuid.uuid4().hex[:6]}"
        result = AuctionResult(
            auction_id=auction_id,
            resource_type=resource_type,
            total_units_available=units_available,
            winning_department_id=winner.bidder_department_id,
            winning_bid_amount=winner.bid_amount_credits,
            clearing_price_credits=round(second_price, 2),
            bids=sorted_bids,
            settled_at=time.time(),
        )
        self.auction_history.insert(0, result)
        return result

    def list_auction_history(self) -> List[Dict[str, Any]]:
        return [a.to_dict() for a in self.auction_history]


vickrey_auction_manager = VickreyAuctionManager()
