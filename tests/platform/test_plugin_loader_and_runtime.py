"""Tests for Plugin Loader and Plugin Runtime."""

from app.platform.plugins.plugin_loader import (
    PluginLoader,
)
from app.platform.plugins.plugin_runtime import PluginRuntime


def test_plugin_loader_and_runtime():
    loader = PluginLoader()
    manifests = loader.discover_and_load_all()
    assert len(manifests) >= 4
    assert loader.get_plugin("plugin.invoice.processing") is not None

    runtime = PluginRuntime(loader=loader)
    res = runtime.execute_plugin_capability(
        plugin_id="plugin.invoice.processing",
        capability="extraction.invoice",
        input_payload={"doc_id": "inv-001", "items": [{"name": "Widget", "price": 10.0}]},
    )
    assert res["status"] == "COMPLETED"
    assert len(runtime.get_history()) == 1
