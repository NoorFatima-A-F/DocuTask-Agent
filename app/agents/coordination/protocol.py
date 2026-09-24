"""
Coordination Protocols.
Defines formal communication protocols: FIPA-ACL, Contract Net, Auction, Consensus, and Swarm.
"""

from enum import Enum


class ProtocolType(str, Enum):
    """Supported coordination and negotiation protocol types."""
    FIPA_REQUEST = "FIPA_REQUEST"
    CONTRACT_NET = "CONTRACT_NET"
    AUCTION_FIRST_PRICE = "AUCTION_FIRST_PRICE"
    AUCTION_DUTCH = "AUCTION_DUTCH"
    MAJORITY_VOTING = "MAJORITY_VOTING"
    LEADER_ELECTION = "LEADER_ELECTION"
    SWARM_CONSENSUS = "SWARM_CONSENSUS"


class ProtocolState(str, Enum):
    """Protocol negotiation lifecycle states."""
    INITIATED = "INITIATED"
    IN_PROGRESS = "IN_PROGRESS"
    PROPOSALS_RECEIVED = "PROPOSALS_RECEIVED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    TERMINATED = "TERMINATED"
