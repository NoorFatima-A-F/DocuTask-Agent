from app.runtime.deliberation.agents import CouncilAgent
from app.runtime.deliberation.voting import DeliberationVotingEngine
from app.runtime.deliberation.auction import VickreyTaskAuctioneer, WorkerTaskBid
from app.runtime.deliberation.council import DeliberationCouncilCoordinator


def test_council_agent_opinions():
    agent = CouncilAgent(agent_id="agt_risk_test", role_name="RISK_AGENT", domain_objective="Zero Trust Safety")
    candidates = [
        {"strategy_id": "strat_alpha_fast"},
        {"strategy_id": "strat_delta_pareto"},
    ]
    vote = agent.formulate_opinion(candidates, {"mission_id": "m_test"})
    assert vote.agent_role == "RISK_AGENT"
    assert len(vote.strategy_rankings) == 2


def test_deliberation_borda_voting():
    engine = DeliberationVotingEngine()
    agent_risk = CouncilAgent(agent_id="agt_risk", role_name="RISK_AGENT", domain_objective="Safety")
    agent_econ = CouncilAgent(agent_id="agt_econ", role_name="ECONOMIC_AGENT", domain_objective="Cost")
    
    candidates = [{"strategy_id": "strat_delta_pareto"}, {"strategy_id": "strat_alpha_fast"}]
    v1 = agent_risk.formulate_opinion(candidates, {})
    v2 = agent_econ.formulate_opinion(candidates, {})
    
    tally = engine.tally_borda_count([v1, v2], ["strat_delta_pareto", "strat_alpha_fast"])
    assert tally.winning_strategy_id in ["strat_delta_pareto", "strat_alpha_fast"]
    assert tally.consensus_entropy_bits >= 0


def test_vickrey_second_price_auction():
    auctioneer = VickreyTaskAuctioneer()
    bids = [
        WorkerTaskBid(bidder_agent_id="agt_plan", task_id="task_ocr", bid_amount_credits=10.0),
        WorkerTaskBid(bidder_agent_id="agt_risk", task_id="task_ocr", bid_amount_credits=15.0),
        WorkerTaskBid(bidder_agent_id="agt_econ", task_id="task_ocr", bid_amount_credits=8.0),
    ]
    res = auctioneer.conduct_task_auction("task_ocr", bids)
    assert res.winning_agent_id == "agt_risk"  # Highest bidder
    assert res.clearing_price_credits == 10.0   # Second highest price


def test_deliberation_council_session():
    coordinator = DeliberationCouncilCoordinator()
    session = coordinator.convene_deliberation_session(mission_id="m_session_001")
    
    assert len(session.participating_agents) == 8
    assert len(session.agent_arguments) == 8
    assert session.final_ratified_strategy_id != ""
    assert len(session.resource_auctions) > 0
