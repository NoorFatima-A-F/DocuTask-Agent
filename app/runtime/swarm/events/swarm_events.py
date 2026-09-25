"""
AMCN-SIP Phase 13.8 - Swarm Domain Events Layer
Immutable, replay-verifiable operational events for multi-agent coordination, negotiation, consensus, coalitions, and marketplace.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class AgentRoleType(str, Enum):
    EXECUTIVE = "EXECUTIVE"
    PLANNER = "PLANNER"
    COORDINATOR = "COORDINATOR"
    NEGOTIATOR = "NEGOTIATOR"
    SPECIALIST = "SPECIALIST"
    VALIDATOR = "VALIDATOR"
    REVIEWER = "REVIEWER"
    RESOURCE = "RESOURCE"
    KNOWLEDGE = "KNOWLEDGE"
    SECURITY = "SECURITY"
    RECOVERY = "RECOVERY"
    OBSERVER = "OBSERVER"


class AgentLifecycleState(str, Enum):
    CREATED = "CREATED"
    REGISTERED = "REGISTERED"
    AVAILABLE = "AVAILABLE"
    ASSIGNED = "ASSIGNED"
    EXECUTING = "EXECUTING"
    WAITING = "WAITING"
    NEGOTIATING = "NEGOTIATING"
    VOTING = "VOTING"
    RECOVERING = "RECOVERING"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


AgentRole = AgentRoleType
AgentState = AgentLifecycleState


class NegotiationStatus(str, Enum):
    PROPOSED = "PROPOSED"
    COUNTER_OFFERED = "COUNTER_OFFERED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    REVISED = "REVISED"
    WITHDRAWN = "WITHDRAWN"
    DEADLOCKED = "DEADLOCKED"
    TIMED_OUT = "TIMED_OUT"


class ConsensusVotingMode(str, Enum):
    MAJORITY = "MAJORITY"
    WEIGHTED = "WEIGHTED"
    WEIGHTED_REPUTATION = "WEIGHTED_REPUTATION"
    CONFIDENCE_WEIGHTED = "CONFIDENCE_WEIGHTED"
    EXPERTISE_WEIGHTED = "EXPERTISE_WEIGHTED"
    UNANIMOUS = "UNANIMOUS"
    QUORUM = "QUORUM"
    BYZANTINE_FAULT_TOLERANT = "BYZANTINE_FAULT_TOLERANT"


@dataclass(frozen=True)
class SwarmBaseEvent:
    event_id: str = field(default_factory=lambda: f"swm-evt-{uuid.uuid4().hex[:12]}")
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    event_type: str = "SwarmBaseEvent"
    agent_id: Optional[str] = None
    mission_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentRegistered(SwarmBaseEvent):
    event_type: str = "AgentRegistered"
    agent_name: str = ""
    role: AgentRoleType = AgentRoleType.SPECIALIST
    capabilities: List[str] = field(default_factory=list)
    initial_reputation: float = 1.0


@dataclass(frozen=True)
class AgentDiscovered(SwarmBaseEvent):
    event_type: str = "AgentDiscovered"
    search_query: str = ""
    discovered_agent_id: str = ""
    match_score: float = 0.95


@dataclass(frozen=True)
class AgentRetired(SwarmBaseEvent):
    event_type: str = "AgentRetired"
    reason: str = "NORMAL_COMPLETION"
    total_tasks_completed: int = 0


@dataclass(frozen=True)
class AgentStatusChanged(SwarmBaseEvent):
    event_type: str = "AgentStatusChanged"
    previous_state: AgentLifecycleState = AgentLifecycleState.AVAILABLE
    new_state: AgentLifecycleState = AgentLifecycleState.ASSIGNED


@dataclass(frozen=True)
class TaskPublished(SwarmBaseEvent):
    event_type: str = "TaskPublished"
    task_id: str = ""
    required_capabilities: List[str] = field(default_factory=list)
    budget_cap_usd: float = 0.05
    deadline_ms: float = 3000.0


@dataclass(frozen=True)
class TaskBidSubmitted(SwarmBaseEvent):
    event_type: str = "TaskBidSubmitted"
    bid_id: str = ""
    task_id: str = ""
    bidder_agent_id: str = ""
    bid_cost_usd: float = 0.015
    bid_latency_ms: float = 450.0
    bid_confidence: float = 0.98


@dataclass(frozen=True)
class BidAccepted(SwarmBaseEvent):
    event_type: str = "BidAccepted"
    bid_id: str = ""
    task_id: str = ""
    winning_agent_id: str = ""
    agreed_price_usd: float = 0.015


@dataclass(frozen=True)
class TaskDelegated(SwarmBaseEvent):
    event_type: str = "TaskDelegated"
    delegator_agent_id: str = ""
    delegatee_agent_id: str = ""
    task_id: str = ""
    delegation_depth: int = 1


@dataclass(frozen=True)
class CoalitionCreated(SwarmBaseEvent):
    event_type: str = "CoalitionCreated"
    coalition_id: str = ""
    coalition_name: str = ""
    member_agent_ids: List[str] = field(default_factory=list)
    objective: str = ""


@dataclass(frozen=True)
class CoalitionMerged(SwarmBaseEvent):
    event_type: str = "CoalitionMerged"
    parent_coalition_ids: List[str] = field(default_factory=list)
    new_coalition_id: str = ""


@dataclass(frozen=True)
class CoalitionSplit(SwarmBaseEvent):
    event_type: str = "CoalitionSplit"
    original_coalition_id: str = ""
    child_coalition_ids: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class CoalitionDissolved(SwarmBaseEvent):
    event_type: str = "CoalitionDissolved"
    coalition_id: str = ""
    reason: str = "OBJECTIVE_ACCOMPLISHED"


@dataclass(frozen=True)
class NegotiationStarted(SwarmBaseEvent):
    event_type: str = "NegotiationStarted"
    negotiation_id: str = ""
    initiator_agent_id: str = ""
    respondent_agent_ids: List[str] = field(default_factory=list)
    topic: str = ""


@dataclass(frozen=True)
class NegotiationProposalSubmitted(SwarmBaseEvent):
    event_type: str = "NegotiationProposalSubmitted"
    negotiation_id: str = ""
    proposer_agent_id: str = ""
    proposal_payload: Dict[str, Any] = field(default_factory=dict)
    round_number: int = 1


@dataclass(frozen=True)
class NegotiationCounterProposalSubmitted(SwarmBaseEvent):
    event_type: str = "NegotiationCounterProposalSubmitted"
    negotiation_id: str = ""
    proposer_agent_id: str = ""
    counter_payload: Dict[str, Any] = field(default_factory=dict)
    round_number: int = 2


@dataclass(frozen=True)
class NegotiationCompleted(SwarmBaseEvent):
    event_type: str = "NegotiationCompleted"
    negotiation_id: str = ""
    final_status: NegotiationStatus = NegotiationStatus.ACCEPTED
    agreement_hash: str = ""
    participating_agents: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class NegotiationDeadlocked(SwarmBaseEvent):
    event_type: str = "NegotiationDeadlocked"
    negotiation_id: str = ""
    deadlock_reason: str = ""
    escalate_to: str = "EXECUTIVE_COORDINATOR"


@dataclass(frozen=True)
class ConsensusStarted(SwarmBaseEvent):
    event_type: str = "ConsensusStarted"
    consensus_id: str = ""
    topic: str = ""
    voting_mode: ConsensusVotingMode = ConsensusVotingMode.CONFIDENCE_WEIGHTED
    eligible_voter_ids: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class VoteCast(SwarmBaseEvent):
    event_type: str = "VoteCast"
    consensus_id: str = ""
    voter_agent_id: str = ""
    vote_value: str = ""
    vote_weight: float = 1.0
    confidence: float = 0.95
    reasoning: str = ""


@dataclass(frozen=True)
class ConsensusReached(SwarmBaseEvent):
    event_type: str = "ConsensusReached"
    consensus_id: str = ""
    outcome: str = ""
    consensus_ratio: float = 1.0
    quorum_reached: bool = True
    signed_decision_hash: str = ""


@dataclass(frozen=True)
class ConsensusFailed(SwarmBaseEvent):
    event_type: str = "ConsensusFailed"
    consensus_id: str = ""
    reason: str = "QUORUM_NOT_REACHED"


@dataclass(frozen=True)
class DelegationCreated(SwarmBaseEvent):
    event_type: str = "DelegationCreated"
    delegation_id: str = ""
    grantor_agent_id: str = ""
    grantee_agent_id: str = ""
    granted_capabilities: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class DelegationRevoked(SwarmBaseEvent):
    event_type: str = "DelegationRevoked"
    delegation_id: str = ""
    reason: str = "REVOCATION_POLICY"


@dataclass(frozen=True)
class ConflictDetected(SwarmBaseEvent):
    event_type: str = "ConflictDetected"
    conflict_id: str = ""
    conflict_type: str = "RESOURCE_CONTENTION"
    contending_agent_ids: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class ConflictResolved(SwarmBaseEvent):
    event_type: str = "ConflictResolved"
    conflict_id: str = ""
    resolution_strategy: str = "PRIORITY_SCALARIZATION"
    winning_agent_id: str = ""


@dataclass(frozen=True)
class MessageSent(SwarmBaseEvent):
    event_type: str = "MessageSent"
    message_id: str = ""
    sender_agent_id: str = ""
    recipient_agent_id: str = ""
    message_type: str = "DIRECT"
    topic: str = ""


@dataclass(frozen=True)
class MessageDelivered(SwarmBaseEvent):
    event_type: str = "MessageDelivered"
    message_id: str = ""
    delivery_latency_ms: float = 2.5


@dataclass(frozen=True)
class ContextShared(SwarmBaseEvent):
    event_type: str = "ContextShared"
    sharing_agent_id: str = ""
    recipient_agent_id: str = ""
    context_type: str = "EVIDENCE_PROOF_REF"
    context_hash: str = ""


@dataclass(frozen=True)
class TrustUpdated(SwarmBaseEvent):
    event_type: str = "TrustUpdated"
    source_agent_id: str = ""
    target_agent_id: str = ""
    new_trust_score: float = 0.95
    trust_delta: float = +0.02


@dataclass(frozen=True)
class ReputationUpdated(SwarmBaseEvent):
    event_type: str = "ReputationUpdated"
    agent_id: str = ""
    new_reputation_score: float = 0.98
    performance_factor: float = 1.0


@dataclass(frozen=True)
class SwarmLearningCompleted(SwarmBaseEvent):
    event_type: str = "SwarmLearningCompleted"
    session_id: str = ""
    new_patterns_mined_count: int = 4
    knowledge_graph_node_updates: int = 12


@dataclass(frozen=True)
class CoordinationFailed(SwarmBaseEvent):
    event_type: str = "CoordinationFailed"
    failure_reason: str = ""
    affected_agents_count: int = 0


@dataclass(frozen=True)
class MissionCoordinated(SwarmBaseEvent):
    event_type: str = "MissionCoordinated"
    mission_id: str = ""
    participating_coalition_id: str = ""
    total_coordination_rounds: int = 3
    final_execution_confidence: float = 0.992
