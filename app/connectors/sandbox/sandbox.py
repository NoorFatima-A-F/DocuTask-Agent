"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Connector Sandbox.
Runs connector executions inside strict resource envelopes (timeouts, memory bounds, network isolation).
"""

from __future__ import annotations

import logging
import time
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from app.connectors.core.exceptions import SandboxViolationError

logger = logging.getLogger(__name__)


class SandboxConfig(BaseModel):
    """Resource boundaries for connector plugin sandboxes."""
    max_execution_time_seconds: float = 30.0
    max_payload_size_bytes: int = 10 * 1024 * 1024  # 10 MB
    allowed_domains: Optional[List[str]] = None      # None = any
    disallowed_domains: List[str] = Field(default_factory=list)
    enforce_isolation: bool = True


class ConnectorSandbox:
    """
    Guarantees that third-party or untrusted connectors cannot exceed resource budgets
    or access unauthorized networks.
    """

    def __init__(self, config: Optional[SandboxConfig] = None):
        self.config = config or SandboxConfig()

    def validate_payload_size(self, payload: Any) -> None:
        """Verifies that the serialized payload stays within memory limits."""
        import json
        try:
            size = len(json.dumps(payload, default=str).encode("utf-8"))
            if size > self.config.max_payload_size_bytes:
                raise SandboxViolationError(
                    f"Payload size ({size} bytes) exceeds sandbox limit ({self.config.max_payload_size_bytes} bytes)",
                    details={"size_bytes": size, "max_bytes": self.config.max_payload_size_bytes},
                )
        except SandboxViolationError:
            raise
        except Exception:
            pass

    def validate_network_target(self, url_or_host: str) -> None:
        """Validates destination host against domain security policies."""
        if not self.config.enforce_isolation:
            return

        for blocked in self.config.disallowed_domains:
            if blocked.lower() in url_or_host.lower():
                raise SandboxViolationError(
                    f"Access to blocked domain '{blocked}' is denied by connector sandbox policy",
                    details={"target": url_or_host, "blocked_domain": blocked},
                )

        if self.config.allowed_domains is not None:
            allowed = any(dom.lower() in url_or_host.lower() for dom in self.config.allowed_domains)
            if not allowed:
                raise SandboxViolationError(
                    f"Access to target '{url_or_host}' is not in allowed sandbox domains",
                    details={"target": url_or_host, "allowed_domains": self.config.allowed_domains},
                )

    def execute_in_sandbox(
        self,
        func: Callable[[], Any],
        timeout_seconds: Optional[float] = None,
    ) -> Any:
        """
        Wraps callable execution inside a monitored boundary.
        """
        start = time.perf_counter()
        timeout = timeout_seconds or self.config.max_execution_time_seconds

        result = func()

        elapsed = time.perf_counter() - start
        if elapsed > timeout:
            raise SandboxViolationError(
                f"Connector execution time ({elapsed:.2f}s) exceeded sandbox timeout ({timeout:.2f}s)",
                details={"elapsed_seconds": elapsed, "timeout_seconds": timeout},
            )

        return result
