"""
Tests for Enterprise 11-Tier Configuration Precedence and Validation.
"""

from app.platform.configuration.provider import ConfigurationProvider
from app.platform.configuration.schema import ConfigDomain, ConfigSource


def test_configuration_defaults():
    provider = ConfigurationProvider()
    pool_size = provider.get("database.pool_size")
    assert pool_size == 20


def test_configuration_precedence_hierarchy():
    provider = ConfigurationProvider()

    # 1. Default is 20
    assert provider.get("database.pool_size") == 20

    # 2. YAML layer overrides Default
    provider.set_layer_value(ConfigSource.YAML_FILE, "database.pool_size", 25)
    assert provider.get("database.pool_size") == 25

    # 3. Environment layer overrides YAML
    provider.set_layer_value(ConfigSource.ENVIRONMENT, "database.pool_size", 30)
    assert provider.get("database.pool_size") == 30

    # 4. Organization layer overrides Environment
    assert provider.get("database.pool_size", org_overrides={"database.pool_size": 40}) == 40

    # 5. Workspace overrides Organization
    assert provider.get(
        "database.pool_size",
        org_overrides={"database.pool_size": 40},
        workspace_overrides={"database.pool_size": 50},
    ) == 50

    # 6. Execution override wins over all
    assert provider.get(
        "database.pool_size",
        org_overrides={"database.pool_size": 40},
        workspace_overrides={"database.pool_size": 50},
        execution_overrides={"database.pool_size": 100},
    ) == 100


def test_configuration_source_attribution():
    provider = ConfigurationProvider()
    provider.set_layer_value(ConfigSource.YAML_FILE, "database.pool_size", 25)

    resolved = provider.get_resolved("database.pool_size")
    assert resolved is not None
    assert resolved.value == 25
    assert resolved.source == ConfigSource.YAML_FILE
    assert resolved.domain == ConfigDomain.DATABASE
