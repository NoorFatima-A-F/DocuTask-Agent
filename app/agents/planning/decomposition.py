"""
Goal Decomposition Models.
Defines GoalDecomposition and DecompositionStrategy.
"""

from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from app.agents.planning.goals import PlanGoal
from app.agents.planning.tasks import PlanningTask


class DecompositionStrategy(str, Enum):
    HIERARCHICAL = "HIERARCHICAL"
    SEQUENTIAL = "SEQUENTIAL"
    PARALLEL = "PARALLEL"
    CAPABILITY_DRIVEN = "CAPABILITY_DRIVEN"


class GoalDecomposition(BaseModel):
    """Decomposition result mapping a Goal into subgoals and executable PlanningTasks."""
    goal: PlanGoal
    subgoals: List[PlanGoal] = Field(default_factory=list)
    tasks: List[PlanningTask] = Field(default_factory=list)
    strategy: DecompositionStrategy = Field(default=DecompositionStrategy.HIERARCHICAL)
    model_config = {"frozen": True}
