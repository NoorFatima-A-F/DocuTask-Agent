"""
Agent Matcher and Selector.
Selects optimal agents based on capabilities, current workload, availability, and reputation.
"""

from typing import List, Optional
from uuid import UUID
from app.agents.coordination.agent import Agent
from app.agents.coordination.capability_matcher import CapabilityMatcher, CapabilityRequirement
from app.agents.coordination.exceptions import MissingCapabilityError


class AgentMatcher:
    """Matches requirements to registered agents using CapabilityMatcher."""

    def __init__(self, matcher: Optional[CapabilityMatcher] = None):
        self.matcher = matcher or CapabilityMatcher()

    def find_best_candidates(
        self,
        required: CapabilityRequirement,
        candidates: List[Agent]
    ) -> List[Agent]:
        """Returns qualified candidates ordered by match score."""
        match_results = self.matcher.match_capabilities(required, candidates)
        qualified_ids = {r.agent_id for r in match_results if r.is_fully_qualified}

        if not qualified_ids:
            # Fall back to best non-qualified if no exact match
            if match_results and match_results[0].match_score >= 0.5:
                qualified_ids = {match_results[0].agent_id}
            else:
                raise MissingCapabilityError(
                    f"No agent satisfied the required capabilities: {required.required_skills}"
                )

        # Map back to Agent instances preserving match order
        id_to_agent = {str(a.agent_id): a for a in candidates}
        return [id_to_agent[r.agent_id] for r in match_results if r.agent_id in qualified_ids]


class AgentSelector:
    """Selects the single optimal agent for a task considering workload and concurrency."""

    def __init__(self, matcher: Optional[AgentMatcher] = None):
        self.matcher = matcher or AgentMatcher()

    def select_agent(
        self,
        required: CapabilityRequirement,
        candidates: List[Agent]
    ) -> Agent:
        """Selects the best available candidate agent."""
        best_candidates = self.matcher.find_best_candidates(required, candidates)

        # Pick candidate with least active tasks
        best_candidates.sort(key=lambda a: (len(a.current_tasks), -a.reputation_score))
        return best_candidates[0]
