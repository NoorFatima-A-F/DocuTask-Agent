"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Planning Engine.
Provides multi-strategy planning (Deterministic, AI, Constraint, Hybrid),
agent assignment, dependency resolution, constraint verification, and cost estimation.
"""

from __future__ import annotations

from typing import Dict, Optional
import logging

from app.agents.decomposition.task_decomposer import TaskDecomposer
from app.agents.domain.agent_entity import AgentPlan, GoalModel
from app.agents.registry.agent_registry import AgentRegistry

logger = logging.getLogger(__name__)


class PlanningError(Exception):
    """Raised when plan generation or validation fails."""
    pass


class PlanningEngine:
    """
    Cognitive Planning Engine responsible for orchestrating goal decomposition,
    agent assignment, constraint validation, and fallback planning.
    """

    def __init__(
        self,
        registry: Optional[AgentRegistry] = None,
        decomposer: Optional[TaskDecomposer] = None
    ):
        self.registry = registry or AgentRegistry()
        self.decomposer = decomposer or TaskDecomposer()

    def create_plan(
        self,
        goal: GoalModel,
        strategy: str = "HYBRID",
        template_name: Optional[str] = None,
        max_cost_limit: Optional[float] = None,
    ) -> AgentPlan:
        """
        Generates a validated AgentPlan for a given GoalModel using the specified strategy.
        Assigns capable agents to each step from the AgentRegistry.
        """
        # 1. Decompose goal into plan
        plan = self.decomposer.decompose(goal=goal, strategy=strategy, template_name=template_name)

        # 2. Match and assign specific agents from registry
        for step in plan.steps:
            # Find best agent matching required skills or agent type
            candidate = self.registry.find_best_agent(
                skill=step.required_skills[0] if step.required_skills else None,
                agent_type=step.assigned_agent_type,
            )
            if candidate:
                step.assigned_agent_type = candidate.name
                if candidate.name not in plan.assigned_agents:
                    plan.assigned_agents.append(candidate.name)

        # 3. Constraint checking
        cost_limit = max_cost_limit or goal.budget.get("max_cost_usd")
        if cost_limit and plan.estimated_cost_usd > cost_limit:
            msg = f"Plan estimated cost (${plan.estimated_cost_usd}) exceeds budget constraint (${cost_limit})"
            logger.warning(msg)
            # Re-adjust or flag plan risk
            plan.risk_score = min(1.0, plan.risk_score + 0.3)

        # 4. Dependency cycle verification
        self._verify_plan_dag(plan)

        logger.info(
            f"PlanningEngine generated plan {plan.plan_id} with {len(plan.steps)} steps "
            f"for goal '{goal.description}'"
        )
        return plan

    def _verify_plan_dag(self, plan: AgentPlan) -> None:
        """Verifies that plan step dependencies form an acyclic directed graph."""
        visited: Dict[str, int] = {}  # 0: unvisited, 1: visiting, 2: visited
        step_ids = {s.id for s in plan.steps}

        for sid in step_ids:
            visited[sid] = 0

        def dfs(node: str) -> bool:
            visited[node] = 1
            for dep in plan.dependencies.get(node, []):
                if dep not in visited:
                    continue
                if visited[dep] == 1:
                    return False  # Cycle detected
                if visited[dep] == 0:
                    if not dfs(dep):
                        return False
            visited[node] = 2
            return True

        for sid in step_ids:
            if visited[sid] == 0:
                if not dfs(sid):
                    raise PlanningError(f"Plan {plan.plan_id} contains a dependency cycle involving step {sid}")
