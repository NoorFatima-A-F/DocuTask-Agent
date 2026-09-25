"""
Constraint Resolver Engine.
Maps operational policies and user limits into PlanConstraint models.
"""

from typing import List
from app.agents.planner.context import PlannerContext
from app.agents.planning.constraints import ConstraintType, PlanConstraint


class ConstraintResolver:
    """Resolves and binds plan constraints from planning context."""

    def resolve_constraints(self, context: PlannerContext) -> List[PlanConstraint]:
        constraints = [
            PlanConstraint(
                constraint_id="const_budget",
                constraint_type=ConstraintType.BUDGET,
                limit_value=context.planning_budget_usd
            )
        ]
        return constraints
