"""
Agent Profile Model.
Comprehensive descriptor of an autonomous agent: identity, capabilities, performance traits, and limits.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.agents.coordination.agent_identity import AgentIdentity
from app.agents.coordination.capability import CapabilityProfile


class AgentProfile(BaseModel):
    """Profile describing an agent's identity, advertised capabilities, and operational attributes."""
    identity: AgentIdentity
    capabilities: CapabilityProfile = Field(default_factory=CapabilityProfile)
    endpoint_url: Optional[str] = None
    priority_level: int = Field(default=1, ge=1, le=10)
    attributes: Dict[str, str] = Field(default_factory=dict)

    model_config = {"frozen": True}
