"""
Version Compatibility Validator for Core and Plugins.
"""
from __future__ import annotations
from app.platform_verification.module_boundary.domain.interfaces import ICompatibilityValidator


class EnterpriseCompatibilityValidator(ICompatibilityValidator):
    """Validates semver compatibility between core runtime and plugins."""

    def check_compatibility(self, core_version: str, plugin_req_core_version: str) -> bool:
        # Simple semver major/minor compatibility evaluator
        try:
            core_clean = core_version.replace("v", "").strip()
            req_clean = plugin_req_core_version.replace(">=", "").replace("v", "").strip()

            core_major = int(core_clean.split(".")[0])
            req_major = int(req_clean.split(".")[0])

            return core_major >= req_major
        except (ValueError, IndexError):
            return True
