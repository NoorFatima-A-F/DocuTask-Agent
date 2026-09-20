"""
Platform Plugin Validator.
"""

from typing import Any, Dict
from .models import PluginManifest
from ..kernel.exceptions import PluginException
from ..kernel.versioning import SemanticVersion


class PluginValidator:
    """Validates plugin manifests, versions, and security permissions."""

    @staticmethod
    def validate_manifest(manifest: PluginManifest) -> None:
        """Validate required fields in plugin manifest."""
        if not manifest.id or not manifest.id.strip():
            raise PluginException("Plugin manifest missing 'id'")
        if not manifest.name or not manifest.name.strip():
            raise PluginException("Plugin manifest missing 'name'")
        if not isinstance(manifest.version, SemanticVersion):
            raise PluginException("Plugin manifest version must be SemanticVersion")

    @staticmethod
    def validate_permissions(manifest: PluginManifest, allowed_permissions: set) -> None:
        """Verify that requested plugin permissions are within acceptable boundaries."""
        unauthorized = set(manifest.permissions) - allowed_permissions
        if unauthorized:
            raise PluginException(f"Plugin '{manifest.id}' requested unauthorized permissions: {unauthorized}")
