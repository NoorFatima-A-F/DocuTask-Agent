"""Meta Planner Coordinator for DocuTask ADIP.

Orchestrates metacognitive reasoning, self-critique, dynamic parameter tuning,
regret calculation, and Multi-Armed Bandit policy exploration.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.runtime.events.event_bus import EventBus
from app.runtime.events.probabilistic_events import (
    MetaPlanningStartedEvent,
    PlannerCritiquedEvent,
    RegretComputedEvent,
    ExplorationTriggeredEvent,
)
from app.runtime.meta.regret import RegretEngine, RegretAnalysisResult
from app.runtime.meta.exploration import ExplorationEngine, ExplorationDecision
from app.runtime.meta.planner_critic import PlannerCritic, PlannerCritiqueReport
from app.runtime.meta.planner_optimizer import PlannerOptimizer, PlannerHyperparameters


class MetaPlanningReview(BaseModel):
    """Complete metacognitive evaluation package."""
    mission_id: str
    critique: PlannerCritiqueReport
    regret: RegretAnalysisResult
    exploration: ExplorationDecision
    optimized_params: PlannerHyperparameters
    meta_verdict: str = "ACCEPT_PLAN"


class MetaPlanner:
    """The metacognitive brain monitoring and tuning the autonomous planner."""

    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self.event_bus = event_bus or EventBus.get_instance()
        self.regret_engine = RegretEngine()
        self.exploration_engine = ExplorationEngine()
        self.critic = PlannerCritic()
        self.optimizer = PlannerOptimizer()

    def evaluate_and_supervise(
        self,
        mission_id: str,
        chosen_strategy_id: str,
        strategy_utilities: Dict[str, float],
        strategy_costs: Dict[str, float],
        estimated_risk: float = 0.06,
        confidence: float = 0.96,
        document_complexity: float = 1.0,
    ) -> MetaPlanningReview:
        # 1. Regret Analysis
        regret_res = self.regret_engine.compute_regret(
            mission_id=mission_id,
            chosen_strategy_id=chosen_strategy_id,
            strategy_utilities=strategy_utilities,
            strategy_costs=strategy_costs,
        )
        self._publish(RegretComputedEvent(
            mission_id=mission_id,
            expected_regret=regret_res.expected_regret,
            counterfactual_regret=regret_res.counterfactual_regret,
            opportunity_cost=regret_res.opportunity_cost_usd,
        ))

        # 2. Self-Critique
        critique_res = self.critic.critique_plan(
            mission_id=mission_id,
            strategy_id=chosen_strategy_id,
            candidate_count=len(strategy_utilities),
            search_depth=4,
            estimated_risk=estimated_risk,
            confidence_score=confidence,
        )
        self._publish(PlannerCritiquedEvent(
            mission_id=mission_id,
            mistake_count=len(critique_res.diagnoses),
            bias_detected=any("BIAS" in d.code for d in critique_res.diagnoses),
            critique_score=critique_res.critique_score,
        ))

        # 3. Exploration / MAB selection
        exploration_res = self.exploration_engine.select_arm_ucb1()
        self._publish(ExplorationTriggeredEvent(
            mission_id=mission_id,
            chosen_arm=exploration_res.selected_arm_id,
            ucb_score=exploration_res.score,
            novelty_reward=exploration_res.exploration_bonus,
        ))

        # 4. Dynamic Hyperparameter Tuning
        opt_params = self.optimizer.optimize_parameters(
            document_complexity=document_complexity,
            critique_score=critique_res.critique_score,
        )

        verdict = "ACCEPT_PLAN"
        if critique_res.should_deepen_search:
            verdict = "DEEPEN_SEARCH"
        elif critique_res.should_switch_algorithm:
            verdict = "SWITCH_ALGORITHM"

        self._publish(MetaPlanningStartedEvent(
            mission_id=mission_id,
            planner_strategy=chosen_strategy_id,
            search_depth=opt_params.search_depth_limit,
            beam_width=opt_params.beam_width,
        ))

        return MetaPlanningReview(
            mission_id=mission_id,
            critique=critique_res,
            regret=regret_res,
            exploration=exploration_res,
            optimized_params=opt_params,
            meta_verdict=verdict,
        )

    def _publish(self, event: Any) -> None:
        if self.event_bus:
            self.event_bus.publish(event)
