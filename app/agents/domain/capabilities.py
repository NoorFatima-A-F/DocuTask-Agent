"""
Agent Capabilities Domain Model.
Agents advertise capabilities; tasks declare required capabilities.
"""

from typing import Dict, List, Set
from pydantic import BaseModel, Field
from app.agents.domain.enums import CapabilityType


class AgentCapability(BaseModel):
    """Capability specification object."""

    capability_type: CapabilityType
    version: str = Field(default="v1.0")
    parameters: Dict[str, str] = Field(default_factory=dict)

    model_config = {"frozen": True}


class CapabilityRequirement(BaseModel):
    """Set of required capabilities for task execution."""

    required: List[AgentCapability] = Field(default_factory=list)

    def is_satisfied_by(self, agent_capabilities: List[AgentCapability]) -> bool:
        """Returns True if all required capabilities are present in agent capabilities."""
        agent_types: Set[CapabilityType] = {cap.capability_type for cap in agent_capabilities}
        return all(req.capability_type in agent_types for req in self.required)
