"""
Monte Carlo and Metric Property Invariant Verification Test Suite.
Verifies statistical consistency, unbiasedness, and strict domain boundaries.
"""

import pytest
from app.runtime.metrics.definitions import MetricDefinition, MetricUnit, AggregationType
from app.runtime.metrics.provenance import MetricProvenanceRecord, compute_merkle_root
from app.runtime.metrics.validation import MetricValidator


def test_merkle_root_computation():
    ids = ["evt_1", "evt_2", "evt_3", "evt_4"]
    root = compute_merkle_root(ids)
    assert len(root) == 64
    # Deterministic order
    assert compute_merkle_root(["evt_4", "evt_1", "evt_3", "evt_2"]) == root


def test_metric_validator_invariants():
    defn = MetricDefinition(
        id="test_pct",
        name="Test Percentage",
        description="Test percentage invariant",
        category="EXECUTION",
        formula_id="FORMULA_WORKER_UTILIZATION",
        formula_expression="x / y",
        formula_latex=r"\frac{x}{y}",
        unit=MetricUnit.PERCENTAGE,
        version="2.0",
    )

    valid_record = MetricProvenanceRecord(
        metric_id="test_pct",
        metric_name="Test Percentage",
        metric_version="2.0",
        value=0.85,
        formatted_value="85.00%",
        unit=MetricUnit.PERCENTAGE.value,
        formula_id="FORMULA_WORKER_UTILIZATION",
        formula_expression="x / y",
        formula_latex=r"\frac{x}{y}",
        variables_used={},
        raw_event_ids=["e1", "e2"],
        sample_size=2,
        observation_window={"duration_seconds": 10.0},
        statistical_summary={
            "mean": 0.85,
            "variance": 0.01,
            "confidence_interval_95": [0.80, 0.90],
        },
        merkle_events_root_sha256=compute_merkle_root(["e1", "e2"]),
    )

    errors = MetricValidator.validate_provenance_record(valid_record, defn)
    assert len(errors) == 0


def test_monte_carlo_estimator_convergence():
    result = MetricValidator.run_monte_carlo_verification(
        true_mean=100.0,
        true_stdev=10.0,
        sample_size=200,
        trials=50,
    )
    assert result["is_statistically_sound"] is True
    assert result["mean_bias"] < 0.5
    assert result["ci_95_coverage_rate"] >= 0.85
