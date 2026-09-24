"""
Core Planning Domain Contracts and Aggregate Models.
Defines Plan, PlanReference, PlanningRequest, PlanningResult, and PlanningSession.
"""

from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.planning.constraints import PlanConstraint
from app.agents.planning.dependencies import Dependency
from app.agents.planning.graph import PlanGraph
from app.agents.planning.lifecycle import PlanLifecycleState
from app.agents.planning.metadata import PlanContext, PlanIdentity, PlanMetadata, PlanStatistics
from app.agents.planning.resources import ResourceRequirement
from app.agents.planning.risk import PlanRiskAssessment
from app.agents.planning.snapshots import PlanSnapshot


class Plan(BaseModel):
    """
    Canonical strongly typed Plan Aggregate Domain Model.
    Consumed by Executors, Workflow Engines, Observers, Reflection Engines, and Multi-Agent Coordinators.
    """
    identity: PlanIdentity = Field(default_factory=PlanIdentity)
    name: str = Field(default="ExecutionPlan")
    lifecycle_state: PlanLifecycleState = Field(default=PlanLifecycleState.DRAFT)
    graph: PlanGraph = Field(default_factory=lambda: PlanGraph(graph_id=str(uuid4())))
    metadata: PlanMetadata = Field(default_factory=PlanMetadata)
    statistics: PlanStatistics = Field(default_factory=PlanStatistics)
    dependencies: List[Dependency] = Field(default_factory=list)
    constraints: List[PlanConstraint] = Field(default_factory=list)
    resource_requirements: List[ResourceRequirement] = Field(default_factory=list)
    risk_assessment: PlanRiskAssessment = Field(default_factory=PlanRiskAssessment)
    snapshot: Optional[PlanSnapshot] = Field(default=None)

    model_config = {"frozen": True}


class PlanReference(BaseModel):
    """Lightweight pointer reference to a Plan aggregate."""
    plan_id: UUID
    version: str = Field(default="v1.0")
    lifecycle_state: PlanLifecycleState = Field(default=PlanLifecycleState.DRAFT)
    model_config = {"frozen": True}


class PlanningRequest(BaseModel):
    """Request payload to generate, optimize, or evaluate a plan."""
    goal_description: str
    context: PlanContext = Field(default_factory=PlanContext)
    constraints: List[PlanConstraint] = Field(default_factory=list)
    model_config = {"frozen": True}


class PlanningResult(BaseModel):
    """Result payload emitted upon plan generation or validation."""
    success: bool = Field(default=True)
    plan: Optional[Plan] = Field(default=None)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}


class PlanningSession(BaseModel):
    """Interactive planning session boundary object."""
    session_id: UUID = Field(default_factory=uuid4)
    active_plan_id: Optional[UUID] = Field(default=None)
    plan_history: List[PlanReference] = Field(default_factory=list)
    model_config = {"frozen": True}
