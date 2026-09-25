"""
Risk Optimizer for Autonomous Plan Optimization Engine.
Identifies execution vulnerability points, enforces verification gates,
assigns secondary fallback policies, and mitigates regulatory risk.
"""

from __future__ import annotations

import copy
import logging
from typing import List, Tuple

from app.agents.planning.execution_plan import ExecutionPlan, FallbackStrategy, PlannedTask

logger = logging.getLogger(__name__)


class RiskOptimizer:
    """Hardens ExecutionPlan against failure, data loss, and compliance violations."""

    def estimate_plan_risk(self, plan: ExecutionPlan) -> float:
        """
        Calculates composite risk score in [0.0, 1.0].
        Lower is safer.
        """
        if not plan.tasks:
            return 0.0

        risk_points = 0.0
        max_possible = len(plan.tasks) * 3.0

        for task in plan.tasks:
            # 1. Missing fallback agent/tools on critical tasks
            if task.is_critical and not task.fallback_agent and not task.fallback_tools:
                risk_points += 1.0
            # 2. Critical tasks without verification steps
            if task.is_critical and not any("validate" in t.action.lower() for t in plan.tasks if task.task_id in t.dependencies):
                risk_points += 1.0
            # 3. High-risk actions (e.g. payout, delete, external transmit) without human gate
            if any(term in task.action.lower() for term in ["payout", "wire", "delete", "export_phi"]):
                if not any("human" in t.action.lower() or "approve" in t.action.lower() for t in plan.tasks):
                    risk_points += 1.0

        return min(1.0, risk_points / max_possible if max_possible > 0 else 0.0)

    def optimize(self, plan: ExecutionPlan) -> Tuple[ExecutionPlan, float]:
        """
        Hardens plan by injecting validation nodes and fallbacks where risk is elevated.
        Returns (hardened_plan, risk_reduction_percentage).
        """
        hardened = copy.deepcopy(plan)
        initial_risk = self.estimate_plan_risk(plan)

        new_tasks: List[PlannedTask] = []
        injected_count = 0

        for task in hardened.tasks:
            new_tasks.append(task)
            
            # Ensure fallback strategy exists for all critical tasks
            if task.is_critical and not task.fallback_agent:
                task.fallback_agent = "SecondaryRecoveryAgent"
                task.fallback_tools = ["fallback_heuristic_parser"]
                hardened.fallback_strategies[task.task_id] = FallbackStrategy(
                    task_id=task.task_id,
                    fallback_action="SWITCH_TOOL",
                    alternative_agent="SecondaryRecoveryAgent",
                    alternative_tools=["fallback_heuristic_parser"],
                )

            # If task performs high-value extraction, inject validation gate
            if "extract" in task.action.lower() and task.is_critical:
                val_id = f"val_{task.task_id}"
                if not any(t.task_id == val_id for t in hardened.tasks):
                    validation_task = PlannedTask(
                        task_id=val_id,
                        name=f"Validate {task.name}",
                        action="validate_extraction",
                        assigned_agent="ComplianceValidationAgent",
                        required_tools=["rule_validator"],
                        dependencies=[task.task_id],
                        is_critical=True,
                    )
                    new_tasks.append(validation_task)
                    injected_count += 1

        hardened.tasks = new_tasks
        final_risk = self.estimate_plan_risk(hardened)
        reduction = (initial_risk - final_risk) / initial_risk if initial_risk > 0 else 0.0
        logger.info("RiskOptimizer: Injected %d validation gates. Risk reduced by %.1f%%", injected_count, reduction * 100)
        return hardened, max(0.0, reduction)
