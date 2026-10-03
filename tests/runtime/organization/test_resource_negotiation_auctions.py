"""
Test Suite: Autonomous Negotiation & Game-Theoretic Framework
Validates Vickrey second-price auctions, bilateral resource trades, Nash Bargaining, and signed SLA contracts.
"""
from app.runtime.negotiation.auction_manager import VickreyAuctionManager, AuctionBid
from app.runtime.negotiation.resource_negotiation import ResourceNegotiator
from app.runtime.negotiation.utility_negotiator import UtilityNegotiator
from app.runtime.negotiation.contract_manager import ContractManager


def test_vickrey_second_price_auction():
    mgr = VickreyAuctionManager()
    
    bids = [
        AuctionBid("dept_a", 100.0, 2, 0.9),
        AuctionBid("dept_b", 75.0, 2, 0.8),
        AuctionBid("dept_c", 50.0, 2, 0.7),
    ]

    result = mgr.run_auction("GPU_SLOT", units_available=2, bids=bids)
    
    # Highest bidder wins (dept_a at 100.0)
    assert result.winning_department_id == "dept_a"
    assert result.winning_bid_amount == 100.0
    # Pays second highest bid (75.0)
    assert result.clearing_price_credits == 75.0


def test_bilateral_resource_trade():
    negotiator = ResourceNegotiator()
    
    prop = negotiator.propose_trade(
        initiator_dept_id="dept_ocr",
        target_dept_id="dept_extraction",
        offered_resource="OCR_THREADS",
        offered_quantity=2.0,
        requested_resource="LLM_TOKENS",
        requested_quantity=10000.0,
        duration_seconds=600.0,
        rationale="Trade surplus OCR capacity for LLM quota",
    )

    assert prop.status == "PROPOSED"
    assert negotiator.accept_trade(prop.proposal_id) is True
    assert negotiator.proposals[prop.proposal_id].status == "ACCEPTED"


def test_nash_bargaining_utility_solution():
    solution = UtilityNegotiator.solve_nash_bargaining(
        dept_a="dept_extraction",
        dept_b="dept_ocr",
        total_resource=100.0,
        disagreement_a=10.0,
        disagreement_b=10.0,
        weight_a=0.6,
        weight_b=0.4,
    )

    assert solution.optimal_allocation_a == 58.0
    assert solution.optimal_allocation_b == 42.0
    assert solution.optimal_allocation_a + solution.optimal_allocation_b == 100.0
    assert solution.is_pareto_optimal is True


def test_contract_manager_creation_and_signature():
    mgr = ContractManager()
    
    contract = mgr.create_contract(
        provider_dept_id="dept_ocr",
        consumer_dept_id="dept_extraction",
        resource_type="OCR_STREAM",
        committed_capacity=15.0,
        max_latency_ms=200.0,
        penalty_rate=3.0,
    )

    assert contract.is_active is True
    assert contract.signature_digest.startswith("ED25519_SIG_")
    assert len(mgr.list_contracts()) >= 2
