"""
Unit Tests for APDLE Planner Simulation, Execution Predictor, and Completion Estimator.
"""

import pytest
from app.runtime.planning.graph.graph_builder import ExecutionGraphBuilder
from app.runtime.planning.simulation.completion_estimator import CompletionEstimator
from app.runtime.planning.simulation.execution_predictor import ExecutionPredictor
from app.runtime.planning.simulation.planner_simulator import PlannerSimulator


def test_planner_monte_carlo_simulator():
    """Verifies that Monte Carlo simulation computes P50, P90, P99 and expected costs."""
    dag = ExecutionGraphBuilder.build_financial_invoice_audit_dag(mission_id="m-sim")
    sim = PlannerSimulator.simulate_dag(dag, num_trials=50)

    assert sim.trials_count == 50
    assert sim.p50_completion_ms > 0
    assert sim.p90_completion_ms >= sim.p50_completion_ms
    assert sim.p99_completion_ms >= sim.p90_completion_ms
    assert sim.expected_total_cost_usd > 0
    assert len(sim.bottleneck_node_ids) > 0


def test_execution_predictor():
    """Verifies prediction vs actual comparison and accuracy score calculation."""
    dag = ExecutionGraphBuilder.build_financial_invoice_audit_dag(mission_id="m-pred")
    comp = ExecutionPredictor.compare_prediction_vs_actual(
        dag=dag, actual_runtime_ms=750.0, actual_cost_usd=0.0028
    )

    assert comp.predicted_runtime_ms > 0
    assert 0.0 <= comp.accuracy_score <= 1.0


def test_completion_estimator():
    """Verifies progress percentage and remaining ETA calculation."""
    dag = ExecutionGraphBuilder.build_financial_invoice_audit_dag(mission_id="m-eta")
    completed = {"node_ocr_01", "node_extract_items"}
    
    eta_info = CompletionEstimator.estimate_remaining(dag, completed)
    assert eta_info["progress_pct"] == 40.0
    assert eta_info["remaining_ms"] > 0
