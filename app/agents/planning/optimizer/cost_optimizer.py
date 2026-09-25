"""
Cost Optimizer for Autonomous Plan Optimization Engine.
Prunes redundant operations, substitutes expensive models with specialized extractors,
and calculates potential financial savings.
"""

from __future__ import annotations

import copy
import logging
from typing import Dict, List, Set, Tuple

from app.agents.planning.execution_plan import ExecutionPlan, PlannedTask

logger = logging.getLogger(__name__)

# Estimated cost table in USD per execution
ESTIMATED_TOOL_COSTS: Dict[str, float] = {
    "gemini_vision": 0.005,
    "claude_opus": 0.015,
    "gpt4o": 0.010,
    "tesseract_ocr": 0.0001,
    "pdf_plumber": 0.00005,
    "regex_extractor": 0.00001,
    "rule_validator": 0.00001,
}


class CostOptimizer:
    """Optimizes ExecutionPlan for minimum monetary and token cost."""

    def __init__(self, tool_costs: Dict[str, float] = None) -> None:
        self.tool_costs = tool_costs or ESTIMATED_TOOL_COSTS

    def estimate_plan_cost(self, plan: ExecutionPlan) -> float:
        """Calculates total estimated cost in USD for the entire plan."""
        total = 0.0
        for task in plan.tasks:
            for tool in task.required_tools:
                total += self.tool_costs.get(tool.lower(), 0.001)
        return round(total, 6)

    def optimize(self, plan: ExecutionPlan) -> Tuple[ExecutionPlan, float]:
        """
        Creates a cost-optimized variant of the plan by:
        1. Substituting expensive general vision LLMs with local OCR where high-confidence digital text exists.
        2. Deduplicating redundant validation passes.
        Returns (optimized_plan, cost_savings_percentage).
        """
        optimized = copy.deepcopy(plan)
        initial_cost = self.estimate_plan_cost(plan)

        # 1. Substitute expensive tools if lightweight alternatives exist
        for task in optimized.tasks:
            new_tools = []
            for tool in task.required_tools:
                if tool == "gemini_vision" and task.metadata.get("is_digital_pdf", False):
                    new_tools.append("pdf_plumber")
                    logger.debug("CostOptimizer: Substituted gemini_vision with pdf_plumber for task %s", task.task_id)
                elif tool == "claude_opus" and not task.is_critical:
                    new_tools.append("regex_extractor")
                else:
                    new_tools.append(tool)
            task.required_tools = new_tools

        # 2. Prune duplicate validation steps
        seen_actions: Set[str] = set()
        pruned_tasks: List[PlannedTask] = []
        for task in optimized.tasks:
            action_key = f"{task.action}_{task.assigned_agent}"
            if "validate" in task.action.lower() and action_key in seen_actions and not task.is_critical:
                logger.info("CostOptimizer: Pruned redundant non-critical validation task %s", task.task_id)
                continue
            seen_actions.add(action_key)
            pruned_tasks.append(task)
        optimized.tasks = pruned_tasks

        final_cost = self.estimate_plan_cost(optimized)
        savings = (initial_cost - final_cost) / initial_cost if initial_cost > 0 else 0.0
        return optimized, max(0.0, savings)
