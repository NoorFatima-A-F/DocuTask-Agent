"""
Capability, Skill, and Resource Models.
Defines formal specifications of what an agent can perform, its cost, latency, and tool requirements.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class AgentSkill(BaseModel):
    """Specific skill or competency advertised by an agent."""
    name: str
    description: str = ""
    domain: str = "general"  # financial, legal, technical, extraction, summarization
    confidence_score: float = Field(default=0.9, ge=0.0, le=1.0)
    parameters_schema: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class CapabilityProfile(BaseModel):
    """Aggregate capability specification advertised by an agent."""
    skills: List[AgentSkill] = Field(default_factory=list)
    supported_tools: List[str] = Field(default_factory=list)
    supported_plans: List[str] = Field(default_factory=list)
    execution_domains: List[str] = Field(default_factory=list)
    max_concurrency: int = Field(default=4, ge=1)
    cost_per_task_usd: float = Field(default=0.01, ge=0.0)
    average_latency_ms: float = Field(default=500.0, ge=0.0)
    confidence_rating: float = Field(default=0.95, ge=0.0, le=1.0)

    model_config = {"frozen": True}
