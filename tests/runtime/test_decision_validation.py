"""
Unit & Invariant Tests for Decision Validation Engine (QDIOP / SDIOP).
"""

from app.runtime.decision_validation import (
    InvariantChecker,
    ReplayVerifier,
    DecisionValidator,
)
from app.runtime.optimization import MultiObjectivePlanOptimizer


def test_invariant_checker_catches_negative_costs_or_probabilities():
    invalid_plan = {"cost_usd": -0.01, "latency_ms": 500.0, "accuracy": 1.25}
    is_ok, errors = InvariantChecker.check_decision_invariants(invalid_plan)
    assert not is_ok
    assert any("negative" in e for e in errors)
    assert any("outside [0, 1]" in e for e in errors)


def test_replay_verifier_ensures_identical_decision():
    candidates = [
        {"id": "p1", "accuracy": 0.98, "latency_ms": 600.0, "cost_usd": 0.01},
        {"id": "p2", "accuracy": 0.92, "latency_ms": 300.0, "cost_usd": 0.005},
    ]
    constraints = {"max_budget_usd": 0.05}

    is_deterministic = ReplayVerifier.verify_replay_determinism(
        optimize_fn=lambda c, constr: MultiObjectivePlanOptimizer.optimize(c, constr),
        candidates=candidates,
        constraints=constraints,
        original_decision_id="p1",
        trials=5,
    )
    assert is_deterministic


def test_decision_validator_pre_dispatch():
    plan = {"id": "plan_1", "accuracy": 0.98, "latency_ms": 800.0, "cost_usd": 0.015, "overall_risk": 0.02}
    constraints = {"max_budget_usd": 0.03, "max_latency_ms": 1200.0}
    features = {f"f_{i}": 0.5 for i in range(12)}

    val_res = DecisionValidator.validate_plan_for_dispatch(
        plan=plan,
        constraints=constraints,
        features=features,
        policy_version="v1.0.0",
    )
    assert val_res.is_approved
    assert val_res.constraint_compliance
    assert val_res.invariant_compliance
    assert val_res.feature_completeness
    assert val_res.certificate_hash != ""
