"""Tests for Environment Management and Quota Isolation."""

from app.infrastructure.core.environment import (
    EnvironmentManager,
    EnvironmentType,
)


def test_environment_profile_retrieval_and_switching():
    mgr = EnvironmentManager(current_env=EnvironmentType.LOCAL)
    profile = mgr.get_profile()
    assert profile.env_type == EnvironmentType.LOCAL
    assert profile.max_cpu_cores == 8
    assert profile.allow_mock_providers is True

    mgr.set_current_environment(EnvironmentType.PRODUCTION)
    prod_profile = mgr.get_profile()
    assert prod_profile.env_type == EnvironmentType.PRODUCTION
    assert prod_profile.max_cpu_cores == 256
    assert prod_profile.require_deployment_approval is True


def test_environment_quota_validation():
    mgr = EnvironmentManager()

    # Valid deployment in LOCAL
    allowed, _ = mgr.validate_deployment_allowed(
        requested_replicas=2,
        requested_cpu=4,
        requested_memory_gb=8,
        env_type=EnvironmentType.LOCAL,
    )
    assert allowed is True

    # Exceeding replicas in LOCAL
    denied, reason = mgr.validate_deployment_allowed(
        requested_replicas=10,
        requested_cpu=4,
        requested_memory_gb=8,
        env_type=EnvironmentType.LOCAL,
    )
    assert denied is False
    assert "exceeds" in reason

    # Unsupported region in DEVELOPMENT
    denied_reg, reg_reason = mgr.validate_deployment_allowed(
        requested_replicas=2,
        requested_cpu=4,
        requested_memory_gb=8,
        target_region="ap-south-1",
        env_type=EnvironmentType.DEVELOPMENT,
    )
    assert denied_reg is False
    assert "not allowed" in reg_reason
