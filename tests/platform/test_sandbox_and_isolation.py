"""Tests for Sandbox Runtime and Resource Quota Isolation."""

import pytest
import time
from app.platform.sandbox.sandbox_runtime import (
    ResourceQuota,
    SandboxRuntime,
)


def test_sandbox_permissions_and_timeouts():
    sandbox = SandboxRuntime(
        quota=ResourceQuota(max_cpu_ms=50.0),
        granted_scopes={"ocr:read"},
    )

    assert sandbox.check_permission("ocr:read") is True
    assert sandbox.check_permission("admin:root") is False
    assert len(sandbox.get_violations()) == 1

    # Fast execution succeeds
    val = sandbox.execute_in_sandbox(lambda: 42 * 2)
    assert val == 84

    # Timeout execution fails
    def slow_func():
        time.sleep(0.08)
        return "done"

    with pytest.raises(TimeoutError):
        sandbox.execute_in_sandbox(slow_func)

    assert any(v.violation_type == "TIMEOUT" for v in sandbox.get_violations())
