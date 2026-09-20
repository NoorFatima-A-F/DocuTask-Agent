"""Tests for Configuration Templating, Versioning, and Feature Flag Targeting."""

import pytest
from app.infrastructure.deployment.configuration import ConfigTemplate, ConfigurationManager
from app.infrastructure.deployment.features import RolloutRule, FeatureFlag, FeatureRolloutManager


def test_config_template_rendering_and_version_rollback() -> None:
    # 1. Template
    tmpl = ConfigTemplate(
        template_id="t1",
        name="WorkerConfig",
        template_string="WORKERS=${NUM_WORKERS:-8}\nREDIS_URL=${REDIS_HOST:-localhost}:6379",
    )
    rendered = tmpl.render({"NUM_WORKERS": 16})
    assert "WORKERS=16" in rendered
    assert "REDIS_URL=localhost:6379" in rendered

    # 2. Config manager versioning and rollback
    mgr = ConfigurationManager()
    v1 = mgr.set_config("ocr-service", "prod", {"batch_size": 10})
    assert v1.version == 1

    v2 = mgr.set_config("ocr-service", "prod", {"batch_size": 50})
    assert v2.version == 2
    assert mgr.get_active_config("ocr-service", "prod")["batch_size"] == 50

    # Rollback to v1
    rolled = mgr.rollback_config("ocr-service", "prod")
    assert rolled is not None
    assert rolled.version == 1
    assert mgr.get_active_config("ocr-service", "prod")["batch_size"] == 10


def test_feature_rollout_manager_targeting_and_kill_switch() -> None:
    mgr = FeatureRolloutManager()
    flag = mgr.create_flag("new_ai_agent_runtime", "New AI Agent Runtime", default_enabled=True)

    # 1. Environment & Tenant specific rule
    flag.rules = [
        RolloutRule(target_environments=["prod"], target_tenants=["tenant-enterprise-01"], percentage=100.0),
    ]

    assert mgr.is_feature_enabled("new_ai_agent_runtime", tenant_id="tenant-enterprise-01", environment="prod") is True
    assert mgr.is_feature_enabled("new_ai_agent_runtime", tenant_id="tenant-other", environment="prod") is False
    assert mgr.is_feature_enabled("new_ai_agent_runtime", tenant_id="tenant-enterprise-01", environment="dev") is False

    # 2. Kill switch activation
    mgr.set_kill_switch("new_ai_agent_runtime", active=True)
    assert mgr.is_feature_enabled("new_ai_agent_runtime", tenant_id="tenant-enterprise-01", environment="prod") is False
