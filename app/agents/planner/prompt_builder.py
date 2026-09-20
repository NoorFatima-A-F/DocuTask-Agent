"""
Planning Prompt Builder.
"""

from app.agents.planner.context import PlannerRequest
from app.agents.planner.prompt_templates import PLANNING_SYSTEM_PROMPT, TASK_DECOMPOSITION_PROMPT


class PlanningPromptBuilder:
    """Constructs structured LLM prompts for plan decomposition and candidate generation."""

    def build_decomposition_prompt(self, request: PlannerRequest) -> str:
        return TASK_DECOMPOSITION_PROMPT.format(
            goal_name=request.goal.name,
            goal_description=request.goal.description,
            budget_usd=request.context.planning_budget_usd
        )

    def build_system_prompt(self) -> str:
        return PLANNING_SYSTEM_PROMPT
