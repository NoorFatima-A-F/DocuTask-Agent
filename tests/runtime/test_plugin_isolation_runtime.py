"""
Plugin Isolation Runtime Test Suite.
Validates:
- Logical permission enforcement and rejection of unauthorized permissions
- Resource limits (CPU timeout)
- Network egress isolation policy
- Sandbox providers (LocalRestrictedSandbox, DockerSandbox, WasmSandbox)
"""

import asyncio
import pytest
from app.agents.runtime.exceptions import PluginValidationError
from app.agents.runtime.plugin_runtime.isolation_policy import PluginIsolationPolicy
from app.agents.runtime.plugin_runtime.permission_manager import (
    PluginPermission,
    PluginPermissionManager,
)
from app.agents.runtime.plugin_runtime.plugin_executor import PluginExecutor
from app.agents.runtime.plugin_runtime.resource_limiter import (
    PluginResourceLimitExceededError,
    PluginResourceLimiter,
)
from app.agents.runtime.plugin_runtime.sandbox_provider import (
    DockerSandbox,
    LocalRestrictedSandbox,
    WasmSandbox,
)


@pytest.mark.asyncio
async def test_plugin_permission_denied():
    perm_mgr = PluginPermissionManager(
        allowed_permissions={PluginPermission.FILESYSTEM_READ, PluginPermission.DATABASE_ACCESS}
    )
    executor = PluginExecutor(permission_manager=perm_mgr)

    async def dummy_action():
        return "done"

    # Authorized permissions pass
    res = await executor.execute("p1", dummy_action, declared_permissions=["filesystem.read"])
    assert res == "done"

    # Unauthorized permission rejected
    with pytest.raises(PluginValidationError) as exc_info:
        await executor.execute("p2", dummy_action, declared_permissions=["secret.access"])
    assert "unauthorized security permissions" in str(exc_info.value)


@pytest.mark.asyncio
async def test_plugin_resource_limit():
    limiter = PluginResourceLimiter(max_execution_time_seconds=0.05)
    executor = PluginExecutor(resource_limiter=limiter)

    async def infinite_loop():
        await asyncio.sleep(0.2)
        return "finished"

    with pytest.raises(PluginResourceLimitExceededError) as exc_info:
        await executor.execute("slow_plugin", infinite_loop)
    assert "exceeded CPU time limit" in str(exc_info.value)


def test_plugin_network_restriction():
    policy = PluginIsolationPolicy(allowed_network_hosts=["api.ocr-service.internal", "storage.internal"])

    # Allowed host passes
    policy.verify_network_access("api.ocr-service.internal")

    # Unauthorized host rejected
    with pytest.raises(PluginValidationError) as exc_info:
        policy.verify_network_access("malicious-exfiltration.com")
    assert "Network egress violation" in str(exc_info.value)


@pytest.mark.asyncio
async def test_sandbox_providers():
    policy = PluginIsolationPolicy()

    async def work():
        return 123

    local_sb = LocalRestrictedSandbox()
    assert await local_sb.execute_plugin(work, policy) == 123

    docker_sb = DockerSandbox()
    assert await docker_sb.execute_plugin(work, policy) == 123

    wasm_sb = WasmSandbox()
    assert await wasm_sb.execute_plugin(work, policy) == 123
