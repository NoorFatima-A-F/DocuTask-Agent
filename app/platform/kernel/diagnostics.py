"""
Platform Kernel Diagnostics Protocols and Models.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass(frozen=True)
class DiagnosticReport:
    """Comprehensive platform diagnostic report structure."""
    platform_version: str
    build_version: str
    git_commit: str
    status: str = "HEALTHY"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    loaded_modules: List[str] = field(default_factory=list)
    loaded_plugins: List[str] = field(default_factory=list)
    active_services: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    infrastructure_status: Dict[str, Any] = field(default_factory=dict)
    system_metrics: Dict[str, Any] = field(default_factory=dict)
    configuration_summary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "platform_version": self.platform_version,
            "build_version": self.build_version,
            "git_commit": self.git_commit,
            "status": self.status,
            "timestamp": self.timestamp.isoformat(),
            "loaded_modules": self.loaded_modules,
            "loaded_plugins": self.loaded_plugins,
            "active_services": self.active_services,
            "capabilities": self.capabilities,
            "infrastructure_status": self.infrastructure_status,
            "system_metrics": self.system_metrics,
            "configuration_summary": self.configuration_summary,
        }


class IDiagnosticProvider(ABC):
    """Protocol for components providing diagnostic information."""

    @abstractmethod
    async def provide_diagnostics(self) -> Dict[str, Any]:
        """Collect and return component diagnostic metadata."""
        pass
