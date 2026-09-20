"""
Supervisor Agent.
Supervises agent teams, reviews delegated task outputs, and handles multi-agent escalation.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from app.agents.coordination.agent import Agent
from app.agents.coordination.delegation import DelegationRequest, DelegationResult


class SupervisorAgent:
    """High-level supervisory authority overseeing team composition and delegation progression."""

    def __init__(self, agent: Agent):
        self.agent = agent

    @property
    def supervisor_id(self) -> UUID:
        return self.agent.agent_id

    def review_delegation_outcome(self, result: DelegationResult) -> bool:
        """Reviews aggregated delegation results and determines if escalation is needed."""
        return len(result.errors) == 0
