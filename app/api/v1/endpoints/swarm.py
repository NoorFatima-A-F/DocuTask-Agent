"""
AMCN-SIP Phase 13.8 - REST API Endpoints
Comprehensive REST API for Multi-Agent Coordination, Negotiation, Consensus, Coalitions, Marketplace, Reputation, Learning, Governance & Replay.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.runtime.swarm import (
    get_swarm_runtime,
    AgentRole,
    AgentState,
    SwarmAgentProfile,
    MessageType,
    SwarmMessage,
    NegotiationOffer,
    ConsensusVotingMode,
    SwarmVote,
    AuctionType,
    MarketplaceTask,
    AgentBid,
)

router = APIRouter()


# Request Models
class RegisterAgentRequest(BaseModel):
    agent_id: str
    name: str
    role: AgentRole
    capabilities: List[str] = []
    tools: List[str] = []
    max_concurrency: int = 4
    compute_cost_per_sec: float = 0.05
    description: str = ""


class DiscoverAgentRequest(BaseModel):
    capability: Optional[str] = None
    role: Optional[AgentRole] = None
    query: Optional[str] = None


class TransitionStateRequest(BaseModel):
    target_state: AgentState
    reason: str = "Operator or autonomous trigger"


class SendMessageRequest(BaseModel):
    sender_id: str
    recipient_id: Optional[str] = None
    message_type: MessageType = MessageType.DIRECT
    topic: Optional[str] = None
    conversation_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
    context_data: Dict[str, Any] = Field(default_factory=dict)


class StartNegotiationRequest(BaseModel):
    initiator_id: str
    responder_id: str
    topic: str
    demands: Dict[str, Any]
    concessions: Dict[str, Any]
    priority: int = 1


class StartConsensusRequest(BaseModel):
    decision_id: str
    proposal: str
    voting_mode: ConsensusVotingMode = ConsensusVotingMode.WEIGHTED_REPUTATION
    eligible_voter_ids: List[str]
    quorum_threshold: float = 0.5


class CastVoteRequest(BaseModel):
    voter_id: str
    choice: str  # APPROVE, REJECT, ABSTAIN
    weight: float = 1.0
    rationale: str = ""


class CreateCoalitionRequest(BaseModel):
    coalition_id: str
    name: str
    mission_id: str
    lead_agent_id: str
    member_agent_ids: List[str]
    objective: str


class OptimizeTeamRequest(BaseModel):
    required_skills: List[str]


class PublishAuctionRequest(BaseModel):
    task_id: str
    name: str
    description: str
    required_skills: List[str]
    max_budget: float
    deadline_sec: float
    auction_type: AuctionType = AuctionType.FIRST_PRICE_SEALED


class SubmitBidRequest(BaseModel):
    bidder_id: str
    bid_amount: float
    estimated_latency_ms: float
    reputation_score: float = 0.95
    proposed_sla: str = "Standard 99.9%"


class RecordPerformanceRequest(BaseModel):
    agent_id: str
    task_success: bool
    sla_met: bool
    governance_clean: bool = True


class DelegateGrantRequest(BaseModel):
    delegator_id: str
    delegator_role: str
    delegatee_id: str
    delegatee_role: str
    scope: str
    depth: int = 1


# Endpoints


@router.get("/overview")
def get_society_overview():
    runtime = get_swarm_runtime()
    return runtime.get_society_overview()


@router.get("/agents")
def list_agents(role: Optional[AgentRole] = None, state: Optional[AgentState] = None):
    runtime = get_swarm_runtime()
    agents = runtime.registry.list_agents()
    if role:
        agents = [a for a in agents if a.role == role]
    if state:
        agents = [a for a in agents if a.state == state]
    return [a.__dict__ for a in agents]


@router.post("/agents")
def register_agent(req: RegisterAgentRequest):
    runtime = get_swarm_runtime()
    profile = SwarmAgentProfile(
        agent_id=req.agent_id,
        name=req.name,
        role=req.role,
        capabilities=req.capabilities,
        tools=req.tools,
        max_concurrency=req.max_concurrency,
        compute_cost_per_sec=req.compute_cost_per_sec,
        description=req.description,
    )
    runtime.registry.register_agent(profile)
    return {"status": "REGISTERED", "profile": profile.__dict__}


@router.post("/agents/discover")
def discover_agent(req: DiscoverAgentRequest):
    runtime = get_swarm_runtime()
    if req.capability:
        agent = runtime.directory.discover_agent(req.capability)
    elif req.role:
        agents = runtime.registry.get_by_role(req.role)
        agent = agents[0] if agents else None
    else:
        agent = runtime.directory.fallback_discovery()

    if not agent:
        raise HTTPException(status_code=404, detail="No matching agent found.")
    return {"agent": agent.__dict__}


@router.get("/agents/{agent_id}")
def get_agent_detail(agent_id: str):
    runtime = get_swarm_runtime()
    agent = runtime.registry.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent {agent_id} not found.")
    history = runtime.lifecycle.get_history(agent_id)
    return {"profile": agent.__dict__, "lifecycle_history": history}


@router.post("/agents/{agent_id}/transition")
def transition_agent_state(agent_id: str, req: TransitionStateRequest):
    runtime = get_swarm_runtime()
    success, msg = runtime.lifecycle.transition(runtime.registry, agent_id, req.target_state, req.reason)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "TRANSITIONED", "message": msg, "current_state": req.target_state.value}


@router.get("/messages")
def get_messages(conversation_id: Optional[str] = None, agent_id: Optional[str] = None):
    runtime = get_swarm_runtime()
    if conversation_id:
        msgs = runtime.communication.get_conversation_history(conversation_id)
    elif agent_id:
        msgs = runtime.communication.get_agent_inbox(agent_id)
    else:
        msgs = runtime.communication.get_all_messages()
    return [m.__dict__ for m in msgs]


@router.post("/messages/send")
def send_message(req: SendMessageRequest):
    runtime = get_swarm_runtime()
    msg = SwarmMessage(
        message_id=f"msg_{hash(req.sender_id + str(req.payload))}",
        sender_id=req.sender_id,
        recipient_id=req.recipient_id,
        message_type=req.message_type,
        topic=req.topic,
        conversation_id=req.conversation_id,
        payload=req.payload,
        context_data=req.context_data,
    )
    success, err = runtime.communication.send_message(msg)
    if not success:
        raise HTTPException(status_code=400, detail=err)
    return {"status": "SENT", "message": msg.__dict__}


@router.get("/negotiations/agreements")
def list_agreements():
    runtime = get_swarm_runtime()
    agreements = runtime.negotiation.get_all_agreements()
    return [a.__dict__ for a in agreements]


@router.post("/negotiations/start")
def start_negotiation(req: StartNegotiationRequest):
    runtime = get_swarm_runtime()
    offer = NegotiationOffer(
        offer_id=f"off_{abs(hash(req.topic))}",
        proposer_id=req.initiator_id,
        receiver_id=req.responder_id,
        topic=req.topic,
        demands=req.demands,
        concessions=req.concessions,
        priority=req.priority,
    )
    agreement = runtime.negotiation.propose_offer(offer)
    return {"status": "NEGOTIATED", "agreement": agreement.__dict__}


@router.get("/consensus/decisions")
def list_consensus_decisions():
    runtime = get_swarm_runtime()
    decisions = runtime.consensus.get_all_decisions()
    return [d.__dict__ for d in decisions]


@router.post("/consensus/start")
def start_consensus(req: StartConsensusRequest):
    runtime = get_swarm_runtime()
    decision = runtime.consensus.initiate_voting(
        decision_id=req.decision_id,
        proposal=req.proposal,
        voting_mode=req.voting_mode,
        eligible_voters=req.eligible_voter_ids,
        quorum_threshold=req.quorum_threshold,
    )
    return {"status": "VOTING_INITIATED", "decision": decision.__dict__}


@router.post("/consensus/{decision_id}/vote")
def cast_consensus_vote(decision_id: str, req: CastVoteRequest):
    runtime = get_swarm_runtime()
    vote = SwarmVote(
        voter_id=req.voter_id,
        decision_id=decision_id,
        choice=req.choice,
        weight=req.weight,
        rationale=req.rationale,
    )
    success, msg = runtime.consensus.cast_vote(decision_id, vote)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    finalized = runtime.consensus.finalize_decision(decision_id)
    return {"status": "VOTE_CAST", "message": msg, "decision": finalized.__dict__ if finalized else None}


@router.get("/coalitions")
def list_coalitions():
    runtime = get_swarm_runtime()
    coalitions = runtime.coalitions.list_coalitions()
    return [c.__dict__ for c in coalitions]


@router.post("/coalitions")
def create_coalition(req: CreateCoalitionRequest):
    runtime = get_swarm_runtime()
    coalition = runtime.coalitions.create_coalition(
        coalition_id=req.coalition_id,
        name=req.name,
        mission_id=req.mission_id,
        lead_agent_id=req.lead_agent_id,
        member_agent_ids=req.member_agent_ids,
        objective=req.objective,
    )
    return {"status": "COALITION_CREATED", "coalition": coalition.__dict__}


@router.post("/coalitions/optimize")
def optimize_team(req: OptimizeTeamRequest):
    runtime = get_swarm_runtime()
    all_agents = runtime.registry.list_agents()
    optimized = runtime.coalitions.optimizer.optimize_team(all_agents, req.required_skills)
    return {
        "required_skills": req.required_skills,
        "selected_agents": [a.__dict__ for a in optimized],
        "team_size": len(optimized),
    }


@router.get("/marketplace/auctions")
def list_auctions():
    runtime = get_swarm_runtime()
    auctions = runtime.marketplace.list_auctions()
    return [a.__dict__ for a in auctions]


@router.post("/marketplace/publish")
def publish_auction(req: PublishAuctionRequest):
    runtime = get_swarm_runtime()
    task = MarketplaceTask(
        task_id=req.task_id,
        name=req.name,
        description=req.description,
        required_skills=req.required_skills,
        max_budget=req.max_budget,
        deadline_sec=req.deadline_sec,
    )
    auction = runtime.marketplace.publish_task(task, req.auction_type)
    return {"status": "AUCTION_PUBLISHED", "auction": auction.__dict__}


@router.post("/marketplace/{auction_id}/bid")
def submit_auction_bid(auction_id: str, req: SubmitBidRequest):
    runtime = get_swarm_runtime()
    bid = AgentBid(
        bid_id=f"bid_{abs(hash(req.bidder_id + str(req.bid_amount)))}",
        auction_id=auction_id,
        bidder_agent_id=req.bidder_id,
        bid_cost=req.bid_amount,
        estimated_latency_ms=req.estimated_latency_ms,
        reputation_score=req.reputation_score,
        proposed_sla=req.proposed_sla,
    )
    success, msg = runtime.marketplace.submit_bid(auction_id, bid)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "BID_SUBMITTED", "message": msg, "bid": bid.__dict__}


@router.post("/marketplace/{auction_id}/evaluate")
def evaluate_auction(auction_id: str):
    runtime = get_swarm_runtime()
    auction = runtime.marketplace.get_auction(auction_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found.")
    winning_bid = runtime.marketplace.evaluate_and_award(auction_id)
    return {
        "auction_id": auction_id,
        "status": auction.status,
        "winning_bid": winning_bid.__dict__ if winning_bid else None,
    }


@router.get("/reputation/scores")
def list_reputations():
    runtime = get_swarm_runtime()
    reputations = runtime.reputation.get_all_reputations()
    return [r.__dict__ for r in reputations]


@router.get("/reputation/trust-graph")
def get_trust_graph():
    runtime = get_swarm_runtime()
    return {"edges": runtime.reputation.trust_engine.get_all_edges()}


@router.post("/reputation/record")
def record_reputation_event(req: RecordPerformanceRequest):
    runtime = get_swarm_runtime()
    runtime.reputation.record_performance(
        agent_id=req.agent_id,
        task_success=req.task_success,
        sla_met=req.sla_met,
        governance_clean=req.governance_clean,
    )
    rec = runtime.reputation.get_reputation(req.agent_id)
    return {"status": "UPDATED", "record": rec.__dict__ if rec else None}


@router.get("/learning/knowledge-graph")
def get_knowledge_graph():
    runtime = get_swarm_runtime()
    return runtime.learning.knowledge_graph.get_summary()


@router.get("/learning/patterns")
def list_coordination_patterns():
    runtime = get_swarm_runtime()
    patterns = runtime.learning.pattern_miner.get_patterns()
    return [p.__dict__ for p in patterns]


@router.get("/learning/insights")
def get_learned_insights():
    runtime = get_swarm_runtime()
    return runtime.learning.get_collective_learning_summary()


@router.get("/governance/summary")
def get_governance_summary():
    runtime = get_swarm_runtime()
    return runtime.governance.get_governance_summary()


@router.post("/governance/delegate")
def create_delegation_grant(req: DelegateGrantRequest):
    runtime = get_swarm_runtime()
    success, grant, msg = runtime.governance.grant_delegation(
        delegator_id=req.delegator_id,
        delegator_role=req.delegator_role,
        delegatee_id=req.delegatee_id,
        delegatee_role=req.delegatee_role,
        scope=req.scope,
        depth=req.depth,
    )
    if not success:
        raise HTTPException(status_code=403, detail=msg)
    return {"status": "GRANTED", "grant": grant.__dict__ if grant else None, "message": msg}


@router.get("/replay/timeline")
def get_replay_timeline(limit: int = 50):
    runtime = get_swarm_runtime()
    return runtime.replay.get_timeline(limit)


@router.get("/replay/trace")
def reconstruct_replay_trace(start_idx: int = 0, end_idx: Optional[int] = None):
    runtime = get_swarm_runtime()
    return runtime.replay.reconstruct_trace(start_idx, end_idx)
