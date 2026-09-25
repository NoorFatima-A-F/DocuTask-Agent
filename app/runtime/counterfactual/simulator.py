"""
Counterfactual Simulator - High-level simulator facade.
Coordinates scenario generation, candidate branch generation, and differential evaluation.
"""

from typing import Dict, List, Any
from app.runtime.counterfactual.scenario_generator import ScenarioGenerator
from app.runtime.counterfactual.alternate_planner import AlternatePlanner
from app.runtime.counterfactual.comparison_engine import CounterfactualComparisonEngine
from app.runtime.counterfactual.replay_optimizer import CounterfactualReplayOptimizer


class CounterfactualSimulator:
    """Enterprise Counterfactual & Scenario Replay Simulator."""

    def __init__(self):
        self.scenario_gen = ScenarioGenerator()
        self.alt_planner = AlternatePlanner()
        self.comp_engine = CounterfactualComparisonEngine()
        self.replay_optimizer = CounterfactualReplayOptimizer()

    def get_available_scenarios(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self.scenario_gen.list_scenarios()]

    def simulate_decision_branches(
        self,
        factual_model: str,
        factual_accuracy: float,
        factual_latency_ms: float,
        factual_cost_usd: float,
        factual_utility: float,
    ) -> Dict[str, Any]:
        candidates = self.alt_planner.generate_alternatives(
            factual_model=factual_model,
            factual_accuracy=factual_accuracy,
            factual_latency_ms=factual_latency_ms,
            factual_cost_usd=factual_cost_usd,
            factual_utility=factual_utility,
        )
        differentials = [
            self.comp_engine.compare_branch(
                factual_model=factual_model,
                factual_acc=factual_accuracy,
                factual_lat_ms=factual_latency_ms,
                factual_cost_usd=factual_cost_usd,
                factual_u=factual_utility,
                candidate=c,
            ).to_dict()
            for c in candidates
        ]
        return {
            "factual_model": factual_model,
            "factual_utility": factual_utility,
            "candidates": [c.to_dict() for c in candidates],
            "differentials": differentials,
        }

    def run_replay(
        self,
        mission_id: str,
        factual_model: str = "gemini-2.5-flash",
        factual_accuracy: float = 0.962,
        factual_latency_ms: float = 480.0,
        factual_cost_usd: float = 0.0018,
        factual_utility: float = 0.884,
        scenario_id: str = "sc_nominal",
    ) -> Dict[str, Any]:
        return self.replay_optimizer.replay_mission(
            mission_id=mission_id,
            factual_model=factual_model,
            factual_accuracy=factual_accuracy,
            factual_latency_ms=factual_latency_ms,
            factual_cost_usd=factual_cost_usd,
            factual_utility=factual_utility,
            scenario_id=scenario_id,
        ).to_dict()
