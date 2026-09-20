"""
Strategy Simulation Engine for Phase 13.11 (ASC-GEEIP).
Simulates Quarterly and Annual Strategic Scenarios, Budget Rebalancing, and Scalability Stress Tests.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.strategy.events.strategy_events import (
    StrategicHorizon,
    StrategySimulationStarted,
    StrategySimulationCompleted,
)


@dataclass
class StrategicScenario:
    scenario_id: str = field(default_factory=lambda: f"scen-{uuid.uuid4().hex[:6]}")
    name: str = "Quarterly High-Load Surge Scenario"
    horizon: StrategicHorizon = StrategicHorizon.DAYS_90
    budget_delta_usd: float = 5000.0
    worker_scale_delta: int = 8
    cache_hit_rate_pct: float = 85.0
    traffic_growth_pct: float = 150.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "name": self.name,
            "horizon": self.horizon.value if hasattr(self.horizon, "value") else str(self.horizon),
            "budget_delta_usd": self.budget_delta_usd,
            "worker_scale_delta": self.worker_scale_delta,
            "cache_hit_rate_pct": self.cache_hit_rate_pct,
            "traffic_growth_pct": self.traffic_growth_pct,
        }


@dataclass
class StrategySimulation:
    simulation_id: str = field(default_factory=lambda: f"sim-{uuid.uuid4().hex[:8]}")
    scenario: StrategicScenario = field(default_factory=StrategicScenario)
    expected_roi_multiplier: float = 3.65
    expected_p95_latency_ms: float = 215.0
    expected_throughput_qps: float = 2450.0
    risk_score: float = 0.08
    recommended_actions: List[str] = field(default_factory=list)
    simulated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "simulation_id": self.simulation_id,
            "scenario": self.scenario.to_dict(),
            "expected_roi_multiplier": round(self.expected_roi_multiplier, 4),
            "expected_p95_latency_ms": round(self.expected_p95_latency_ms, 2),
            "expected_throughput_qps": round(self.expected_throughput_qps, 2),
            "risk_score": round(self.risk_score, 4),
            "recommended_actions": self.recommended_actions,
            "simulated_at": self.simulated_at,
        }


class StrategicSimulationEngine:
    """
    Simulates prospective strategic scenarios over multi-horizon timeframes.
    """

    def __init__(self) -> None:
        self.simulations: Dict[str, StrategySimulation] = {}
        self.event_log: List[Any] = []
        self._initialize_bootstrap_simulations()

    def _initialize_bootstrap_simulations(self) -> None:
        # Simulation 1: 3x Traffic Surge + Auto-Scaling
        scen1 = StrategicScenario(
            scenario_id="scen-surge-3x",
            name="Q4 Year-End 300% Invoicing Peak Surge",
            horizon=StrategicHorizon.DAYS_90,
            budget_delta_usd=6000.0,
            worker_scale_delta=12,
            cache_hit_rate_pct=88.0,
            traffic_growth_pct=300.0,
        )
        sim1 = StrategySimulation(
            simulation_id="sim-surge-3x-opt",
            scenario=scen1,
            expected_roi_multiplier=4.20,
            expected_p95_latency_ms=195.0,
            expected_throughput_qps=3200.0,
            risk_score=0.065,
            recommended_actions=[
                "Deploy +12 pre-warmed worker replicas across AWS us-east-1 and us-west-2.",
                "Activate aggressive 88% speculative tensor caching on corporate schemas.",
                "Enable triadic agent coalitions on balance sheet queue.",
            ],
        )
        self.simulations[sim1.simulation_id] = sim1

        # Simulation 2: Budget Tightening Scenario
        scen2 = StrategicScenario(
            scenario_id="scen-budget-cut-20",
            name="Operational Efficiency & -20% Cost Constraint",
            horizon=StrategicHorizon.DAYS_180,
            budget_delta_usd=-4000.0,
            worker_scale_delta=-2,
            cache_hit_rate_pct=92.0,
            traffic_growth_pct=50.0,
        )
        sim2 = StrategySimulation(
            simulation_id="sim-budget-cut-opt",
            scenario=scen2,
            expected_roi_multiplier=3.10,
            expected_p95_latency_ms=260.0,
            expected_throughput_qps=1800.0,
            risk_score=0.120,
            recommended_actions=[
                "Maximize lock-free memory ring buffer cache utilization to 92%.",
                "Consolidate idle night-time worker nodes into spot instances.",
            ],
        )
        self.simulations[sim2.simulation_id] = sim2

    def run_simulation(
        self,
        name: str,
        horizon: StrategicHorizon,
        budget_delta_usd: float = 0.0,
        worker_scale_delta: int = 4,
        cache_hit_rate_pct: float = 80.0,
        traffic_growth_pct: float = 100.0,
    ) -> StrategySimulation:
        scenario = StrategicScenario(
            name=name,
            horizon=horizon,
            budget_delta_usd=budget_delta_usd,
            worker_scale_delta=worker_scale_delta,
            cache_hit_rate_pct=cache_hit_rate_pct,
            traffic_growth_pct=traffic_growth_pct,
        )

        event_start = StrategySimulationStarted(
            simulation_id=f"sim-temp",
            horizon=horizon,
            scenario_type=name,
        )
        self.event_log.append(event_start)

        # Calculate projected metrics
        base_latency = 280.0
        latency_reduction = (worker_scale_delta * 6.5) + (cache_hit_rate_pct * 0.8)
        p95_latency = max(95.0, base_latency - latency_reduction)

        base_throughput = 1000.0
        throughput = base_throughput * (1.0 + (traffic_growth_pct / 100.0) * 0.7) + (worker_scale_delta * 120.0)

        roi = max(1.2, 2.5 + (cache_hit_rate_pct / 40.0) - (budget_delta_usd / 20000.0))
        risk = max(0.02, min(0.40, (traffic_growth_pct / 1000.0) - (worker_scale_delta * 0.015)))

        actions = [
            f"Allocate ${abs(budget_delta_usd):.0f} adjustment for {horizon.value} operational plan.",
            f"Adjust worker pool by {worker_scale_delta:+d} instances.",
            f"Maintain cache hit rate above {cache_hit_rate_pct:.0f}%.",
        ]

        sim = StrategySimulation(
            scenario=scenario,
            expected_roi_multiplier=roi,
            expected_p95_latency_ms=p95_latency,
            expected_throughput_qps=throughput,
            risk_score=risk,
            recommended_actions=actions,
        )
        self.simulations[sim.simulation_id] = sim

        event_end = StrategySimulationCompleted(
            simulation_id=sim.simulation_id,
            expected_roi_multiplier=sim.expected_roi_multiplier,
            risk_score=sim.risk_score,
        )
        self.event_log.append(event_end)

        return sim

    def list_simulations(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self.simulations.values()]

    def get_simulation(self, simulation_id: str) -> Optional[Dict[str, Any]]:
        s = self.simulations.get(simulation_id)
        return s.to_dict() if s else None
