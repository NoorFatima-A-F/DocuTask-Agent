"""
Consensus Engine.
Verifies quorum thresholds and confirms distributed consensus on decisions across agent teams.
"""

from typing import List, Optional
from pydantic import BaseModel
from app.agents.coordination.exceptions import ConsensusNotReachedError
from app.agents.coordination.interfaces import IConsensusEngine
from app.agents.coordination.voting import AgentVote, VotingEngine, VotingResult


class ConsensusOutcome(BaseModel):
    """Formal consensus verification outcome."""
    topic: str
    agreed_decision: str
    quorum_met: bool
    majority_met: bool
    total_participants: int
    participating_voters: int

    model_config = {"frozen": True}


class ConsensusEngine(IConsensusEngine):
    """Enforces quorum and majority consensus rules."""

    def __init__(self, voting_engine: Optional[VotingEngine] = None):
        self.voting_engine = voting_engine or VotingEngine()

    async def reach_consensus(
        self,
        topic: str,
        votes: List[AgentVote],
        total_cluster_size: Optional[int] = None,
        quorum_fraction: float = 0.5
    ) -> ConsensusOutcome:
        """Evaluates whether quorum is present and a majority decision is formed."""
        cluster_size = total_cluster_size or len(votes)
        voter_count = len(votes)

        # 1. Quorum check
        quorum_met = (voter_count / cluster_size) >= quorum_fraction if cluster_size > 0 else False
        if not quorum_met:
            raise ConsensusNotReachedError(
                f"Quorum failure on topic '{topic}': {voter_count}/{cluster_size} votes cast."
            )

        # 2. Majority tally
        result: VotingResult = self.voting_engine.tally_majority_vote(votes)
        if not result.has_majority or not result.winning_choice:
            raise ConsensusNotReachedError(
                f"Majority not achieved on topic '{topic}'. Vote distribution: {result.vote_counts}"
            )

        return ConsensusOutcome(
            topic=topic,
            agreed_decision=result.winning_choice,
            quorum_met=True,
            majority_met=True,
            total_participants=cluster_size,
            participating_voters=voter_count
        )
