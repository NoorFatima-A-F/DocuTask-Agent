"""Tests for Declarative Configuration, Validation, and Rollback."""

import pytest
from app.infrastructure.config.manager import ConfigurationManager
from app.infrastructure.config.models import (
    InfrastructureManifest,
    RegionConfig,
    ResourceLimits,
    RuntimeConfig,
    ScalingPolicy,
)
from app.infrastructure.core.exceptions import ConfigurationInvalidError


def test_manifest_validation_and_registration():
    config_mgr = ConfigurationManager()

    valid_manifest = InfrastructureManifest(
        manifest_id="man_001",
        service_name="agent-runtime",
        version="1.0.0",
        environment="PRODUCTION",
        runtime=RuntimeConfig(replicas=3),
        resources=ResourceLimits(cpu=2.0, memory_gb=4.0),
        region=RegionConfig(primary="us-east-1", supported_regions=["us-east-1", "eu-west-1"]),
        scaling=ScalingPolicy(enabled=True, min_replicas=1, max_replicas=10),
    )

    registered = config_mgr.register_manifest(valid_manifest)
    assert registered.manifest_id == "man_001"

    current = config_mgr.get_current_manifest("agent-runtime", "PRODUCTION")
    assert current.version == "1.0.0"


def test_manifest_validation_failure():
    config_mgr = ConfigurationManager()

    invalid_manifest = InfrastructureManifest(
        manifest_id="man_bad",
        service_name="agent-runtime",
        version="1.0.1",
        environment="PRODUCTION",
        runtime=RuntimeConfig(replicas=20),
        scaling=ScalingPolicy(enabled=True, min_replicas=5, max_replicas=2),  # min > max
    )

    with pytest.raises(ConfigurationInvalidError):
        config_mgr.register_manifest(invalid_manifest)


def test_manifest_versioning_and_rollback():
    config_mgr = ConfigurationManager()

    v1 = InfrastructureManifest(
        manifest_id="man_v1",
        service_name="workflow-engine",
        version="1.0.0",
        runtime=RuntimeConfig(replicas=2),
    )
    v2 = InfrastructureManifest(
        manifest_id="man_v2",
        service_name="workflow-engine",
        version="2.0.0",
        runtime=RuntimeConfig(replicas=5),
    )

    config_mgr.register_manifest(v1)
    config_mgr.register_manifest(v2)
    assert config_mgr.get_current_manifest("workflow-engine").version == "2.0.0"

    # Rollback to 1.0.0
    rolled_back = config_mgr.rollback("workflow-engine", "1.0.0")
    assert rolled_back.version == "1.0.0"
    assert config_mgr.get_current_manifest("workflow-engine").version == "1.0.0"
