"""
Goal Normalizer Engine.
Normalizes raw goal text and user intents into canonical PlanGoal models.
"""

from typing import Optional
from app.agents.planning.goals import PlanGoal


class GoalNormalizer:
    """Normalizes raw input goals into canonical PlanGoal specifications."""

    def normalize(self, raw_text: str, goal_id: Optional[str] = None) -> PlanGoal:
        gid = goal_id or "GOAL_DEFAULT"
        clean_text = raw_text.strip()
        return PlanGoal(
            goal_id=gid,
            name=clean_text,
            description=clean_text,
            success_criteria=["Complete task execution without unhandled exceptions"]
        )
