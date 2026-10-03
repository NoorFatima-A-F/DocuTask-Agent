"""
Unit & Determinism Tests for Multi-Objective Plan Optimizer (QDIOP / SDIOP).
"""

from app.runtime.optimization import (
    MultiObjectivePlanOptimizer,
    ObjectiveFunctions,
)


def test_objective_scalarizations():
    objs = {"accuracy": 0.95, "latency_ms": 0.20, "cost_usd": 0.10}
    weights = {"accuracy": 0.5, "latency_ms": 0.25, "cost_usd": 0.25}
    is_cost = {"accuracy": False, "latency_ms": True, "cost_usd": True}

    # Weighted sum
    score = ObjectiveFunctions.weighted_sum_scalarization(objs, weights, is_cost)
    assert 0.0 <= score <= 1.0

    # Chebyshev
    chebyshev = ObjectiveFunctions.chebyshev_scalarization(objs, weights, is_cost)
    assert 0.0 <= chebyshev <= 1.0


def test_multi_objective_plan_optimizer():
    candidates = [
        {"id": "plan_a", "plan_name": "Fast Wavefront", "accuracy": 0.92, "latency_ms": 400.0, "cost_usd": 0.005, "safety_compliance": 1.0, "reliability": 0.95},
        {"id": "plan_b", "plan_name": "Balanced Hybrid", "accuracy": 0.98, "latency_ms": 800.0, "cost_usd": 0.015, "safety_compliance": 1.0, "reliability": 0.98},
        {"id": "plan_c", "plan_name": "Slow High-Cost", "accuracy": 0.93, "latency_ms": 2500.0, "cost_usd": 0.050, "safety_compliance": 0.9, "reliability": 0.90},
    ]

    res = MultiObjectivePlanOptimizer.optimize(
        candidate_plans=candidates,
        constraints={"max_budget_usd": 0.03, "max_latency_ms": 1500.0},
    )

    assert res["selected_plan"] is not None
    assert res["selected_plan"]["id"] in ("plan_a", "plan_b")
    assert len(res["pareto_frontier"]) >= 1
    assert res["selected_utility"] > 0.0
