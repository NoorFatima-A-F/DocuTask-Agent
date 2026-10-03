"""Tests for Extension Registry and Extension Contracts."""

import pytest
from app.governance.platform.extensions.contracts import (
    CustomRiskEvaluatorContract,
    ExtensionCapability,
)
from app.governance.platform.extensions.registry import ExtensionRegistry
from app.governance.platform.extensions.validators import ExtensionValidationError


class MockRiskExtension(CustomRiskEvaluatorContract):
    def calculate_risk(self, action: str, resource: str, context: dict) -> float:
        if "sensitive" in resource:
            return 95.0
        return 5.0


class InvalidExtension:
    pass


def test_extension_validation_and_registration():
    registry = ExtensionRegistry()
    ext = MockRiskExtension()

    # Successful registration
    rec = registry.register_extension(
        extension_obj=ext,
        name="Mock Risk Scorer",
        version="1.0.0",
        owner="risk_team",
        tenant_id="tenant_gamma",
        capabilities=[ExtensionCapability.RISK_SCORER],
    )
    assert rec.extension_id.startswith("ext_")
    assert rec.is_enabled is True

    # Invalid extension missing interface
    with pytest.raises(ExtensionValidationError):
        registry.register_extension(
            extension_obj=InvalidExtension(),
            name="Broken Ext",
            version="1.0.0",
            owner="risk_team",
            tenant_id="tenant_gamma",
            capabilities=[ExtensionCapability.RISK_SCORER],
        )


def test_extension_enable_disable_and_invocation():
    registry = ExtensionRegistry()
    ext = MockRiskExtension()

    rec = registry.register_extension(
        extension_obj=ext,
        name="Risk Scorer Ext",
        version="1.0.0",
        owner="risk_team",
        tenant_id="tenant_gamma",
        capabilities=[ExtensionCapability.RISK_SCORER],
    )

    # Query
    inst = registry.get_extension_instance(rec.extension_id)
    assert inst is not None
    assert inst.calculate_risk("read", "sensitive_data", {}) == 95.0

    # Disable
    disabled = registry.disable_extension(rec.extension_id)
    assert disabled.is_enabled is False

    # List only enabled
    enabled_list = registry.list_extensions(tenant_id="tenant_gamma", only_enabled=True)
    assert len(enabled_list) == 0

    # Enable
    enabled = registry.enable_extension(rec.extension_id)
    assert enabled.is_enabled is True
