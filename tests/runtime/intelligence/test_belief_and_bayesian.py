import pytest
from app.runtime.intelligence.belief_state import (
    BeliefStateEngine,
    BetaBelief,
    KalmanBelief,
)
from app.runtime.intelligence.bayesian_update import BayesianUpdateEngine


def test_beta_belief_initialization_and_properties():
    belief = BetaBelief(
        name="ocr_success",
        alpha=18.0,
        beta_param=2.0,
        description="Probability that OCR completes with high accuracy",
    )
    assert belief.name == "ocr_success"
    assert round(belief.mean, 4) == 0.9000
    assert belief.variance > 0
    ci_low, ci_high = belief.get_credible_interval_95()
    assert 0.70 < ci_low < 0.95
    assert ci_low < ci_high <= 1.0
    assert belief.shannon_entropy() > 0


def test_kalman_belief_filtering():
    kalman = KalmanBelief(
        name="worker_latency_ms",
        state_mean=250.0,
        state_variance=2500.0,
        process_noise_q=10.0,
        measurement_noise_r=50.0,
    )
    assert kalman.state_mean == 250.0
    
    # Update with new measurement
    updated = kalman.update_measurement(300.0)
    assert 250.0 < updated < 300.0
    assert kalman.state_variance > 0


def test_belief_state_engine_registration_and_queries():
    engine = BeliefStateEngine(mission_id="m_test_001")
    beliefs = engine.list_beliefs()
    assert len(beliefs) >= 10
    assert engine.compute_total_entropy() > 0
    
    # Query specific belief
    b = engine.get_belief("ocr_success")
    assert b is not None
    assert b.mean > 0.5


def test_bayesian_update_engine_conjugate_update():
    belief_engine = BeliefStateEngine(mission_id="m_test_002")
    update_engine = BayesianUpdateEngine(belief_engine=belief_engine)
    
    initial_mean = belief_engine.get_belief("ocr_success").mean
    
    # Observe 5 successes and 0 failures
    report = update_engine.submit_observation(
        variable_name="ocr_success",
        observed_signal="HIGH_CONFIDENCE_OCR_TEXT",
        success_increment=5.0,
        failure_increment=0.0,
        likelihood=0.98,
        worker_id="worker_ocr_node_1",
    )
    
    updated_mean = belief_engine.get_belief("ocr_success").mean
    assert updated_mean > initial_mean
    assert report.posterior_mean == updated_mean
    assert len(update_engine.get_evidence_chain()) > 0
    assert report.merkle_evidence_root != ""
