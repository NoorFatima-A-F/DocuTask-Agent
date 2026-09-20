"""
Phase 13.14 - Autonomous Organization Runtime Master Coordinator
Orchestrates the complete continuous organizational loop:
Mission -> Strategy -> Organization Design -> Workforce Allocation -> Project Execution -> Simulation -> Governance -> Measurement -> Learning.
"""

from __future__ import annotations
import time
import uuid
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from app.runtime.organization.events.organization_events import (
    AgentRole,
    OrganizationState,
    LearningCycleCompleted,
    OrganizationEvolutionTriggered,
    org_event_bus,
)
from app.runtime.organization.mission.mission_engine import mission_engine
from app.runtime.organization.strategy.organization_strategy_engine import organization_strategy_engine
from app.runtime.organization.organization.organization_engine import organization_engine
from app.runtime.organization.workforce.workforce_engine import workforce_engine
from app.runtime.organization.project.project_engine import project_engine
from app.runtime.organization.resource.resource_engine import resource_engine
from app.runtime.organization.performance.performance_engine import performance_engine
from app.runtime.organization.finance.finance_engine import finance_engine
from app.runtime.organization.governance.governance_engine import governance_engine
from app.runtime.organization.simulation.simulation_engine import organization_simulation_engine


class OrganizationCycleSummary(BaseModel):
    cycle_id: str = Field(default_factory=lambda: f"org_cyc_{uuid.uuid4().hex[:8]}")
    mission_id: str
    strategy_id: str
    org_id: str
    project_id: str
    governance_review_id: str
    simulation_report_id: str
    composite_health_score: float = 0.98
    roi_multiplier: float = 4.2
    status: str = "COMPLETED"
    duration_ms: float = 145.0
    completed_at: float = Field(default_factory=time.time)


class OrganizationRuntime:
    """Master controller orchestrating multi-agent enterprise cognition and mission execution."""

    def __init__(self) -> None:
        self._cycles: List[OrganizationCycleSummary] = []
        self._is_continuous_active: bool = True
        self._initialize_canonical_cycle()

    def _initialize_canonical_cycle(self) -> None:
        init_cycle = OrganizationCycleSummary(
            cycle_id="org_cyc_genesis_001",
            mission_id="msn_reduce_cost_40pct",
            strategy_id="strat_adaptive_quantization_001",
            org_id="org_enterprise_root",
            project_id="proj_cost_reduction_tier_router",
            governance_review_id="gov_rev_tier_router_rollout",
            simulation_report_id="sim_rep_baseline_stress_01",
            composite_health_score=0.98,
            roi_multiplier=4.2,
            status="COMPLETED",
            duration_ms=185.0,
        )
        self._cycles.append(init_cycle)

    def run_full_autonomous_cycle(
        self,
        mission_goal: str = "Reduce document processing cost by 40% while maintaining >=98% accuracy",
    ) -> OrganizationCycleSummary:
        """Executes an end-to-end organizational mission orchestration cycle."""
        start_t = time.time()

        # 1. Mission Decomposition
        mission = mission_engine.decompose_goal(mission_goal)
        mission_engine.validate_mission(mission.mission_id)

        # 2. Strategy Generation & Selection
        strategies = organization_strategy_engine.generate_strategies(mission.mission_id, count=3)
        optimal_strat = organization_strategy_engine.select_optimal_strategy(mission.mission_id)

        # 3. Organization Structure Design
        org = organization_engine.design_organization_for_mission(mission.mission_id, optimal_strat.strategy_id)

        # 4. Workforce Balancing
        workforce_engine.optimize_workforce_allocation()

        # 5. Project Formulation
        project = project_engine.create_project(
            mission_id=mission.mission_id,
            title=f"Execution Project for {mission.title[:35]}",
            description=f"Direct delivery project executing strategy: {optimal_strat.title}",
            task_specs=[
                {"title": "Subsystem Architecture Provisioning", "estimated_days": 3.0},
                {"title": "Worker Integration & Verification", "estimated_days": 4.0},
                {"title": "Production Shadow Testing", "estimated_days": 2.0},
            ],
        )

        # 6. Resource Optimization
        resource_engine.optimize_resources(prioritize_metric="COST_EFFICIENCY")

        # 7. Digital Twin Simulation
        sim_report = organization_simulation_engine.run_simulation(runs=50)

        # 8. Governance Review & Cryptographic Sealing
        gov_review = governance_engine.review_decision(
            decision_title=f"Execute Organization Plan for Mission {mission.mission_id}",
            proposing_role=AgentRole.CEO_AGENT,
            decision_payload={
                "mission_id": mission.mission_id,
                "strategy_id": optimal_strat.strategy_id,
                "org_id": org.org_id,
                "project_id": project.project_id,
                "sim_pass_rate": sim_report.success_rate,
            },
            simulation_verified=(sim_report.success_rate >= 0.85),
        )

        # 9. Performance & Financial Evaluation
        scorecard = performance_engine.generate_scorecard()
        finance_engine.compute_roi_projection()

        duration = (time.time() - start_t) * 1000.0

        summary = OrganizationCycleSummary(
            mission_id=mission.mission_id,
            strategy_id=optimal_strat.strategy_id,
            org_id=org.org_id,
            project_id=project.project_id,
            governance_review_id=gov_review.review_id,
            simulation_report_id=sim_report.report_id,
            composite_health_score=scorecard.composite_health_score,
            roi_multiplier=scorecard.overall_roi_multiplier,
            status="COMPLETED",
            duration_ms=round(duration, 2),
        )

        self._cycles.append(summary)

        org_event_bus.publish(
            LearningCycleCompleted(
                actor_agent_role=AgentRole.CEO_AGENT,
                payload={"cycle_id": summary.cycle_id, "roi": summary.roi_multiplier},
            )
        )

        org_event_bus.publish(
            OrganizationEvolutionTriggered(
                actor_agent_role=AgentRole.CEO_AGENT,
                payload={"cycle_id": summary.cycle_id, "generation": len(self._cycles)},
            )
        )

        return summary

    def get_overview(self) -> Dict[str, Any]:
        """Provides an executive overview aggregation across all organizational engines."""
        scorecard = performance_engine.generate_scorecard()
        finances = finance_engine.get_financial_summary()
        pool = resource_engine.get_pool_status()
        agents = workforce_engine.list_agents()
        missions = mission_engine.list_missions()
        projects = project_engine.list_projects()
        reviews = governance_engine.list_reviews()

        return {
            "organization_name": "DocuTask Autonomous Enterprise",
            "state": OrganizationState.EXECUTING,
            "composite_health_score": scorecard.composite_health_score,
            "overall_roi_multiplier": scorecard.overall_roi_multiplier,
            "monthly_burn_rate_usd": finances.total_monthly_burn_usd,
            "active_missions_count": len(missions),
            "active_projects_count": len(projects),
            "active_workforce_count": len(agents),
            "compute_utilization_pct": round(pool.utilization_rate * 100, 1),
            "governance_approval_rate": round(
                sum(1 for r in reviews if r.verdict.value == "APPROVED") / max(1, len(reviews)), 2
            ),
            "total_cycles_executed": len(self._cycles),
            "latest_cycle": self._cycles[-1].model_dump() if self._cycles else None,
        }

    def list_cycles(self) -> List[OrganizationCycleSummary]:
        return self._cycles


# Global Singleton
organization_runtime = OrganizationRuntime()


def get_organization_runtime() -> OrganizationRuntime:
    return organization_runtime
