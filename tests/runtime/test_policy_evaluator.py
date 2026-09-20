"""
Unit & Stability Tests for Policy Evaluator (QDIOP / SDIOP).
"""

import pytest
from app.runtime.evaluation import (
    PolicyEvaluator,
    PolicyComparator,
    DecisionStabilityAnalyzer,
    WeightSensitivityAnalyzer,
)


def test_policy_comparator_win_rate_and_deltas():
    metrics_a = [{"utility": 0.75, "latency_ms": 1200.0, "cost_usd": 0.02} for _ in range(20)]
    metrics_b = [{"utility": 0.90, "latency_ms": 800.0, "cost_usd": 0.01} for _ in range(20)]

    comp = PolicyComparator.compare_policies(metrics_a, metrics_b)
    assert comp["win_rate_policy_b_percent"] == 100.0
    assert comp["utility_gain_percentage"] > 15.0
    assert comp["is_statistically_superior"]


def test_decision_stability_under_perturbation():
    def simple_decision_rule(feat):
        return "MODEL_PRO" if feat.get("document_complexity", 0.5) > 0.8 else "MODEL_FLASH"

    stable_features = {"document_complexity": 0.3}
    res = DecisionStabilityAnalyzer.evaluate_perturbation_stability(
        decision_fn=simple_decision_rule,
        base_features=stable_features,
        noise_level=0.02,
        trials=30,
    )
    assert res["stability_score"] >= 0.95
    assert res["is_stable"]
