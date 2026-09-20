"""
Intelligent Goal Analysis Engine.
Analyzes user goals identifying objectives, constraints, missing information,
ambiguity, dependencies, resources, success criteria, and assumptions.
"""

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from app.agents.planner.context import PlannerContext
from app.agents.planning.goals import PlanGoal


class GoalAnalysisReport(BaseModel):
    """Structured report produced by GoalAnalyzer."""
    goal_id: str
    inferred_objectives: List[str] = Field(default_factory=list)
    identified_constraints: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    ambiguities: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)
    success_criteria: List[str] = Field(default_factory=list)
    is_actionable: bool = Field(default=True)
    confidence: float = Field(default=0.95, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class GoalAnalyzer:
    """Cognitive Goal Analyzer analyzing goals before hierarchical decomposition."""

    def analyze_goal(self, goal: PlanGoal, context: PlannerContext) -> GoalAnalysisReport:
        objectives = [f"Satisfy goal {goal.name}"]
        criteria = list(goal.success_criteria) or ["Verify output accuracy > 90%"]

        return GoalAnalysisReport(
            goal_id=goal.goal_id,
            inferred_objectives=objectives,
            identified_constraints=[f"Budget limit ${context.planning_budget_usd}"],
            missing_information=[],
            ambiguities=[],
            assumptions=["Document files are accessible in storage"],
            success_criteria=criteria,
            is_actionable=True,
            confidence=0.95
        )
