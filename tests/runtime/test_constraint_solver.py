"""
Unit & Feasibility Tests for Constraint Solver (QDIOP / SDIOP).
"""

from app.runtime.constraints import (
    ConstraintSolver,
    FeasibilityEngine,
)


def test_feasibility_engine_slack_calculation():
    metrics = {"cost_usd": 0.015, "latency_ms": 700.0, "accuracy": 0.98, "overall_risk": 0.02}
    constraints = {"max_budget_usd": 0.030, "max_latency_ms": 1200.0, "min_accuracy": 0.95}

    eval_res = FeasibilityEngine.evaluate(metrics, constraints)
    assert eval_res.is_feasible
    assert eval_res.slack_variables["budget_slack_usd"] == 0.015
    assert eval_res.slack_variables["latency_slack_ms"] == 500.0


def test_constraint_solver_partitions_feasibility():
    plans = [
        {"id": "valid_plan", "cost_usd": 0.01, "latency_ms": 500.0, "accuracy": 0.97},
        {"id": "expensive_plan", "cost_usd": 0.10, "latency_ms": 500.0, "accuracy": 0.99},
    ]
    constraints = {"max_budget_usd": 0.05}

    result = ConstraintSolver.solve(plans, constraints)
    assert result.is_satisfiable
    assert len(result.feasible_candidates) == 1
    assert result.feasible_candidates[0]["id"] == "valid_plan"
    assert len(result.infeasible_candidates) == 1
