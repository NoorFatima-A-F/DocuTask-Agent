"""Autonomous Planning Engine for Enterprise Agent Operating System.

Translates GoalSpecifications into robust, optimized, resilient ExecutionPlans
with agent assignments, tool selection, fallback strategies, and verification gates.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from app.agents.intelligence.goal.goal_specification import GoalSpecification
from app.agents.planning.capability_discovery import CapabilityDiscovery
from app.agents.planning.execution_plan import (
    ExecutionPlan,
    FallbackStrategy,
    PlannedTask,
    TaskStatus,
)
from app.agents.planning.task_decomposer import TaskDecomposer

logger = logging.getLogger(__name__)


class AutonomousPlanner:
    """Autonomous Planning Engine creating fully specified ExecutionPlans."""

    def __init__(
        self,
        discovery: Optional[CapabilityDiscovery] = None,
        decomposer: Optional[TaskDecomposer] = None,
    ) -> None:
        self.discovery = discovery or CapabilityDiscovery()
        self.decomposer = decomposer or TaskDecomposer()

    def generate_plan(self, goal: GoalSpecification) -> ExecutionPlan:
        """Create a complete ExecutionPlan from a GoalSpecification."""
        tasks = self.decomposer.decompose(goal)
        plan = ExecutionPlan(goal_id=goal.goal_id)

        min_accuracy = goal.constraints.get("min_accuracy", 0.90)
        high_accuracy = min_accuracy >= 0.95

        total_cost = 0.0
        total_duration = 0.0

        for task in tasks:
            # 1. Match Agent
            agent = self.discovery.match_agent(task.action, goal.intent)
            if agent:
                task.assigned_agent = agent.agent_id
                total_cost += agent.cost_per_invocation
                total_duration += (agent.latency_ms_p95 / 1000.0)

            # 2. Match Tool
            tool = self.discovery.match_tool(
                action_type=task.action,
                modality="IMAGE" if "ocr" in task.action else "JSON",
                high_accuracy=high_accuracy,
            )
            if tool:
                task.required_tools = [tool.tool_id]
                total_cost += tool.cost_per_call
                total_duration += (tool.latency_ms / 1000.0)

            # 3. Setup Fallback Strategy
            if task.action == "ocr":
                # Primary OCR fallback to Vision LLM
                fallback_tool = "tool_gemini_vision"
                fallback_agent = "agent_correction_gemini"
                task.fallback_agent = fallback_agent
                task.fallback_tools = [fallback_tool]

                plan.fallback_strategies[task.task_id] = FallbackStrategy(
                    task_id=task.task_id,
                    fallback_action="SWITCH_TOOL",
                    alternative_agent=fallback_agent,
                    alternative_tools=[fallback_tool],
                    max_fallback_attempts=2,
                )
            elif task.action == "arithmetic_verification":
                # Math validation failure triggers reflection correction
                plan.fallback_strategies[task.task_id] = FallbackStrategy(
                    task_id=task.task_id,
                    fallback_action="RETRY_WITH_ALTERNATIVE_AGENT",
                    alternative_agent="agent_correction_gemini",
                    alternative_tools=["tool_json_validator"],
                    max_fallback_attempts=3,
                )

            plan.add_task(task)

        # 4. Topological Sort & Invariant Validation
        ordered_tasks = plan.get_topological_order()
        plan.tasks = ordered_tasks

        # 5. Verification Steps
        if goal.success_criteria:
            plan.verification_steps = [
                f"Verify {sc.metric_name} {sc.comparison_operator} {sc.target_value}"
                for sc in goal.success_criteria
            ]
        else:
            plan.verification_steps = [f"Verify {goal.intent} execution and schema consistency"]

        plan.estimated_cost_usd = round(total_cost, 4)
        plan.estimated_duration_seconds = round(total_duration, 2)
        plan.metadata = {
            "intent": goal.intent,
            "priority": goal.priority.value,
            "risk_level": goal.risk_level.value,
            "task_count": len(plan.tasks),
            "critical_task_count": sum(1 for t in plan.tasks if t.is_critical),
        }

        logger.info(
            "Generated Autonomous ExecutionPlan %s with %d tasks (Est: $%.4f, %.2fs)",
            plan.plan_id,
            len(plan.tasks),
            plan.estimated_cost_usd,
            plan.estimated_duration_seconds,
        )

        return plan
