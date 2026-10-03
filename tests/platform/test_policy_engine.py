"""Tests for Enterprise Policy Engine."""

from app.platform.policy.policy_engine import (
    PolicyEngine,
)


def test_policy_enforcement():
    engine = PolicyEngine()
    assert len(engine.list_policies()) >= 4

    # Action under budget
    res_ok = engine.evaluate_action({"cost_usd": 0.002, "amount": 5000})
    assert res_ok.is_allowed is True
    assert len(res_ok.violations) == 0

    # Action exceeding cost budget
    res_cost_fail = engine.evaluate_action({"cost_usd": 0.08})
    assert res_cost_fail.is_allowed is False
    assert any("exceeds ceiling" in v["reason"] for v in res_cost_fail.violations)

    # Action high value without human signature
    res_gov_fail = engine.evaluate_action({"amount": 15000, "human_signed": False})
    assert res_gov_fail.is_allowed is False
    assert any("Human Supervisor Signature" in v["reason"] for v in res_gov_fail.violations)
