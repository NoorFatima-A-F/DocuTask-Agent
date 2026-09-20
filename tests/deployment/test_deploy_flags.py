"""Unit tests for Feature Flag Platform."""
import pytest
from app.deployment.flags.evaluation import FlagEvaluationContext, FlagEvaluator
from app.deployment.flags.manager import FeatureFlagManager


def test_flag_evaluator_percentage_rollout_deterministic():
    # Deterministic test: same entity and key should always evaluate identically
    res1 = FlagEvaluator.evaluate_percentage("key1", "tenant_xyz", 50)
    res2 = FlagEvaluator.evaluate_percentage("key1", "tenant_xyz", 50)
    assert res1 == res2


def test_flag_manager_targeting_and_kill_switch():
    manager = FeatureFlagManager()
    flag = manager.create_flag(
        key="enable_llm_v3",
        name="LLM V3 Extraction",
        enabled=True,
        allowed_tenants=["tenant_alpha", "tenant_beta"],
        allowed_environments=["prod"],
        rollout_percentage=100,
    )

    # Allowed tenant & prod
    ctx_allowed = FlagEvaluationContext(tenant_id="tenant_alpha", environment="prod")
    assert manager.is_enabled("enable_llm_v3", ctx_allowed) is True

    # Disallowed tenant
    ctx_disallowed = FlagEvaluationContext(tenant_id="tenant_gamma", environment="prod")
    assert manager.is_enabled("enable_llm_v3", ctx_disallowed) is False

    # Kill switch activation
    manager.activate_kill_switch("enable_llm_v3", reason="LLM V3 API rate limits hit")
    assert manager.is_enabled("enable_llm_v3", ctx_allowed) is False

    # Deactivate kill switch
    manager.deactivate_kill_switch("enable_llm_v3")
    assert manager.is_enabled("enable_llm_v3", ctx_allowed) is True
