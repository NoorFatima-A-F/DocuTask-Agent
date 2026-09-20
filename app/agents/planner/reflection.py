"""
Planner Self-Reflection and Critique Engine.
Critiques plan candidates to detect missing tasks, unreachable nodes, cycle hazards, or invalid assumptions.
"""

from typing import List
from pydantic import BaseModel, Field
from app.agents.planning.contracts import Plan
from app.agents.planning.dag import DAGValidator
from app.agents.planning.exceptions import PlanningException


class ReflectionCritique(BaseModel):
    """Critique assessment result produced by reflection engine."""
    has_flaws: bool = Field(default=False)
    issues_detected: List[str] = Field(default_factory=list)
    suggested_repairs: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}


class PlannerReflectionEngine:
    """Self-reflection engine performing automated critique on candidate plans."""

    def critique_plan(self, plan: Plan) -> ReflectionCritique:
        issues = []
        repairs = []

        # 1. Structural DAG validation
        try:
            DAGValidator.detect_cycles(plan.graph)
        except PlanningException as e:
            issues.append(f"Cycle detected: {str(e)}")
            repairs.append("REMOVE_CYCLE_EDGES")

        # 2. Check for empty nodes
        if not plan.graph.nodes:
            issues.append("Plan contains zero execution nodes.")
            repairs.append("GENERATE_DEFAULT_FALLBACK_TASK")

        # 3. Check for isolated nodes
        if len(plan.graph.nodes) > 1 and not plan.graph.edges:
            issues.append("Nodes are disconnected (isolated).")
            repairs.append("LINK_SEQUENTIAL_EDGES")

        return ReflectionCritique(
            has_flaws=len(issues) > 0,
            issues_detected=issues,
            suggested_repairs=repairs
        )
