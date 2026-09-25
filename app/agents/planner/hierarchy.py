"""
Decomposition Hierarchy and Abstraction Level Models.
"""

from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from app.agents.planning.goals import PlanGoal
from app.agents.planning.tasks import PlanningTask


class AbstractionLevel(str, Enum):
    STRATEGIC_GOAL = "STRATEGIC_GOAL"
    OBJECTIVE = "OBJECTIVE"
    MILESTONE = "MILESTONE"
    TASK = "TASK"
    ATOMIC_TASK = "ATOMIC_TASK"


class DecompositionNode(BaseModel):
    """Node within a hierarchical task decomposition tree."""
    node_id: str
    name: str
    level: AbstractionLevel = Field(default=AbstractionLevel.TASK)
    parent_id: Optional[str] = Field(default=None)
    children_ids: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}


class DecompositionTree(BaseModel):
    """Hierarchical tree mapping root goal down to atomic tasks."""
    root_goal: PlanGoal
    nodes: Dict[str, DecompositionNode] = Field(default_factory=dict)
    atomic_tasks: List[PlanningTask] = Field(default_factory=list)
    model_config = {"frozen": True}
