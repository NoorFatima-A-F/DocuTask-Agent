"""
Tests for Feature Flag Engine.
"""

import pytest
from app.core.feature_flags.service import FeatureFlagService


def test_feature_flag_boolean_and_kill_switch():
    ff = FeatureFlagService()
    ff.register_flag("new_agent_runtime", default_enabled=True)

    assert ff.is_enabled("new_agent_runtime") is True

    # Activate kill switch
    ff.set_kill_switch("new_agent_runtime", active=True)
    assert ff.is_enabled("new_agent_runtime") is False


def test_feature_flag_org_and_workspace_overrides():
    ff = FeatureFlagService()
    ff.register_flag("experimental_ocr", default_enabled=False)

    assert ff.is_enabled("experimental_ocr", org_id="org-1") is False

    # Enable for org-1
    ff.enable_for_org("experimental_ocr", "org-1")
    assert ff.is_enabled("experimental_ocr", org_id="org-1") is True
    assert ff.is_enabled("experimental_ocr", org_id="org-2") is False

    # Explicitly disable for specific workspace in org-1
    ff.disable_for_workspace("experimental_ocr", "ws-beta")
    assert ff.is_enabled("experimental_ocr", org_id="org-1", workspace_id="ws-beta") is False
    assert ff.is_enabled("experimental_ocr", org_id="org-1", workspace_id="ws-prod") is True


def test_feature_flag_percentage_rollout():
    ff = FeatureFlagService()
    ff.register_flag("canary_feature", default_enabled=False)
    ff.set_percentage("canary_feature", 50)

    # Deterministic evaluation across entities
    res_a = ff.is_enabled("canary_feature", entity_id="user_alpha")
    res_b = ff.is_enabled("canary_feature", entity_id="user_alpha")
    assert res_a == res_b
