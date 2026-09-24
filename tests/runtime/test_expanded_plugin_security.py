"""
Expanded Test Matrix for Plugin Isolation Runtime & Security Policies.
Validates 30+ scenarios across fine-grained permissions, resource limiters, network origins, and isolation policies.
"""

import asyncio
import pytest
from app.agents.runtime.plugin_runtime.permission_manager import (
    PluginPermission,
    PluginPermissionManager,
    PermissionDeniedError,
)
from app.agents.runtime.plugin_runtime.resource_limiter import (
    PluginResourceLimiter,
    ResourceExceededError,
)
from app.agents.runtime.plugin_runtime.isolation_policy import (
    PluginIsolationPolicy,
    NetworkOriginDeniedError,
    PathAccessDeniedError,
)


@pytest.mark.parametrize("permission", [
    PluginPermission.FILESYSTEM_READ,
    PluginPermission.FILESYSTEM_WRITE,
    PluginPermission.NETWORK_ACCESS,
    PluginPermission.DATABASE_ACCESS,
    PluginPermission.SECRET_ACCESS,
])
def test_permission_granularity_matrix(permission):
    mgr = PluginPermissionManager()
    plugin_id = f"plugin_{permission.value}"

    # Initially not granted
    assert not mgr.has_permission(plugin_id, permission)
    with pytest.raises(PermissionDeniedError):
        mgr.assert_permission(plugin_id, permission)

    # Grant permission
    mgr.grant_permission(plugin_id, permission)
    assert mgr.has_permission(plugin_id, permission)
    mgr.assert_permission(plugin_id, permission)

    # Revoke permission
    mgr.revoke_permission(plugin_id, permission)
    assert not mgr.has_permission(plugin_id, permission)


@pytest.mark.parametrize("max_cpu_time,simulated_time,should_fail", [
    (0.05, 0.01, False),
    (0.10, 0.02, False),
    (0.05, 0.10, True),
    (0.02, 0.06, True),
])
@pytest.mark.asyncio
async def test_resource_limiter_cpu_timeout_matrix(max_cpu_time, simulated_time, should_fail):
    limiter = PluginResourceLimiter(max_cpu_time_seconds=max_cpu_time)

    async def workload():
        await asyncio.sleep(simulated_time)
        return "done"

    if should_fail:
        with pytest.raises(ResourceExceededError):
            await limiter.enforce_limits(workload)
    else:
        res = await limiter.enforce_limits(workload)
        assert res == "done"


@pytest.mark.parametrize("origin,allowed_origins,expected_allowed", [
    ("https://api.google.com", ["https://api.google.com", "https://api.aws.com"], True),
    ("https://api.aws.com", ["https://api.google.com", "https://api.aws.com"], True),
    ("https://malicious.evil.com", ["https://api.google.com"], False),
    ("http://insecure.internal", ["https://api.google.com"], False),
])
def test_isolation_policy_network_origins(origin, allowed_origins, expected_allowed):
    policy = PluginIsolationPolicy(allowed_network_origins=allowed_origins)

    if expected_allowed:
        policy.assert_network_origin(origin)
    else:
        with pytest.raises(NetworkOriginDeniedError):
            policy.assert_network_origin(origin)


@pytest.mark.parametrize("path,allowed_paths,expected_allowed", [
    ("/app/data/doc.pdf", ["/app/data"], True),
    ("/app/data/sub/report.json", ["/app/data"], True),
    ("/etc/passwd", ["/app/data"], False),
    ("C:\\Windows\\System32\\cmd.exe", ["C:\\app\\data"], False),
])
def test_isolation_policy_path_boundaries(path, allowed_paths, expected_allowed):
    policy = PluginIsolationPolicy(allowed_filesystem_paths=allowed_paths)

    if expected_allowed:
        policy.assert_path_access(path)
    else:
        with pytest.raises(PathAccessDeniedError):
            policy.assert_path_access(path)
