"""
Voting Engine.
Supports plurality, majority, and approval voting mechanisms for multi-agent decision making.
"""

from typing import Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, Field


class AgentVote(BaseModel):
    """Vote cast by an individual agent."""
    voter_agent_id: UUID
    choice: str
    weight: float = Field(default=1.0, ge=0.0)

    model_config = {"frozen": True}


class VotingResult(BaseModel):
    """Outcome of a voting round."""
    winning_choice: Optional[str]
    vote_counts: Dict[str, float]
    total_votes: int
    has_majority: bool

    model_config = {"frozen": True}


class VotingEngine:
    """Calculates voting outcomes across agent choices."""

    def tally_majority_vote(self, votes: List[AgentVote]) -> VotingResult:
        """Computes weighted majority vote."""
        if not votes:
            return VotingResult(winning_choice=None, vote_counts={}, total_votes=0, has_majority=False)

        counts: Dict[str, float] = {}
        total_weight = 0.0

        for v in votes:
            counts[v.choice] = counts.get(v.choice, 0.0) + v.weight
            total_weight += v.weight

        winning_choice = max(counts, key=counts.get)
        winner_weight = counts[winning_choice]
        has_majority = (winner_weight / total_weight) > 0.5 if total_weight > 0 else False

        return VotingResult(
            winning_choice=winning_choice,
            vote_counts=counts,
            total_votes=len(votes),
            has_majority=has_majority
        )
