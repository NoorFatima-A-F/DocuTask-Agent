"""Enterprise Goal Manager.

Coordinates goal lifecycle, registration, validation, and provides an API
for decomposing user objectives into active execution targets.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.agents.intelligence.goal.goal_parser import GoalParser
from app.agents.intelligence.goal.goal_specification import (
    GoalPriority,
    GoalSpecification,
    GoalStatus,
)

logger = logging.getLogger(__name__)


class GoalManager:
    """Manages creation, parsing, state, and evaluation of goals."""

    def __init__(self, parser: Optional[GoalParser] = None) -> None:
        self.parser = parser or GoalParser()
        self._goals: Dict[str, GoalSpecification] = {}

    def submit_goal(
        self,
        objective: str,
        context: Optional[Dict[str, Any]] = None,
        goal_id: Optional[str] = None,
    ) -> GoalSpecification:
        """Parse, validate, and register a new goal."""
        spec = self.parser.parse(objective=objective, context=context, goal_id=goal_id)

        if spec.is_ambiguous():
            logger.warning("Goal %s has low confidence or brief objective: %s", spec.goal_id, spec.objective)
            # Default to low risk or clarify
            spec.metadata["requires_clarification"] = True

        self._goals[spec.goal_id] = spec
        return spec

    def get_goal(self, goal_id: str) -> Optional[GoalSpecification]:
        return self._goals.get(goal_id)

    def list_goals(self, status: Optional[GoalStatus] = None) -> List[GoalSpecification]:
        if status:
            return [g for g in self._goals.values() if g.status == status]
        return list(self._goals.values())

    def update_status(self, goal_id: str, status: GoalStatus) -> bool:
        if goal_id in self._goals:
            self._goals[goal_id].status = status
            return True
        return False

    def evaluate_goal(self, goal_id: str, metrics: Dict[str, float]) -> tuple[bool, float]:
        goal = self.get_goal(goal_id)
        if not goal:
            raise KeyError(f"Goal {goal_id} not found")
        passed, score = goal.evaluate_success(metrics)
        if passed:
            goal.status = GoalStatus.COMPLETED
        else:
            goal.status = GoalStatus.FAILED
        return passed, score
