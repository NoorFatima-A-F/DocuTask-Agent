"""
Phase 13.14 - Autonomous Strategy Generation Engine
Synthesizes executable organizational strategy plans from decomposed missions using Monte Carlo utility and risk analysis.
"""

from __future__ import annotations
import time
import uuid
import random
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from app.runtime.organization.events.organization_events import (
    AgentRole,
    DecisionConfidence,
    StrategyGenerated,
    StrategyUpdated,
    org_event_bus,
)
from app.runtime.organization.mission.mission_engine import mission_engine


class StrategyAction(BaseModel):
    action_id: str = Field(default_factory=lambda: f"act_{uuid.uuid4().hex[:8]}")
    title: str
    target_department: str
    required_roles: List[AgentRole] = Field(default_factory=list)
    estimated_cost_usd: float = 1200.0
    expected_utility: float = 0.85
    timeline_weeks: int = 4
    status: str = "PLANNED"  # PLANNED, IN_PROGRESS, EXECUTED, BLOCKED


class StrategyRisk(BaseModel):
    risk_id: str = Field(default_factory=lambda: f"rsk_{uuid.uuid4().hex[:8]}")
    description: str
    severity: str = "MEDIUM"  # LOW, MEDIUM, HIGH, CRITICAL
    probability: float = 0.25
    mitigation_strategy: str


