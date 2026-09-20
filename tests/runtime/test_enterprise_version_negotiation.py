"""
Enterprise Version Negotiation Test Suite.
Validates:
- Semantic version parsing (major, minor, patch)
- Breaking major version incompatibility rejection
- Compatible minor/patch version registration
- RuntimeVersionManager catalog inspection
"""

import pytest
from app.agents.runtime.enterprise.compatibility_checker import VersionCompatibilityChecker
from app.agents.runtime.enterprise.version_manager import (
    IncompatibleVersionError,
    RuntimeVersionManager,
)


def test_semver_parsing():
    assert VersionCompatibilityChecker.parse_semver("23.1.4") == (23, 1, 4)
    assert VersionCompatibilityChecker.parse_semver("23") == (23, 0, 0)
    assert VersionCompatibilityChecker.parse_semver("23.2") == (23, 2, 0)


def test_version_compatibility_rules():
    # Matching major, same minor -> compatible
    assert VersionCompatibilityChecker.is_compatible("23.0.0", "23.0.1")
    # Matching major, within +1 minor -> compatible
    assert VersionCompatibilityChecker.is_compatible("23.0.0", "23.1.0")
    # Different major -> incompatible
    assert not VersionCompatibilityChecker.is_compatible("23.0.0", "24.0.0")
    assert not VersionCompatibilityChecker.is_compatible("23.0.0", "22.0.0")
    # Way ahead minor -> incompatible
    assert not VersionCompatibilityChecker.is_compatible("23.0.0", "23.5.0")


def test_version_manager_registration():
    mgr = RuntimeVersionManager(current_runtime_version="23.0.0")

    # Register compatible components
    assert mgr.register_component_version("workflow_engine", "23.0.2")
    assert mgr.register_component_version("reflection_engine", "23.1.0")

    assert mgr.get_version("workflow_engine") == "23.0.2"
    assert mgr.get_version("reflection_engine") == "23.1.0"
    assert "workflow_engine" in mgr.list_components()

    # Reject incompatible major version
    with pytest.raises(IncompatibleVersionError) as exc_info:
        mgr.register_component_version("future_module", "24.0.0")
    assert "is incompatible with Runtime v23.0.0" in str(exc_info.value)
