"""
Enterprise Plugin Loader & Manifest Engine.
Parses and validates PluginManifest models supporting version compatibility, dependencies,
required services, and permission schemas.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.agents.runtime.exceptions import PluginValidationError


class PluginState(str, Enum):
    """Full 8-state plugin lifecycle."""
    DISCOVERED = "DISCOVERED"
    VALIDATED = "VALIDATED"
    LOADED = "LOADED"
    REGISTERED = "REGISTERED"
    ACTIVATED = "ACTIVATED"
    RUNNING = "RUNNING"
    DISABLED = "DISABLED"
    UNLOADED = "UNLOADED"


class PluginManifest(BaseModel):
    """Complete enterprise specification for a runtime plugin."""
    plugin_id: str
    name: str
    version: str = "1.0.0"
    author: str = "Enterprise Architecture"
    api_version: str = "23.0"
    entrypoint: str
    dependencies: List[str] = Field(default_factory=list)
    required_services: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    capabilities: List[str] = Field(default_factory=list)
    enabled: bool = True
    config: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"frozen": True}


class PluginValidator:
    """Validates plugin manifest schemas and version constraints."""

    SUPPORTED_API_VERSIONS = {"23.0", "23.1", "24.0"}

    @classmethod
    def validate_manifest(cls, manifest: PluginManifest) -> None:
        """Enforces schema requirements and API version constraints."""
        if not manifest.plugin_id or not manifest.plugin_id.strip():
            raise PluginValidationError("Plugin manifest 'plugin_id' cannot be empty.")
        if not manifest.name or not manifest.name.strip():
            raise PluginValidationError("Plugin manifest 'name' cannot be empty.")
        if not manifest.entrypoint or not manifest.entrypoint.strip():
            raise PluginValidationError("Plugin manifest 'entrypoint' cannot be empty.")
        if manifest.api_version not in cls.SUPPORTED_API_VERSIONS:
            raise PluginValidationError(
                f"Plugin '{manifest.name}' specifies unsupported api_version '{manifest.api_version}'. "
                f"Supported: {cls.SUPPORTED_API_VERSIONS}"
            )


class PluginLoader:
    """Loads and verifies plugin descriptors."""

    def __init__(self, validator: Optional[PluginValidator] = None) -> None:
        self.validator = validator or PluginValidator()

    def validate_manifest(self, manifest: PluginManifest) -> None:
        """Validates plugin manifest."""
        self.validator.validate_manifest(manifest)

    def load_from_dict(self, data: Dict[str, Any]) -> PluginManifest:
        """Parses dictionary payload into validated PluginManifest."""
        try:
            manifest = PluginManifest.model_validate(data)
            self.validate_manifest(manifest)
            return manifest
        except Exception as e:
            if isinstance(e, PluginValidationError):
                raise
            raise PluginValidationError(f"Malformed plugin manifest: {e}") from e
