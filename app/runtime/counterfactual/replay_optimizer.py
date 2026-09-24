"""
Counterfactual Simulator - Replay Optimizer
Replays historical missions under counterfactual constraints and optimization weights.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from app.runtime.counterfactual.scenario_generator import ScenarioGenerator
from app.runtime.counterfactual.alternate_planner import AlternatePlanner
from app.runtime.counterfactual.comparison_engine import CounterfactualComparisonEngine, CounterfactualDifferential


@dataclass
class ReplaySimulationResult:
    mission_id: str
    original_model: str
    scenario_applied: str
    evaluated_branches: List[Dict[str, Any]]
    differentials: List[Dict[str, Any]]
    best_counterfactual_branch: Optional[str]
    max_regret: float
    factual_decision_efficiency: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CounterfactualReplayOptimizer:
    """Optimizes and re-evaluates historical decision traces against counterfactual interventions."""

    def __init__(self):
        self.scenario_gen = ScenarioGenerator()
        self.alt_planner = AlternatePlanner()
        self.comp_engine = CounterfactualComparisonEngine()

    def replay_mission(
        self,
        mission_id: str,
        factual_model: str = "gemini-2.5-flash",
        factual_accuracy: float = 0.962,
        factual_latency_ms: float = 480.0,
        factual_cost_usd: float = 0.0018,
        factual_utility: float = 0.884,
        scenario_id: str = "sc_nominal",
    ) -> ReplaySimulationResult:
        scenarios = {s.scenario_id: s for s in self.scenario_gen.list_scenarios()}
        scenario = scenarios.get(scenario_id, scenarios["sc_nominal"])

        # Generate candidates
        candidates = self.alt_planner.generate_alternatives(
            factual_model=factual_model,
            factual_accuracy=factual_accuracy,
            factual_latency_ms=factual_latency_ms * scenario.latency_multiplier,
            factual_cost_usd=factual_cost_usd * scenario.cost_multiplier,
            factual_utility=factual_utility,
        )

        differentials: List[CounterfactualDifferential] = []
        max_regret = 0.0
        best_branch = None

        for c in candidates:
            diff = self.comp_engine.compare_branch(
                factual_model=factual_model,
                factual_acc=factual_accuracy,
                factual_lat_ms=factual_latency_ms,
                factual_cost_usd=factual_cost_usd,
                factual_u=factual_utility,
                candidate=c,
            )
            differentials.append(diff)
            # Regret = max(0, U(counterfactual) - U(factual))
            regret = max(0.0, c.simulated_utility - factual_utility)
            if regret > max_regret:
                max_regret = regret
                best_branch = c.branch_id

        # Efficiency = 1.0 - max_regret (bounded in [0, 1])
        efficiency = round(max(0.0, min(1.0, 1.0 - max_regret)), 4)

        return ReplaySimulationResult(
            mission_id=mission_id,
            original_model=factual_model,
            scenario_applied=scenario.name,
            evaluated_branches=[c.to_dict() for c in candidates],
            differentials=[d.to_dict() for d in differentials],
            best_counterfactual_branch=best_branch,
            max_regret=round(max_regret, 4),
            factual_decision_efficiency=efficiency,
        )
