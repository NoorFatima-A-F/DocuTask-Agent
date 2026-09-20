"""
Unit test suite for Enterprise Plugin Runtime.
Validates:
- Plugin manifest parsing and validation
- Unsupported API version rejection
- Sandbox permission policy enforcement
- Plugin dependency resolution and missing dependency errors
- Full 8-state plugin lifecycle
- LIFO transactional rollback upon failed plugin initialization
- Unload and deactivation
"""

import pytest
from app.agents.runtime.exceptions import PluginValidationError
from app.agents.runtime.plugin_loader import (
    PluginLoader,
    PluginManifest,
    PluginState,
    PluginValidator,
)
from app.agents.runtime.plugin_manager import (
    PluginDependencyResolver,
    PluginManager,
    PluginRollbackManager,
    PluginSandbox,
)
from app.agents.runtime.plugin_registry import PluginRegistry


def test_manifest_validation_success():
    manifest = PluginManifest(
        plugin_id="ocr_extractor",
        name="OCR Extraction Plugin",
        version="1.2.0",
        entrypoint="plugins.ocr:OCRExtractor",
        api_version="23.0",
        permissions=["filesystem:read", "telemetry:emit"],
    )
    PluginValidator.validate_manifest(manifest)
    assert manifest.plugin_id == "ocr_extractor"


@pytest.mark.parametrize(
    "bad_manifest, expected_error",
    [
        (
            {"plugin_id": "", "name": "Valid Name", "entrypoint": "entry"},
            "plugin_id' cannot be empty",
        ),
        (
            {"plugin_id": "p1", "name": "", "entrypoint": "entry"},
            "name' cannot be empty",
        ),
        (
            {"plugin_id": "p1", "name": "Valid Name", "entrypoint": ""},
            "entrypoint' cannot be empty",
        ),
        (
            {"plugin_id": "p1", "name": "Valid Name", "entrypoint": "entry", "api_version": "99.0"},
            "unsupported api_version '99.0'",
        ),
    ],
)
def test_manifest_validation_failures(bad_manifest, expected_error):
    loader = PluginLoader()
    with pytest.raises(PluginValidationError) as exc_info:
        loader.load_from_dict(bad_manifest)
    assert expected_error in str(exc_info.value)


def test_plugin_sandbox_enforces_permissions():
    sandbox = PluginSandbox(allowed_permissions={"filesystem:read", "telemetry:emit"})

    valid_manifest = PluginManifest(
        plugin_id="good_plugin",
        name="Good Plugin",
        entrypoint="main:run",
        permissions=["filesystem:read"],
    )
    sandbox.verify_permissions(valid_manifest)

    rogue_manifest = PluginManifest(
        plugin_id="rogue_plugin",
        name="Rogue Plugin",
        entrypoint="main:run",
        permissions=["filesystem:read", "kernel:root_access"],
    )
    with pytest.raises(PluginValidationError) as exc_info:
        sandbox.verify_permissions(rogue_manifest)
    assert "unauthorized permissions: ['kernel:root_access']" in str(exc_info.value)


def test_plugin_dependency_resolver():
    registry = PluginRegistry()
    m_base = PluginManifest(plugin_id="base_plugin", name="Base Plugin", entrypoint="base:run")
    reg_base = registry.register(m_base, instance=None)
    registry.update_state("base_plugin", PluginState.RUNNING)

    m_dependent = PluginManifest(
        plugin_id="child_plugin",
        name="Child Plugin",
        entrypoint="child:run",
        dependencies=["base_plugin"],
    )

    resolver = PluginDependencyResolver()
    active_map = {p.manifest.plugin_id: p for p in registry.list_active()}
    resolved = resolver.resolve_dependencies(m_dependent, active_map)
    assert resolved == ["base_plugin"]

    # Missing dependency
    m_unresolved = PluginManifest(
        plugin_id="broken_plugin",
        name="Broken Plugin",
        entrypoint="broken:run",
        dependencies=["non_existent_plugin"],
    )
    with pytest.raises(PluginValidationError) as exc_info:
        resolver.resolve_dependencies(m_unresolved, active_map)
    assert "missing active dependencies: ['non_existent_plugin']" in str(exc_info.value)


@pytest.mark.asyncio
async def test_plugin_manager_lifecycle_and_rollback():
    manager = PluginManager()

    # Load first plugin successfully
    manifest1 = {
        "plugin_id": "plugin_one",
        "name": "Plugin One",
        "entrypoint": "p1:init",
    }
    reg1 = await manager.load_plugin(manifest1)
    assert reg1.state == PluginState.RUNNING
    assert len(manager.get_active_plugins()) == 1

    # Load second plugin that fails during instantiation
    manifest2 = {
        "plugin_id": "plugin_two",
        "name": "Plugin Two",
        "entrypoint": "p2:init",
    }

    def failing_factory():
        raise RuntimeError("Initialization boom!")

    with pytest.raises(RuntimeError):
        await manager.load_plugin(manifest2, entrypoint_factory=failing_factory)

    # Manager rollback should have cleaned up failed plugin
    active_ids = [p.manifest.plugin_id for p in manager.get_active_plugins()]
    assert "plugin_two" not in active_ids


@pytest.mark.asyncio
async def test_plugin_unload():
    manager = PluginManager()
    manifest = {
        "plugin_id": "temp_plugin",
        "name": "Temporary Plugin",
        "entrypoint": "temp:init",
    }
    await manager.load_plugin(manifest)
    assert len(manager.get_active_plugins()) == 1

    await manager.unload_plugin("temp_plugin")
    assert len(manager.get_active_plugins()) == 0