class StrategyPlan(BaseModel):
    strategy_id: str = Field(default_factory=lambda: f"strat_{uuid.uuid4().hex[:8]}")
    mission_id: str
    title: str
    rationale: str
    objectives: List[str] = Field(default_factory=list)
    actions: List[StrategyAction] = Field(default_factory=list)
    required_agent_roles: List[AgentRole] = Field(default_factory=list)
    timeline_weeks: int = 12
    expected_roi_multiplier: float = 3.5
    total_estimated_cost_usd: float = 8500.0
    risk_score: float = 0.22  # 0.0 to 1.0 (lower is better)
    confidence: DecisionConfidence = DecisionConfidence.HIGH
    fallback_strategy_id: Optional[str] = None
    simulation_pass_rate: float = 0.94
    is_selected: bool = False
    created_at: float = Field(default_factory=time.time)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class OrganizationStrategyEngine:
    """Generates and ranks multi-alternative enterprise strategies for active missions."""

    def __init__(self) -> None:
        self._strategies: Dict[str, StrategyPlan] = {}
        self._initialize_canonical_strategies()

    def _initialize_canonical_strategies(self) -> None:
        strat_a = StrategyPlan(
            strategy_id="strat_adaptive_quantization_001",
            mission_id="msn_reduce_cost_40pct",
            title="Aggressive Token Distillation & Dynamic Tier-Routing",
            rationale="Route 75% of routine document schemas to quantized Flash/Lite models, preserving Pro models strictly for complex unstructured clauses.",
            objectives=[
                "Deploy dynamic model router across all extraction workers",
                "Implement vector memory caching for recurring vendor invoices",
                "Establish automated quality audits with confidence thresholds",
            ],
            actions=[
                StrategyAction(
                    title="Implement Hybrid Tier Router",
                    target_department="Engineering",
                    required_roles=[AgentRole.CTO_AGENT, AgentRole.ENGINEERING_AGENT],
                    estimated_cost_usd=2800.0,
                    expected_utility=0.92,
                    timeline_weeks=3,
                ),
                StrategyAction(
                    title="Pre-compute Semantic OCR Cache",
                    target_department="Research",
                    required_roles=[AgentRole.RESEARCH_AGENT, AgentRole.ENGINEERING_AGENT],
                    estimated_cost_usd=2200.0,
                    expected_utility=0.88,
                    timeline_weeks=4,
                ),
                StrategyAction(
                    title="Continuous Accuracy & ROI Telemetry",
                    target_department="Analytics",
                    required_roles=[AgentRole.ANALYST_AGENT, AgentRole.FINANCE_AGENT],
                    estimated_cost_usd=1400.0,
                    expected_utility=0.90,
                    timeline_weeks=2,
                ),
            ],
            required_agent_roles=[
                AgentRole.CEO_AGENT,
                AgentRole.CTO_AGENT,
                AgentRole.RESEARCH_AGENT,
                AgentRole.ENGINEERING_AGENT,
                AgentRole.ANALYST_AGENT,
                AgentRole.FINANCE_AGENT,
            ],
            timeline_weeks=9,
            expected_roi_multiplier=4.2,
            total_estimated_cost_usd=6400.0,
            risk_score=0.18,
            confidence=DecisionConfidence.VERY_HIGH,
            simulation_pass_rate=0.96,
            is_selected=True,
        )

        strat_b = StrategyPlan(
            strategy_id="strat_batch_speculative_002",
            mission_id="msn_reduce_cost_40pct",
            title="Speculative Batch Execution & Multi-Tenant Scheduling",
            rationale="Aggregate low-priority incoming document queues into overnight speculative batches to exploit off-peak compute discounts.",
            objectives=[
                "Construct off-peak asynchronous execution queue",
                "Enforce tenant SLA deadlines with adaptive scheduling",
            ],
            actions=[
                StrategyAction(
                    title="Develop Asynchronous Batch Aggregator",
                    target_department="Engineering",
                    required_roles=[AgentRole.ENGINEERING_AGENT, AgentRole.OPERATIONS_AGENT],
                    estimated_cost_usd=3500.0,
                    expected_utility=0.81,
                    timeline_weeks=5,
                ),
            ],
            required_agent_roles=[AgentRole.ENGINEERING_AGENT, AgentRole.OPERATIONS_AGENT],
            timeline_weeks=10,
            expected_roi_multiplier=2.8,
            total_estimated_cost_usd=5200.0,
            risk_score=0.28,
            confidence=DecisionConfidence.MEDIUM,
            simulation_pass_rate=0.88,
            is_selected=False,
            fallback_strategy_id="strat_adaptive_quantization_001",
        )

        self._strategies[strat_a.strategy_id] = strat_a
        self._strategies[strat_b.strategy_id] = strat_b

    def generate_strategies(self, mission_id: str, count: int = 3) -> List[StrategyPlan]:
        """Synthesizes candidate strategy plans for a mission."""
        mission = mission_engine.get_mission(mission_id)
        goal_text = mission.raw_goal if mission else "Optimize platform operations"

        generated = []
        archetypes = [
            ("Accelerated Direct Execution", 1.2, 0.15, 3.8),
            ("Balanced Pareto Optimization", 1.0, 0.18, 4.4),
            ("Conservative Quality-First Migration", 0.8, 0.09, 2.9),
        ]

        for idx, (arch_name, cost_mult, risk_val, roi_val) in enumerate(archetypes[:count]):
            strat_id = f"strat_{uuid.uuid4().hex[:8]}"
            actions = [
                StrategyAction(
                    title=f"Phase 1: Architecture Alignment ({arch_name})",
                    target_department="Engineering",
                    required_roles=[AgentRole.CTO_AGENT, AgentRole.ENGINEERING_AGENT],
                    estimated_cost_usd=2000.0 * cost_mult,
                    expected_utility=0.88,
                    timeline_weeks=3,
                ),
                StrategyAction(
                    title=f"Phase 2: Execution Rollout & Validation",
                    target_department="Operations",
                    required_roles=[AgentRole.OPERATIONS_AGENT, AgentRole.ANALYST_AGENT],
                    estimated_cost_usd=2500.0 * cost_mult,
                    expected_utility=0.85,
                    timeline_weeks=4,
                ),
            ]

            plan = StrategyPlan(
                strategy_id=strat_id,
                mission_id=mission_id,
                title=f"{arch_name} Strategy for {goal_text[:40]}",
                rationale=f"Methodology calibrated around {arch_name.lower()} to satisfy mission criteria with calculated utility.",
                objectives=[f"Implement {arch_name.lower()} pipeline", "Meet operational SLA and cost constraints"],
                actions=actions,
                required_agent_roles=[AgentRole.CEO_AGENT, AgentRole.CTO_AGENT, AgentRole.ENGINEERING_AGENT, AgentRole.ANALYST_AGENT],
                timeline_weeks=int(8 * cost_mult),
                expected_roi_multiplier=roi_val,
                total_estimated_cost_usd=4500.0 * cost_mult,
                risk_score=risk_val,
                confidence=DecisionConfidence.HIGH if risk_val < 0.20 else DecisionConfidence.MEDIUM,
                simulation_pass_rate=round(1.0 - (risk_val * 0.5), 2),
                is_selected=(idx == 1),  # Default select balanced
            )

            self._strategies[plan.strategy_id] = plan
            generated.append(plan)

            org_event_bus.publish(
                StrategyGenerated(
                    actor_agent_role=AgentRole.CEO_AGENT,
                    payload={"strategy_id": plan.strategy_id, "mission_id": mission_id, "title": plan.title},
                )
            )

        return generated

    def evaluate_strategy_monte_carlo(self, strategy_id: str, iterations: int = 500) -> Dict[str, Any]:
        """Runs Monte Carlo simulations on strategy parameters to compute probability distributions."""
        strat = self._strategies.get(strategy_id)
        if not strat:
            return {"error": f"Strategy '{strategy_id}' not found"}

        success_count = 0
        roi_samples = []
        cost_samples = []

        base_roi = strat.expected_roi_multiplier
        base_cost = strat.total_estimated_cost_usd
        risk = strat.risk_score

        random.seed(42)
        for _ in range(iterations):
            # Stochastic perturbation
            cost_factor = random.gauss(1.0, risk * 0.5)
            roi_factor = random.gauss(1.0, risk * 0.4)
            sim_cost = max(100.0, base_cost * cost_factor)
            sim_roi = max(0.5, base_roi * roi_factor)

            if sim_roi >= 2.0 and sim_cost <= (base_cost * 1.35):
                success_count += 1
            roi_samples.append(sim_roi)
            cost_samples.append(sim_cost)

        p_success = success_count / iterations
        mean_roi = sum(roi_samples) / iterations
        mean_cost = sum(cost_samples) / iterations

        strat.simulation_pass_rate = round(p_success, 3)

        return {
            "strategy_id": strategy_id,
            "iterations": iterations,
            "probability_of_success": p_success,
            "mean_expected_roi": round(mean_roi, 2),
            "mean_expected_cost_usd": round(mean_cost, 2),
            "p95_worst_case_cost_usd": round(sorted(cost_samples)[int(iterations * 0.95)], 2),
            "confidence_band": "NARROW" if risk < 0.20 else "MODERATE",
            "verdict": "FEASIBLE" if p_success >= 0.85 else "HIGH_UNCERTAINTY",
        }

    def select_optimal_strategy(self, mission_id: str) -> StrategyPlan:
        """Selects the highest utility strategy for the given mission."""
        strats = [s for s in self._strategies.values() if s.mission_id == mission_id]
        if not strats:
            created = self.generate_strategies(mission_id, count=3)
            strats = created

        # Utility function = (ROI * PassRate) / (CostNorm * (1 + Risk))
        def utility_fn(s: StrategyPlan) -> float:
            cost_norm = max(1.0, s.total_estimated_cost_usd / 5000.0)
            return (s.expected_roi_multiplier * s.simulation_pass_rate) / (cost_norm * (1.0 + s.risk_score))

        best = max(strats, key=utility_fn)
        for s in strats:
            s.is_selected = (s.strategy_id == best.strategy_id)

        org_event_bus.publish(
            StrategyUpdated(
                actor_agent_role=AgentRole.CEO_AGENT,
                payload={"strategy_id": best.strategy_id, "mission_id": mission_id, "status": "SELECTED"},
            )
        )
        return best

    def list_strategies(self, mission_id: Optional[str] = None) -> List[StrategyPlan]:
        if mission_id:
            return [s for s in self._strategies.values() if s.mission_id == mission_id]
        return list(self._strategies.values())

    def get_strategy(self, strategy_id: str) -> Optional[StrategyPlan]:
        return self._strategies.get(strategy_id)


# Global Singleton
organization_strategy_engine = OrganizationStrategyEngine()
