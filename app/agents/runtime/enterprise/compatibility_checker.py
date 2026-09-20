"""
Runtime Version Compatibility Checker.
Validates semantic version compatibility between the platform runtime kernel and subsystem modules or plugins.
"""

from typing import Tuple


class VersionCompatibilityChecker:
    """Semantic version comparison and compatibility checker."""

    @staticmethod
    def parse_semver(v_str: str) -> Tuple[int, int, int]:
        """Parses version string into (major, minor, patch)."""
        parts = v_str.strip().split(".")
        major = int(parts[0]) if len(parts) > 0 else 1
        minor = int(parts[1]) if len(parts) > 1 else 0
        patch = int(parts[2]) if len(parts) > 2 else 0
        return (major, minor, patch)

    @classmethod
    def is_compatible(cls, runtime_version: str, component_version: str) -> bool:
        """
        Determines if a component version is compatible with the runtime version.
        Rule: Major versions must match; component minor version must not exceed runtime minor version.
        """
        r_major, r_minor, _ = cls.parse_semver(runtime_version)
        c_major, c_minor, _ = cls.parse_semver(component_version)

        if r_major != c_major:
            return False  # Breaking major change
        return c_minor <= r_minor + 1  # Allows forward minor compatibility within 1 release
