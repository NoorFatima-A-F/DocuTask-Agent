"""
Tests for Capability Registry and Plugin Management.
"""

import pytest
import asyncio
from app.platform.capabilities.registry import CapabilityRegistry
from app.platform.plugins.manager import PluginManager
from app.platform.plugins.models import PluginManifest, PluginStatus, PluginType
from app.platform.kernel.versioning import SemanticVersion


def test_capability_registry():
    registry = CapabilityRegistry()
    assert not registry.has_capability("document.ocr")

    registry.register_capability(
        name="document.ocr",
        provider="TesseractOCRModule",
        version=SemanticVersion(1, 0, 0),
        metadata={"engine": "tesseract"},
    )

    assert registry.has_capability("document.ocr")
    assert registry.get_provider("document.ocr") == "TesseractOCRModule"
    assert len(registry.list_capabilities()) == 1


class SampleConnectorPlugin:
    def __init__(self):
        self.loaded = False
        self.unloaded = False

    async def on_load(self, kernel=None):
        self.loaded = True

    async def on_unload(self):
        self.unloaded = True


def test_plugin_lifecycle():
    manager = PluginManager()
    manifest = PluginManifest(
        id="salesforce-connector",
        name="Salesforce CRM Connector",
        version=SemanticVersion(1, 2, 0),
        plugin_type=PluginType.CONNECTOR,
        permissions=["network:salesforce.com"],
    )

    plugin_inst = SampleConnectorPlugin()
    record = manager.register_plugin(manifest, instance=plugin_inst)

    assert record.status == PluginStatus.VALIDATED
    assert record.manifest.name == "Salesforce CRM Connector"

    # Enable
    asyncio.run(manager.enable_plugin("salesforce-connector"))
    assert record.status == PluginStatus.ACTIVE
    assert plugin_inst.loaded is True

    # Disable
    asyncio.run(manager.disable_plugin("salesforce-connector"))
    assert record.status == PluginStatus.DISABLED
    assert plugin_inst.unloaded is True
