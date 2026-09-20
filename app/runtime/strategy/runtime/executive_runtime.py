"""
Executive Strategy Runtime Coordinator for Phase 13.11 (ASC-GEEIP).
Master orchestration layer uniting all strategic cognition, goal evolution, and executive decisioning engines.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
from typing import Any, Dict, List, Optional

from app.runtime.strategy.events.strategy_events import (
    GoalPriority,
    GoalStatus,
    StrategicHorizon,
    DecisionImportance,
    MissionValue,
    StrategicExecutionStarted,
    StrategicExecutionCompleted,
)
from app.runtime.strategy.goal_engine.goal_engine import GoalEvolutionEngine
from app.runtime.strategy.portfolio.portfolio_engine import MissionPortfolioEngine
from app.runtime.strategy.roadmap.roadmap_engine import RoadmapEngine
from app.runtime.strategy.executive.executive_engine import ExecutiveReasoningEngine
from app.runtime.strategy.resource_negotiation.resource_negotiation import ResourceNegotiationEngine
from app.runtime.strategy.organizational_memory.organization_memory import OrganizationLearningEngine
from app.runtime.strategy.strategy_simulation.strategy_simulation import StrategicSimulationEngine
from app.runtime.strategy.decision_engine.decision_engine import DecisionEngine


class ExecutiveRuntime:
    """
    Master Chief Strategy Officer (CSO) Coordinator.
    """

    _instance: Optional["ExecutiveRuntime"] = None

    def __init__(self) -> None:
        self.goals: GoalEvolutionEngine = GoalEvolutionEngine()
        self.portfolio: MissionPortfolioEngine = MissionPortfolioEngine()
        self.roadmaps: RoadmapEngine = RoadmapEngine()
        self.executive: ExecutiveReasoningEngine = ExecutiveReasoningEngine()
        self.negotiation: ResourceNegotiationEngine = ResourceNegotiationEngine()
        self.memory: OrganizationLearningEngine = OrganizationLearningEngine()
        self.simulation: StrategicSimulationEngine = StrategicSimulationEngine()
        self.decision: DecisionEngine = DecisionEngine()
        self.event_log: List[Any] = []
        self.created_at: str = datetime.now(timezone.utc).isoformat()

    @classmethod
    def get_instance(cls) -> "ExecutiveRuntime":
        if cls._instance is None:
            cls._instance = ExecutiveRuntime()
        return cls._instance

    def get_overview(self) -> Dict[str, Any]:
        goals_summary = self.goals.list_goals()
        portfolio_summary = self.portfolio.get_portfolio()
        decisions_summary = self.executive.list_decisions()
        recommendations_summary = self.executive.list_recommendations()
        roadmaps_summary = self.roadmaps.list_roadmaps()

        total_active_goals = len([g for g in goals_summary if g.get("status") == "ACTIVE"])
        approved_decisions = len([d for d in decisions_summary if d.get("status") == "APPROVED"])
        knowledge_entries = len(self.memory.query_knowledge())

        return {
            "status": "OPERATIONAL",
            "runtime_type": "ASC-GEEIP (Phase 13.11)",
            "cso_agent_state": "ACTIVE",
            "active_goals_count": total_active_goals,
            "portfolio_budget_utilization_pct": portfolio_summary.get("budget_utilization_pct", 0.0),
            "portfolio_overall_risk_index": portfolio_summary.get("overall_risk_index", 0.0),
            "approved_strategic_decisions": approved_decisions,
            "total_recommendations": len(recommendations_summary),
            "roadmaps_active": len(roadmaps_summary),
            "institutional_memory_entries": knowledge_entries,
            "created_at": self.created_at,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

    def execute_strategic_cycle(self) -> Dict[str, Any]:
        """
        Executes an end-to-end strategic review cycle:
        1. Evolves and reprioritizes goals.
        2. Optimizes mission portfolio Pareto balance.
        3. Generates executive investment recommendations.
        """
        exec_id = f"strat-exec-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        self.event_log.append(
            StrategicExecutionStarted(
                execution_id=exec_id,
                roadmap_id="rdmp-90d-quarterly",
            )
        )

        goal_evolution_result = self.goals.evolve_generation()
        portfolio_result = self.portfolio.optimize_portfolio()

        # Produce executive recommendation based on highest utility goal
        active_goals = [g for g in self.goals.tree.all_goals.values() if g.status == GoalStatus.ACTIVE]
        top_goal = max(active_goals, key=lambda g: g.utility_score) if active_goals else None

        if top_goal:
            self.executive.generate_recommendation(
                target_area=top_goal.title,
                allocated_budget_usd=top_goal.estimated_cost_usd,
                expected_gain_pct=top_goal.expected_latency_reduction_pct,
                strategic_rationale=f"Highest utility goal ({top_goal.utility_score:.3f}): {top_goal.description}",
                risk_level="LOW" if top_goal.utility_score > 0.85 else "MEDIUM",
                confidence=top_goal.confidence,
            )

        self.event_log.append(
            StrategicExecutionCompleted(
                execution_id=exec_id,
                status="SUCCESS",
            )
        )

        return {
            "execution_id": exec_id,
            "goal_evolution": goal_evolution_result,
            "portfolio_optimization": portfolio_result,
            "top_recommended_goal": top_goal.to_dict() if top_goal else None,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
