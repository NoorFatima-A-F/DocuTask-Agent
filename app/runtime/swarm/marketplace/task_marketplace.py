"""
AMCN-SIP Phase 13.8 - Task Marketplace & Auctioning
Decentralized task auctions, agent bidding, Pareto-optimal bid evaluation, and award contract settlement.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union
import uuid


class AuctionType(str, Enum):
    FIRST_PRICE = "FIRST_PRICE"
    FIRST_PRICE_SEALED = "FIRST_PRICE_SEALED"
    SECOND_PRICE_VICKREY = "SECOND_PRICE_VICKREY"
    DUTCH = "DUTCH"
    REVERSE = "REVERSE"
    WEIGHTED_UTILITY = "WEIGHTED_UTILITY"


@dataclass
class MarketplaceTask:
    task_id: str
    auction_id: str = ""
    title: str = ""
    name: str = ""
    description: str = ""
    required_capability: str = ""
    required_skills: List[str] = field(default_factory=list)
    budget_cap_usd: float = 100.0
    max_budget: float = 100.0
    deadline_ms: float = 5000.0
    deadline_sec: float = 5.0
    auction_type: AuctionType = AuctionType.WEIGHTED_UTILITY
    status: str = "OPEN"  # OPEN, BIDDING_CLOSED, AWARDED, CANCELLED
    published_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.auction_id:
            self.auction_id = self.task_id
        if not self.task_id and self.auction_id:
            self.task_id = self.auction_id
        if not self.title and self.name:
            self.title = self.name
        if not self.name and self.title:
            self.name = self.title
        if not self.required_capability and self.required_skills:
            self.required_capability = self.required_skills[0]
        if not self.required_skills and self.required_capability:
            self.required_skills = [self.required_capability]
        if self.budget_cap_usd == 100.0 and self.max_budget != 100.0:
            self.budget_cap_usd = self.max_budget
        if self.max_budget == 100.0 and self.budget_cap_usd != 100.0:
            self.max_budget = self.budget_cap_usd


@dataclass
class AgentBid:
    bid_id: str
    auction_id: str = ""
    bidder_agent_id: str = ""
    bid_cost: float = 0.0
    estimated_latency_ms: float = 0.0
    reputation_score: float = 0.95
    proposed_sla: str = "Standard 99.9%"
    task_id: str = ""
    bid_cost_usd: float = 0.0
    bid_latency_ms: float = 0.0
    bid_confidence: float = 0.95
    utility_score: float = 0.0
    status: str = "SUBMITTED"  # SUBMITTED, ACCEPTED, REJECTED
    submitted_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self):
        if not self.task_id and self.auction_id:
            self.task_id = self.auction_id
        if not self.auction_id and self.task_id:
            self.auction_id = self.task_id
        if self.bid_cost_usd == 0.0 and self.bid_cost != 0.0:
            self.bid_cost_usd = self.bid_cost
        if self.bid_cost == 0.0 and self.bid_cost_usd != 0.0:
            self.bid_cost = self.bid_cost_usd
        if self.bid_latency_ms == 0.0 and self.estimated_latency_ms != 0.0:
            self.bid_latency_ms = self.estimated_latency_ms
        if self.estimated_latency_ms == 0.0 and self.bid_latency_ms != 0.0:
            self.estimated_latency_ms = self.bid_latency_ms
        if self.bid_confidence == 0.95 and self.reputation_score != 0.95:
            self.bid_confidence = self.reputation_score
        if self.estimated_latency_ms == 0.0 and self.bid_latency_ms != 0.0:
            self.estimated_latency_ms = self.bid_latency_ms


class BidEvaluator:
    """
    Computes scalarized multi-objective utility scores for agent bids.
    """

    def score_bid(self, bid: AgentBid, budget_cap: float, deadline_ms: float) -> float:
        cost = bid.bid_cost_usd or bid.bid_cost
        lat = bid.bid_latency_ms or bid.estimated_latency_ms
        conf = bid.bid_confidence or bid.reputation_score

        cost_score = max(0.0, 1.0 - (cost / (budget_cap if budget_cap > 0 else 100.0)))
        latency_score = max(0.0, 1.0 - (lat / (deadline_ms if deadline_ms > 0 else 5000.0)))
        confidence_score = conf

        utility = (cost_score * 0.35) + (latency_score * 0.30) + (confidence_score * 0.35)
        return round(utility, 4)


class TaskAuction:
    """
    Settles task awards based on auction mechanics.
    """

    def __init__(self, evaluator: BidEvaluator):
        self.evaluator = evaluator

    def resolve_auction(self, task: MarketplaceTask, bids: List[AgentBid]) -> Optional[AgentBid]:
        if not bids:
            return None

        cap = task.budget_cap_usd or task.max_budget
        dead = task.deadline_ms or (task.deadline_sec * 1000.0)

        for b in bids:
            b.utility_score = self.evaluator.score_bid(b, cap, dead)

        sorted_bids = sorted(bids, key=lambda b: b.utility_score, reverse=True)
        winner = sorted_bids[0]
        winner.status = "ACCEPTED"

        for b in sorted_bids[1:]:
            b.status = "REJECTED"

        return winner


class TaskMarketplace:
    """
    Master coordinator for task listings, bids, and automated award settlements.
    """

    def __init__(self):
        self.evaluator = BidEvaluator()
        self.auction = TaskAuction(self.evaluator)
        self._tasks: Dict[str, MarketplaceTask] = {}
        self._bids: Dict[str, List[AgentBid]] = {}
        self._seed_default_marketplace()

    def publish_task(
        self,
        task_or_title: Union[MarketplaceTask, str],
        required_capability_or_type: Union[str, AuctionType] = "TABLE_PARSING",
        budget_cap: float = 100.0,
        deadline_ms: float = 2500.0,
        auction_type: AuctionType = AuctionType.WEIGHTED_UTILITY,
    ) -> MarketplaceTask:
        if isinstance(task_or_title, MarketplaceTask):
            task = task_or_title
            if isinstance(required_capability_or_type, AuctionType):
                task.auction_type = required_capability_or_type
            self._tasks[task.task_id] = task
            self._bids[task.task_id] = []
            return task

        task_id = f"mkt-tsk-{uuid.uuid4().hex[:8]}"
        task = MarketplaceTask(
            task_id=task_id,
            title=task_or_title,
            name=task_or_title,
            required_capability=str(required_capability_or_type),
            budget_cap_usd=budget_cap,
            deadline_ms=deadline_ms,
            auction_type=auction_type,
            status="OPEN",
        )
        self._tasks[task_id] = task
        self._bids[task_id] = []
        return task

    def submit_bid(
        self,
        task_id_or_auction_id: str,
        bid_or_agent_id: Union[AgentBid, str],
        cost_usd: float = 50.0,
        latency_ms: float = 200.0,
        confidence: float = 0.98,
    ) -> Union[AgentBid, Tuple[bool, str]]:
        if isinstance(bid_or_agent_id, AgentBid):
            bid = bid_or_agent_id
            if task_id_or_auction_id not in self._bids:
                self._bids[task_id_or_auction_id] = []
            self._bids[task_id_or_auction_id].append(bid)
            return True, "Bid submitted successfully."

        bid = AgentBid(
            bid_id=f"bid-{uuid.uuid4().hex[:8]}",
            task_id=task_id_or_auction_id,
            auction_id=task_id_or_auction_id,
            bidder_agent_id=bid_or_agent_id,
            bid_cost_usd=cost_usd,
            bid_cost=cost_usd,
            bid_latency_ms=latency_ms,
            estimated_latency_ms=latency_ms,
            bid_confidence=confidence,
            reputation_score=confidence,
        )
        if task_id_or_auction_id not in self._bids:
            self._bids[task_id_or_auction_id] = []
        self._bids[task_id_or_auction_id].append(bid)
        return bid

    def evaluate_and_award(self, auction_id: str) -> Optional[AgentBid]:
        return self.settle_task(auction_id)

    def settle_task(self, task_id: str) -> Optional[AgentBid]:
        task = self._tasks.get(task_id)
        if not task:
            return None
        bids = self._bids.get(task_id, [])
        winner = self.auction.resolve_auction(task, bids)
        if winner:
            task.status = "AWARDED"
        return winner

    def get_auction(self, auction_id: str) -> Optional[MarketplaceTask]:
        return self._tasks.get(auction_id)

    def list_auctions(self) -> List[MarketplaceTask]:
        return list(self._tasks.values())

    def get_all_tasks(self) -> List[MarketplaceTask]:
        return list(self._tasks.values())

    def get_task_bids(self, task_id: str) -> List[AgentBid]:
        return self._bids.get(task_id, [])

    def _seed_default_marketplace(self):
        t1 = self.publish_task("Extract Tabular Line Items from 50-page Batch", "TABLE_PARSING", 50.0, 3000.0)
        self.submit_bid(t1.task_id, "agent-spec-ocr", 18.0, 850.0, 0.985)
        self.submit_bid(t1.task_id, "agent-res-opt", 12.0, 420.0, 0.920)
        self.settle_task(t1.task_id)
