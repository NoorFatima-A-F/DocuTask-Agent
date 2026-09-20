"""
Agent Identity Model.
Uniquely identifies an autonomous agent instance within the multi-agent framework.
"""

from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class AgentIdentity(BaseModel):
    """Immutable identity identifying an autonomous agent instance, role, and version."""
    agent_id: UUID = Field(default_factory=uuid4)
    name: str
    role: str = Field(default="worker")  # supervisor, planner, worker, critic, specialist
    version: str = Field(default="1.0.0")
    tenant_id: str = Field(default="default")

    model_config = {"frozen": True}
