"""Tests for Governance Plugin Framework, Lifecycle State Machine, and Sandboxing."""

from typing import Any, Dict
import pytest
from app.governance.platform.plugins.lifecycle import (
    PluginLifecycleStateMachine,
    PluginState,
)
from app.governance.platform.plugins.manager import PluginManager
from app.governance.platform.plugins.sandbox import (
    GovernancePlugin,
    PluginSandbox,
)


class MockDLPPlugin(GovernancePlugin):
    """Mock DLP Plugin for testing."""

    def __init__(self) -> None:
        super().__init__(name="MockDLP", version="1.0.0", description="Mock Data Loss Prevention")
        self.config: Dict[str, Any] = {}

    def initialize(self, config: Dict[str, Any]) -> None:
        self.config = config

    def validate(self) -> bool:
        return True

    def execute(self, hook_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        if "secret" in payload.get("text", "").lower():
            return {"violation": True, "reason": "Secret detected in payload"}
        return {"violation": False}

    def shutdown(self) -> None:
        self.config = {}


def test_plugin_lifecycle_state_machine():
    assert PluginLifecycleStateMachine.can_transition(PluginState.REGISTERED, PluginState.VALIDATED) is True
    assert PluginLifecycleStateMachine.can_transition(PluginState.REGISTERED, PluginState.ACTIVE) is False

    with pytest.raises(ValueError, match="Invalid plugin lifecycle transition"):
        PluginLifecycleStateMachine.transition(PluginState.REGISTERED, PluginState.ACTIVE)


def test_plugin_sandbox_execution_and_permissions():
    plugin = MockDLPPlugin()
    plugin.initialize({"mode": "strict"})

    sandbox = PluginSandbox(allowed_permissions={"governance:plugin:read"})

    # Successful execution
    res1 = sandbox.run_sandboxed(plugin, "on_prompt", {"text": "Hello world"})
    assert res1.success is True
    assert res1.output["violation"] is False

    # Detection in payload
    res2 = sandbox.run_sandboxed(plugin, "on_prompt", {"text": "My SECRET key is 123"})
    assert res2.success is True
    assert res2.output["violation"] is True

    # Denied permission test
    res3 = sandbox.run_sandboxed(
        plugin,
        "on_prompt",
        {"text": "Hello"},
        required_permission="governance:admin:write",
    )
    assert res3.success is False
    assert "permission denied" in res3.error


def test_plugin_manager_full_lifecycle_and_hook_dispatch():
    manager = PluginManager()
    plugin = MockDLPPlugin()

    # 1. Register
    meta = manager.register(
        plugin=plugin,
        owner="sec_team",
        tenant_id="tenant_beta",
        permissions={"governance:plugin:read"},
    )
    assert meta.state == PluginState.REGISTERED

    # 2. Validate
    v_meta = manager.validate(meta.plugin_id)
    assert v_meta.state == PluginState.VALIDATED

    # 3. Approve
    a_meta = manager.approve(meta.plugin_id)
    assert a_meta.state == PluginState.APPROVED

    # 4. Activate
    act_meta = manager.activate(meta.plugin_id, {"mode": "live"})
    assert act_meta.state == PluginState.ACTIVE
    assert plugin.initialized is True

    # 5. Dispatch hook
    results = manager.dispatch_hook(
        hook_name="on_input",
        payload={"text": "Here is confidential secret data"},
        tenant_id="tenant_beta",
    )
    assert len(results) == 1
    assert results[0].output["violation"] is True

    # 6. Disable
    d_meta = manager.disable(meta.plugin_id)
    assert d_meta.state == PluginState.DISABLED

    # 7. Remove
    assert manager.remove(meta.plugin_id) is True
