"""
Unit & Dominance Tests for Pareto Optimizer (QDIOP / SDIOP).
"""

import pytest
from app.runtime.optimization.pareto_optimizer import ParetoOptimizer
from app.runtime.optimization.optimizer_validator import OptimizerValidator


def test_pareto_dominance_conditions():
    cand_better = {"accuracy": 0.99, "cost_usd": 0.01, "latency_ms": 500.0}
    cand_worse = {"accuracy": 0.90, "cost_usd": 0.05, "latency_ms": 1500.0}

    assert ParetoOptimizer.dominates(cand_better, cand_worse)
    assert not ParetoOptimizer.dominates(cand_worse, cand_better)


def test_pareto_frontier_extraction():
    candidates = [
        {"id": "c1", "accuracy": 0.99, "cost_usd": 0.04, "latency_ms": 2000.0},
        {"id": "c2", "accuracy": 0.95, "cost_usd": 0.01, "latency_ms": 600.0},
        {"id": "c3", "accuracy": 0.90, "cost_usd": 0.002, "latency_ms": 250.0},
        {"id": "c4_dominated", "accuracy": 0.88, "cost_usd": 0.05, "latency_ms": 3000.0},
    ]

    frontier, dominated = ParetoOptimizer.extract_pareto_frontier(candidates)
    frontier_ids = {c["id"] for c in frontier}
    dominated_ids = {c["id"] for c in dominated}

    assert "c1" in frontier_ids
    assert "c2" in frontier_ids
    assert "c3" in frontier_ids
    assert "c4_dominated" in dominated_ids


def test_pareto_stability_under_permutations():
    candidates = [
        {"id": "p1", "accuracy": 0.98, "cost_usd": 0.02, "latency_ms": 800.0},
        {"id": "p2", "accuracy": 0.92, "cost_usd": 0.005, "latency_ms": 300.0},
        {"id": "p3_dom", "accuracy": 0.90, "cost_usd": 0.03, "latency_ms": 1200.0},
    ]
    assert OptimizerValidator.assert_pareto_stability(candidates, trials=5)
