"""
Planning Workflow Domain Representation.
Defines WorkflowDefinition and execution branching topologies.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.agents.planning.branching import ConditionalBranch, ParallelBranch
from app.agents.planning.graph import PlanGraph


class WorkflowDefinition(BaseModel):
    """Workflow specification orchestrating plan graph execution flow."""
    workflow_id: str
    name: str
    graph: PlanGraph
    parallel_branches: List[ParallelBranch] = Field(default_factory=list)
    conditional_branches: List[ConditionalBranch] = Field(default_factory=list)
    timeout_seconds: float = Field(default=3600.0, gt=0.0)
    model_config = {"frozen": True}
