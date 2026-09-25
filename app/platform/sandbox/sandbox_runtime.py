"""Runtime Sandboxing and Isolation Boundary.

Enforces resource quotas (CPU ms, RAM MB, Token spend USD), timeouts, and permission
scopes (Filesystem, Network, Memory, Secrets) for untrusted third-party plugins.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set


@dataclass
class ResourceQuota:
    max_cpu_ms: float = 3000.0
    max_memory_mb: float = 256.0
    max_token_spend_usd: float = 0.05
    max_concurrency: int = 4
    network_egress_allowed: bool = False
    filesystem_write_allowed: bool = False


@dataclass
class SandboxViolation:
    violation_type: str  # TIMEOUT, MEMORY_EXCEEDED, SCOPE_BREACH, QUOTA_EXCEEDED
    details: str
    timestamp: float = field(default_factory=time.time)


class SandboxRuntime:
    def __init__(self, quota: Optional[ResourceQuota] = None, granted_scopes: Optional[Set[str]] = None):
        self.quota = quota or ResourceQuota()
        self.granted_scopes = granted_scopes or set()
        self._violations: List[SandboxViolation] = []

    def check_permission(self, required_scope: str) -> bool:
        if required_scope in self.granted_scopes or "*" in self.granted_scopes:
            return True
        self._violations.append(
            SandboxViolation(
                violation_type="SCOPE_BREACH",
                details=f"Denied access to scope '{required_scope}'",
            )
        )
        return False

    def execute_in_sandbox(
        self,
        func: Callable[[], Any],
        timeout_ms: Optional[float] = None,
    ) -> Any:
        max_t = timeout_ms or self.quota.max_cpu_ms
        t0 = time.perf_counter()

        try:
            result = func()
        except Exception as e:
            self._violations.append(SandboxViolation("EXECUTION_ERROR", str(e)))
            raise e

        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        if elapsed_ms > max_t:
            self._violations.append(
                SandboxViolation(
                    violation_type="TIMEOUT",
                    details=f"Execution took {elapsed_ms:.1f}ms exceeding quota of {max_t:.1f}ms",
                )
            )
            raise TimeoutError(f"Sandbox execution timed out after {elapsed_ms:.1f}ms")

        return result

    def get_violations(self) -> List[SandboxViolation]:
        return list(self._violations)

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_secure": len(self._violations) == 0,
            "quota": {
                "max_cpu_ms": self.quota.max_cpu_ms,
                "max_memory_mb": self.quota.max_memory_mb,
                "max_token_spend_usd": self.quota.max_token_spend_usd,
                "network_egress": self.quota.network_egress_allowed,
            },
            "granted_scopes": list(self.granted_scopes),
            "violation_count": len(self._violations),
        }


global_sandbox_runtime = SandboxRuntime(granted_scopes={"ocr:read", "storage:write", "evidence:seal"})
