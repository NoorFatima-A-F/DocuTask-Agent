"""Probabilistic Cognitive Runtime Coordinator for DocuTask ADIP.

Coordinates belief states, forward world simulations, Bayesian evidence accumulation,
planner uncertainty decomposition, and EVOI sensing action execution.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.runtime.events.event_bus import EventBus
from app.runtime.events.probabilistic_events import (
    BeliefInitializedEvent,
    BeliefUpdatedEvent,
    PosteriorComputedEvent,
    EntropyReducedEvent,
    InformationRequestedEvent,
    WorldPredictionGeneratedEvent,
    PlannerConfidenceCalculatedEvent,
    ExpectedValueInformationComputedEvent,
)
from app.runtime.intelligence.belief_state import BeliefStateEngine, BeliefSnapshot, BetaBelief
from app.runtime.intelligence.world_model import WorldModel, WorldStateForecast
from app.runtime.intelligence.bayesian_update import BayesianUpdateEngine, BayesianPosteriorReport
from app.runtime.intelligence.planner_uncertainty import PlannerUncertaintyEngine, UncertaintyDecomposition
from app.runtime.intelligence.active_information import ActiveInformationEngine, InformationActionRecommendation


class CognitiveStateSummary(BaseModel):
    """Unified snapshot of the agent's probabilistic mental state."""
    mission_id: str
    total_entropy_bits: float
    beliefs: Dict[str, Dict[str, Any]]
    world_forecasts: List[WorldStateForecast]
    uncertainty: UncertaintyDecomposition
    evoi_recommendations: List[InformationActionRecommendation]


class ProbabilisticCognitiveRuntime:
    """The central probabilistic intelligence runtime coordinator."""

    def __init__(self, mission_id: str = "default_mission", event_bus: Optional[EventBus] = None) -> None:
        self.mission_id = mission_id
        self.event_bus = event_bus or EventBus.get_instance()
        self.belief_engine = BeliefStateEngine(mission_id=mission_id)
        self.world_model = WorldModel()
        self.bayesian_engine = BayesianUpdateEngine(self.belief_engine)
        self.uncertainty_engine = PlannerUncertaintyEngine()
        self.active_info_engine = ActiveInformationEngine()

        # Emit initialization event
        self._publish(BeliefInitializedEvent(
            mission_id=mission_id,
            belief_version=self.belief_engine.version,
            prior_entropy=self.belief_engine.compute_total_entropy(),
            variable_count=len(self.belief_engine.list_beliefs()),
        ))

    def update_evidence(
        self,
        variable_name: str,
        observed_signal: str,
        success_inc: float,
        failure_inc: float,
        likelihood: float = 0.95,
        worker_id: Optional[str] = None,
    ) -> BayesianPosteriorReport:
        old_entropy = self.belief_engine.compute_total_entropy()
        report = self.bayesian_engine.submit_observation(
            variable_name=variable_name,
            observed_signal=observed_signal,
            success_increment=success_inc,
            failure_increment=failure_inc,
            likelihood=likelihood,
            worker_id=worker_id,
        )
        new_entropy = self.belief_engine.compute_total_entropy()
        entropy_delta = new_entropy - old_entropy

        self._publish(BeliefUpdatedEvent(
            mission_id=self.mission_id,
            variable_name=variable_name,
            prior_mean=report.prior_mean,
            posterior_mean=report.posterior_mean,
            entropy_delta=entropy_delta,
        ))
        self._publish(PosteriorComputedEvent(
            mission_id=self.mission_id,
            hypothesis=f"{variable_name}==True",
            likelihood=report.likelihood,
            posterior_probability=report.posterior_mean,
            credible_interval=report.credible_interval_95,
        ))
        if entropy_delta < 0:
            self._publish(EntropyReducedEvent(
                mission_id=self.mission_id,
                initial_entropy=old_entropy,
                final_entropy=new_entropy,
                information_gain_bits=abs(entropy_delta),
            ))

        return report

    def forecast_world(self, load_factor: float = 1.0, concurrency: int = 4) -> List[WorldStateForecast]:
        forecasts = self.world_model.forecast_trajectory(load_factor, concurrency)
        for f in forecasts:
            self._publish(WorldPredictionGeneratedEvent(
                mission_id=self.mission_id,
                horizon_minutes=f.horizon_minutes,
                predicted_gpu_load=f.predicted_gpu_load_pct,
                predicted_token_burn=int(f.predicted_token_burn_velocity * 60 * f.horizon_minutes),
                predicted_queue_depth=f.predicted_queue_depth,
            ))
        return forecasts

    def evaluate_evoi(self) -> List[InformationActionRecommendation]:
        recs = self.active_info_engine.evaluate_sensing_actions(self.belief_engine)
        for r in recs:
            self._publish(ExpectedValueInformationComputedEvent(
                mission_id=self.mission_id,
                candidate_action=r.action_type.value,
                expected_gain=r.expected_utility_gain,
                net_evoi=r.net_evoi,
            ))
        return recs

    def get_cognitive_state(self) -> CognitiveStateSummary:
        beliefs_dict = {}
        for k, b in self.belief_engine.list_beliefs().items():
            ci = b.get_credible_interval_95()
            beliefs_dict[k] = {
                "name": b.name,
                "mean": round(b.mean, 4),
                "variance": round(b.variance, 6),
                "entropy_bits": round(b.shannon_entropy(), 4),
                "credible_interval_95": [ci[0], ci[1]],
                "description": b.description,
            }

        forecasts = self.world_model.forecast_trajectory()
        unc = self.uncertainty_engine.evaluate_uncertainty(self.mission_id, self.belief_engine)
        evoi = self.active_info_engine.evaluate_sensing_actions(self.belief_engine)

        self._publish(PlannerConfidenceCalculatedEvent(
            mission_id=self.mission_id,
            epistemic_uncertainty=unc.epistemic_uncertainty,
            aleatoric_uncertainty=unc.aleatoric_uncertainty,
            composite_confidence=unc.composite_confidence,
        ))

        return CognitiveStateSummary(
            mission_id=self.mission_id,
            total_entropy_bits=round(self.belief_engine.compute_total_entropy(), 4),
            beliefs=beliefs_dict,
            world_forecasts=forecasts,
            uncertainty=unc,
            evoi_recommendations=evoi,
        )

    def _publish(self, event: Any) -> None:
        if self.event_bus:
            self.event_bus.publish(event)
