"""
Unit and Integration Tests for Outcome Verification & Reconstructors (ASVSP Pillar 1).
"""

import pytest
from app.runtime.outcomes import (
    OutcomeCollector,
    OutcomeValidator,
    OutcomeReconstructor,
    OutcomeStatisticsTracker,
)


def test_outcome_collection_and_validation():
    collector = OutcomeCollector()
    record = collector.record_outcome(
        mission_id="test_m_01",
        task_id="t_extract",
        predicted_accuracy=0.98,
        observed_accuracy=0.96,
        predicted_latency_ms=500.0,
        observed_latency_ms=520.0,
        predicted_cost_usd=0.002,
        observed_cost_usd=0.0021,
        sla_target_ms=1000.0,
    )

    assert record.mission_id == "test_m_01"
    assert record.accuracy_residual == pytest.approx(0.02, rel=1e-3)
    assert record.latency_residual == pytest.approx(-20.0, rel=1e-3)
    assert record.sla_breached is False
    assert len(collector.get_all_records()) == 1


def test_outcome_validator_invariants():
    # Valid
    assert OutcomeValidator.validate_bounds(0.95, 450.0, 0.001) is True
    # Invalid accuracy
    assert OutcomeValidator.validate_bounds(1.5, 450.0, 0.001) is False
    # Negative latency
    assert OutcomeValidator.validate_bounds(0.95, -10.0, 0.001) is False
    # Negative cost
    assert OutcomeValidator.validate_bounds(0.95, 450.0, -0.05) is False


def test_outcome_reconstructor():
    events = [
        {"event_type": "TASK_DISPATCHED", "task_id": "t1", "timestamp": 100.0},
        {"event_type": "MODEL_INFERENCE_DONE", "task_id": "t1", "timestamp": 100.45, "token_count": 1200},
        {"event_type": "TASK_VALIDATED", "task_id": "t1", "confidence_score": 0.965},
    ]

    reconstructed = OutcomeReconstructor.reconstruct_from_events("mission_reconstruct", events)
    assert reconstructed.observed_latency_ms >= 450.0
    assert reconstructed.observed_accuracy == pytest.approx(1.0, rel=1e-3)
    assert reconstructed.observed_cost_usd > 0.0


def test_outcome_statistics_tracker():
    tracker = OutcomeStatisticsTracker()
    collector = OutcomeCollector()
    for i in range(10):
        collector.record_outcome(
            mission_id=f"m_{i}",
            task_id="t1",
            predicted_accuracy=0.95,
            observed_accuracy=0.90 if i == 0 else 0.95,
            predicted_latency_ms=500.0,
            observed_latency_ms=1200.0 if i == 0 else 480.0,
            predicted_cost_usd=0.002,
            observed_cost_usd=0.002,
            sla_target_ms=1000.0,
        )

    stats = tracker.compute_window_statistics(collector.get_all_records())
    assert stats.total_samples == 10
    assert stats.sla_compliance_rate == pytest.approx(0.90, rel=1e-2)
    assert stats.mean_accuracy_error >= 0.0
