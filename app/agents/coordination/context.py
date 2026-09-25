"""
Coordination Context, Request, and Result Models.
Defines canonical envelopes for invoking the Multi-Agent Coordination Engine.
"""

from typing import Any, Dict, List
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.coordination.lifecycle import CoordinationLifecycleState
from app.agents.coordination.metadata import CoordinationIdentity, CoordinationStatistics


class CoordinationContext(BaseModel):
    """Operational limits and correlation boundaries for coordination."""
    tenant_id: str = Field(default="default")
    correlation_id: str = Field(default_factory=lambda: str(uuid4()))
    max_coordination_timeout_sec: float = Field(default=300.0, gt=0.0)
    enable_work_stealing: bool = True
    enable_consensus_validation: bool = True
    parameters: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class CoordinationRequest(BaseModel):
    """Request payload to coordinate multi-agent execution for a high-level goal."""
    goal: str
    initiator_agent_id: UUID
    context: CoordinationContext = Field(default_factory=CoordinationContext)
    required_capabilities: List[str] = Field(default_factory=list)
    input_data: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class CoordinationResult(BaseModel):
    """Structured outcome produced by the Coordination Engine."""
    identity: CoordinationIdentity
    lifecycle_state: CoordinationLifecycleState = Field(default=CoordinationLifecycleState.COMPLETED)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    participating_agents: List[UUID] = Field(default_factory=list)
    teams_involved: List[UUID] = Field(default_factory=list)
    statistics: CoordinationStatistics = Field(default_factory=CoordinationStatistics)
    errors: List[str] = Field(default_factory=list)

    model_config = {"frozen": True}
