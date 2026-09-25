"""
Agent Profile Builder.
Fluent builder for constructing validated Agent instances and profiles.
"""

from typing import List
from uuid import UUID, uuid4
from app.agents.coordination.agent import Agent
from app.agents.coordination.agent_identity import AgentIdentity
from app.agents.coordination.agent_profile import AgentProfile
from app.agents.coordination.capability import AgentSkill, CapabilityProfile


class AgentBuilder:
    """Fluent builder for constructing Agent domain entities."""

    def __init__(self, name: str):
        self._name = name
        self._agent_id = uuid4()
        self._role = "worker"
        self._version = "1.0.0"
        self._skills: List[AgentSkill] = []
        self._tools: List[str] = []
        self._domains: List[str] = ["general"]
        self._confidence = 0.95
        self._cost_usd = 0.01
        self._latency_ms = 500.0

    def with_id(self, agent_id: UUID) -> "AgentBuilder":
        self._agent_id = agent_id
        return self

    def with_role(self, role: str) -> "AgentBuilder":
        self._role = role
        return self

    def add_skill(self, name: str, domain: str = "general", confidence: float = 0.9) -> "AgentBuilder":
        self._skills.append(AgentSkill(name=name, domain=domain, confidence_score=confidence))
        return self

    def add_tool(self, tool_name: str) -> "AgentBuilder":
        self._tools.append(tool_name)
        return self

    def add_domain(self, domain: str) -> "AgentBuilder":
        self._domains.append(domain)
        return self

    def with_confidence(self, conf: float) -> "AgentBuilder":
        self._confidence = conf
        return self

    def with_cost(self, cost_usd: float) -> "AgentBuilder":
        self._cost_usd = cost_usd
        return self

    def with_latency(self, latency_ms: float) -> "AgentBuilder":
        self._latency_ms = latency_ms
        return self

    def build(self) -> Agent:
        identity = AgentIdentity(
            agent_id=self._agent_id,
            name=self._name,
            role=self._role,
            version=self._version
        )
        capabilities = CapabilityProfile(
            skills=self._skills,
            supported_tools=self._tools,
            execution_domains=list(set(self._domains)),
            confidence_rating=self._confidence,
            cost_per_task_usd=self._cost_usd,
            average_latency_ms=self._latency_ms
        )
        profile = AgentProfile(identity=identity, capabilities=capabilities)
        return Agent(profile=profile)
