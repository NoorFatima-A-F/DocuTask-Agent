"""
AMCN-SIP Phase 13.8 - Autonomous Multi-Agent Coordination, Negotiation & Swarm Intelligence Platform
"""

from app.runtime.swarm.events.swarm_events import *
from app.runtime.swarm.runtime import *
from app.runtime.swarm.communication import *
from app.runtime.swarm.negotiation import *
from app.runtime.swarm.consensus import *
from app.runtime.swarm.coalitions import *
from app.runtime.swarm.marketplace import *
from app.runtime.swarm.reputation import *
from app.runtime.swarm.learning import *
from app.runtime.swarm.governance import *
from app.runtime.swarm.explainability import *

__all__ = [
    # Runtime & Profiles
    "AgentRole",
    "AgentState",
    "SwarmAgentProfile",
    "AgentRegistry",
    "AgentLifecycleManager",
    "AgentDirectory",
    "AgentCoordinator",
    "SwarmRuntime",
    "get_swarm_runtime",
    # Communication
    "MessageType",
    "SwarmMessage",
    "MessageValidator",
    "ContextExchangeEngine",
    "ConversationManager",
    "CommunicationBus",
    # Negotiation
    "NegotiationOffer",
    "NegotiationAgreement",
    "BargainingEngine",
    "ConflictResolver",
    "AgreementLedger",
    "NegotiationEngine",
    # Consensus
    "ConsensusVotingMode",
    "SwarmVote",
    "ConsensusDecision",
    "VotingManager",
    "ConsensusValidator",
    "DecisionFinalizer",
    "ConsensusEngine",
    # Coalitions
    "AgentCoalition",
    "TeamOptimizer",
    "CoalitionMemory",
    "CoalitionManager",
    # Marketplace
    "AuctionType",
    "MarketplaceTask",
    "AgentBid",
    "BidEvaluator",
    "TaskAuction",
    "TaskMarketplace",
    # Reputation
    "AgentReputationRecord",
    "ReputationDecayEngine",
    "TrustEngine",
    "ReputationEngine",
    # Learning
    "SwarmKnowledgeNode",
    "SwarmKnowledgeEdge",
    "CoordinationPattern",
    "SwarmKnowledgeGraph",
    "CollaborationPatternMiner",
    "CollectiveLearningEngine",
    # Governance
    "AuthorityTier",
    "ROLE_TIER_MAPPING",
    "DelegationPolicy",
    "DelegationGrant",
    "DelegationValidator",
    "SwarmGovernanceEngine",
    # Explainability
    "CoordinationFrame",
    "CoordinationReplayEngine",
]
