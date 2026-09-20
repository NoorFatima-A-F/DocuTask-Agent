"""
Plan Validation Engine.
Defines GraphValidationResult and PlanValidator.
"""

from typing import List
from pydantic import BaseModel, Field
from app.agents.planning.contracts import Plan
from app.agents.planning.dag import DAGValidator
from app.agents.planning.exceptions import PlanningException
from app.agents.planning.interfaces import IPlanValidator


class GraphValidationResult(BaseModel):
    """Validation report containing error list and validity flag."""
    is_valid: bool = Field(default=True)
    errors: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}


class PlanValidator(IPlanValidator):
    """Validator inspecting plan graph structure, constraints, and dependencies."""

    def validate_plan(self, plan: Plan) -> List[str]:
        errors: List[str] = []

        # 1. Check graph has at least one node if not draft
        if not plan.graph.nodes:
            errors.append("Plan graph contains no execution nodes.")

        # 2. Check DAG acyclicity
        try:
            DAGValidator.detect_cycles(plan.graph)
        except PlanningException as e:
            errors.append(str(e))

        return errors

    def validate_and_report(self, plan: Plan) -> GraphValidationResult:
        errors = self.validate_plan(plan)
        return GraphValidationResult(
            is_valid=len(errors) == 0,
            errors=errors
        )
