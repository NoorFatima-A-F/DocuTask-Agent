"""
Tests for Scientific Planner Optimization (Pillar 3).
"""

import pytest
from app.runtime.intelligence.planner_opt.planner_optimizer import PlannerOptimizer
from app.runtime.intelligence.planner_opt.planner_version import (
    PlannerVersionConfig,
    PlannerVersionManager,
)
from app.runtime.intelligence.planner_opt.prediction_error import (
    PredictionErrorAnalyzer,
)


def test_prediction_error_tracking_and_loss_convergence():
    analyzer = PredictionErrorAnalyzer()

    # Record series of errors
    for i in range(10):
        analyzer.record_error(
            mission_id=f"msn_{i}",
            predicted={"latency_ms": 1000.0, "cost_usd": 0.010, "confidence": 0.95},
            actual={"latency_ms": 1000.0 + (10 - i) * 20, "cost_usd": 0.012, "confidence": 0.96},
        )

    summary = analyzer.compute_summary()
    assert summary["count"] == 10
    assert summary["mean_latency_mae_ms"] > 0
    assert summary["convergence_score"] > 0.5


def test_planner_version_manager_and_rollback():
    vmanager = PlannerVersionManager()
    assert vmanager.get_active().version_id == "v1.0.0"

    optimizer = PlannerOptimizer(version_manager=vmanager)
    candidate = optimizer.formulate_candidate_optimization(target_metric="latency_ms")
    assert candidate.status == "CANDIDATE"

    # Promote candidate
    promoted = optimizer.promote_candidate(candidate.version_id, experiment_id="exp_01", p_value=0.002)
    assert promoted is True
    assert vmanager.get_active().version_id == candidate.version_id

    # Rollback
    rolled = vmanager.rollback("v1.0.0")
    assert rolled is not None
    assert vmanager.get_active().version_id == "v1.0.0"
