"""Deliberation Voting & Social Choice Aggregation for DocuTask ACOS.

Implements Borda Count rank-order voting and consensus entropy measurement over multi-agent council votes.
"""

from __future__ import annotations

import math
from typing import Dict, List
from pydantic import BaseModel, Field

from app.runtime.deliberation.agents import CouncilAgentVote


class DeliberationVoteTally(BaseModel):
    winning_strategy_id: str
    borda_points: Dict[str, int] = Field(default_factory=dict)
    first_choice_votes: Dict[str, int] = Field(default_factory=dict)
    consensus_entropy_bits: float = 0.0
    is_unanimous: bool = False
    deliberation_verdict: str = ""


class DeliberationVotingEngine:
    """Aggregates multi-agent votes using axiomatic Borda Count social choice theory."""

    def tally_borda_count(self, votes: List[CouncilAgentVote], candidate_strategies: List[str]) -> DeliberationVoteTally:
        borda_points: Dict[str, int] = {sid: 0 for sid in candidate_strategies}
        first_choice_counts: Dict[str, int] = {sid: 0 for sid in candidate_strategies}

        num_candidates = len(candidate_strategies)

        for vote in votes:
            if vote.preferred_strategy_id in first_choice_counts:
                first_choice_counts[vote.preferred_strategy_id] += 1

            for rank_idx, strat_id in enumerate(vote.strategy_rankings):
                if strat_id in borda_points:
                    points = (num_candidates - 1) - rank_idx
                    borda_points[strat_id] += max(0, points)

        # Winner with maximum Borda points
        winner = max(borda_points, key=borda_points.get) if borda_points else candidate_strategies[0] # type: ignore

        # Consensus Shannon entropy across first choice distribution
        total_votes = len(votes)
        entropy = 0.0
        for count in first_choice_counts.values():
            if count > 0:
                p = count / total_votes
                entropy -= p * math.log2(p)

        is_unanimous = any(c == total_votes for c in first_choice_counts.values())

        verdict = (
            f"Council Consensus Reached: {winner} won with {borda_points.get(winner, 0)} Borda points "
            f"(Entropy: {entropy:.3f} bits, {'UNANIMOUS' if is_unanimous else 'SUPERMAJORITY'})."
        )

        return DeliberationVoteTally(
            winning_strategy_id=winner,
            borda_points=borda_points,
            first_choice_votes=first_choice_counts,
            consensus_entropy_bits=round(entropy, 3),
            is_unanimous=is_unanimous,
            deliberation_verdict=verdict,
        )
