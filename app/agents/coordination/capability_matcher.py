"""
Capability Matcher.
Matches task execution requirements (skills, tools, domains, latency limits) against candidate agents.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.agents.coordination.agent import Agent
from app.agents.coordination.interfaces import ICapabilityMatcher


class CapabilityRequirement(BaseModel):
    """Specification of capabilities required to execute a task."""
    required_skills: List[str] = Field(default_factory=list)
    required_tools: List[str] = Field(default_factory=list)
    domain: Optional[str] = None
    max_acceptable_cost_usd: float = Field(default=1.0, ge=0.0)
    max_acceptable_latency_ms: float = Field(default=10000.0, ge=0.0)
    min_confidence: float = Field(default=0.8, ge=0.0, le=1.0)

    model_config = {"frozen": True}


class CapabilityMatchResult(BaseModel):
    """Scored match result for an agent candidate."""
    agent_id: str
    match_score: float = Field(ge=0.0, le=1.0)
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    matched_tools: List[str] = Field(default_factory=list)
    is_fully_qualified: bool = True

    model_config = {"frozen": True}


class CapabilityMatcher(ICapabilityMatcher):
    """Evaluates agent capability profiles against task requirements."""

    def match_capabilities(
        self,
        required: CapabilityRequirement,
        candidates: List[Agent]
    ) -> List[CapabilityMatchResult]:
        """Calculates multi-criteria capability scores for all candidates."""
        results: List[CapabilityMatchResult] = []

        for candidate in candidates:
            cap = candidate.profile.capabilities
            agent_skills = {s.name.lower(): s for s in cap.skills}
            agent_tools = {t.lower() for t in cap.supported_tools}

            matched_skills: List[str] = []
            missing_skills: List[str] = []
            for req_skill in required.required_skills:
                if req_skill.lower() in agent_skills:
                    matched_skills.append(req_skill)
                else:
                    missing_skills.append(req_skill)

            matched_tools = [t for t in required.required_tools if t.lower() in agent_tools]
            missing_tools = [t for t in required.required_tools if t.lower() not in agent_tools]

            # Hard qualification gate
            fully_qualified = (
                len(missing_skills) == 0
                and len(missing_tools) == 0
                and cap.confidence_rating >= required.min_confidence
                and cap.cost_per_task_usd <= required.max_acceptable_cost_usd
                and cap.average_latency_ms <= required.max_acceptable_latency_ms
            )

            # Compute match score
            skill_ratio = len(matched_skills) / len(required.required_skills) if required.required_skills else 1.0
            tool_ratio = len(matched_tools) / len(required.required_tools) if required.required_tools else 1.0
            score = (
                0.4 * skill_ratio
                + 0.3 * tool_ratio
                + 0.2 * cap.confidence_rating
                + 0.1 * candidate.reputation_score
            )

            results.append(CapabilityMatchResult(
                agent_id=str(candidate.agent_id),
                match_score=max(0.0, min(1.0, score)),
                matched_skills=matched_skills,
                missing_skills=missing_skills,
                matched_tools=matched_tools,
                is_fully_qualified=fully_qualified
            ))

        # Sort descending by match_score
        results.sort(key=lambda r: (r.is_fully_qualified, r.match_score), reverse=True)
        return results
