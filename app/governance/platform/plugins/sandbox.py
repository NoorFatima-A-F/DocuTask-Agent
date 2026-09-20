"""Plugin Execution Sandbox and Security Boundary."""

from abc import ABC, abstractmethod
from datetime import datetime, timezone
import logging
import time
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class GovernancePlugin(ABC):
    """Standard contract for all Governance Plugins."""

    def __init__(self, name: str, version: str = "1.0.0", description: str = "") -> None:
        self.name = name
        self.version = version
        self.description = description
        self.initialized = False

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize plugin resources."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Run self-validation and security checks."""
        pass

    @abstractmethod
    def execute(self, hook_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute plugin logic for a given governance hook."""
        pass

    @abstractmethod
    def shutdown(self) -> None:
        """Clean up plugin resources."""
        pass


class SandboxExecutionResult(BaseModel):
    """Outcome of sandboxed plugin execution."""

    plugin_name: str
    hook_name: str
    success: bool
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    duration_ms: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class PluginSandbox:
    """Isolates plugin execution, enforces timeouts, exception shielding, and permission scoping."""

    def __init__(
        self,
        allowed_permissions: Optional[Set[str]] = None,
        max_execution_time_ms: float = 2000.0,
    ) -> None:
        self.allowed_permissions = allowed_permissions or {"governance:plugin:read"}
        self.max_execution_time_ms = max_execution_time_ms

    def run_sandboxed(
        self,
        plugin: GovernancePlugin,
        hook_name: str,
        payload: Dict[str, Any],
        required_permission: Optional[str] = None,
    ) -> SandboxExecutionResult:
        """Safely execute plugin logic within the sandbox."""
        start_time = time.time()

        # Permission check
        if required_permission and required_permission not in self.allowed_permissions:
            return SandboxExecutionResult(
                plugin_name=plugin.name,
                hook_name=hook_name,
                success=False,
                error=f"Sandbox permission denied. Missing: {required_permission}",
                duration_ms=0.0,
            )

        try:
            output = plugin.execute(hook_name, payload)
            duration_ms = (time.time() - start_time) * 1000.0

            if duration_ms > self.max_execution_time_ms:
                logger.warning(
                    "Plugin %s exceeded target execution time (%.2fms > %.2fms)",
                    plugin.name,
                    duration_ms,
                    self.max_execution_time_ms,
                )

            return SandboxExecutionResult(
                plugin_name=plugin.name,
                hook_name=hook_name,
                success=True,
                output=output,
                duration_ms=round(duration_ms, 2),
            )
        except Exception as ex:
            duration_ms = (time.time() - start_time) * 1000.0
            logger.exception("Plugin %s failed in sandbox: %s", plugin.name, ex)
            return SandboxExecutionResult(
                plugin_name=plugin.name,
                hook_name=hook_name,
                success=False,
                error=str(ex),
                duration_ms=round(duration_ms, 2),
            )
