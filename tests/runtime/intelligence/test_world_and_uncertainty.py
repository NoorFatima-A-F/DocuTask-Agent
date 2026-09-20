import pytest
from app.runtime.intelligence.world_model import WorldModel, WorldStateForecast
from app.runtime.intelligence.planner_uncertainty import PlannerUncertaintyEngine
from app.runtime.intelligence.active_information import ActiveInformationEngine
from app.runtime.intelligence.belief_state import BeliefStateEngine


def test_world_model_multistep_forecasting():
    world_model = WorldModel()
    
    # Generate 5m, 10m, 30m forecasts
    forecasts = world_model.forecast_trajectory(
        current_mission_load_factor=1.2,
        cluster_concurrency=4,
    )
    
    assert len(forecasts) == 3
    for fcast in forecasts:
        assert fcast.horizon_minutes in [5, 10, 30]
        assert 0.0 <= fcast.predicted_gpu_load_pct <= 100.0
        assert fcast.predicted_queue_depth >= 0
        assert fcast.predicted_token_burn_velocity >= 0
        assert fcast.predicted_budget_burn_usd >= 0


def test_planner_uncertainty_epistemic_aleatoric():
    belief_engine = BeliefStateEngine(mission_id="m_test_unc")
    uncertainty_engine = PlannerUncertaintyEngine()
    
    decomposition = uncertainty_engine.evaluate_uncertainty(
        mission_id="m_test_unc",
        belief_engine=belief_engine,
        strategy_utility_delta=0.06,
        simulation_variance=0.005,
    )
    
    assert decomposition.mission_id == "m_test_unc"
    assert decomposition.epistemic_uncertainty >= 0
    assert decomposition.aleatoric_uncertainty >= 0
    assert decomposition.decision_stability_index > 0
    assert 0.0 <= decomposition.composite_confidence <= 1.0


def test_active_information_evoi_sensing():
    belief_engine = BeliefStateEngine(mission_id="m_test_evoi")
    evoi_engine = ActiveInformationEngine()
    
    recs = evoi_engine.evaluate_sensing_actions(
        belief_engine=belief_engine,
        current_max_utility=0.4392,
    )
    
    assert len(recs) >= 3
    for r in recs:
        assert r.expected_information_gain_bits >= 0
        assert r.net_evoi is not None
        assert isinstance(r.should_execute, bool)
