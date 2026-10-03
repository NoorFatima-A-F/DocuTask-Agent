"""
Platform Versioning and Compatibility Matrix.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from ..container import DependencyContainer
from ...platform.kernel.versioning import SemanticVersion, VersionRange


@dataclass(frozen=True)
class APIVersionInfo:
    """API version metadata."""
    version: str
    status: str = "CURRENT"  # CURRENT, DEPRECATED, SUNSET
    sunset_date: Optional[str] = None
    compatible_clients: List[str] = field(default_factory=list)


class PlatformCompatibilityMatrix:
    """Evaluates cross-module and client-platform semantic version compatibility."""

    PLATFORM_VERSION = SemanticVersion(2, 0, 0)
    MIN_SUPPORTED_SDK_VERSION = SemanticVersion(1, 0, 0)

    def __init__(self):
        self._api_versions: Dict[str, APIVersionInfo] = {
            "v1": APIVersionInfo(version="v1", status="CURRENT"),
            "v2": APIVersionInfo(version="v2", status="CURRENT"),
        }
        self._module_compatibility: Dict[str, VersionRange] = {}

    def register_module_compatibility(self, module_name: str, required_range: VersionRange) -> None:
        """Register required platform version range for a module."""
        self._module_compatibility[module_name] = required_range

    def is_module_compatible(self, module_name: str, platform_version: Optional[SemanticVersion] = None) -> bool:
        """Check if a module is compatible with platform version."""
        p_ver = platform_version or self.PLATFORM_VERSION
        req_range = self._module_compatibility.get(module_name)
        if not req_range:
            return True
        return req_range.satisfies(p_ver)

    def is_sdk_compatible(self, sdk_version: str) -> bool:
        """Check if external client SDK version is supported."""
        try:
            parsed = SemanticVersion.parse(sdk_version)
            return parsed >= self.MIN_SUPPORTED_SDK_VERSION
        except Exception:
            return False
