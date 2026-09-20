"""
Platform Metadata Definitions and Models.
Defines structured metadata descriptors for Components, Services, Modules, and Plugins.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from .versioning import SemanticVersion


@dataclass(frozen=True)
class ComponentMetadata:
    """Universal metadata container for any kernel component."""
    name: str
    version: SemanticVersion = field(default_factory=lambda: SemanticVersion(1, 0, 0))
    description: str = ""
    author: str = "DocuTask Platform"
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": str(self.version),
            "description": self.description,
            "author": self.author,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "attributes": self.attributes,
        }


@dataclass(frozen=True)
class ModuleMetadata(ComponentMetadata):
    """Metadata specification for managed modules."""
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    events_published: List[str] = field(default_factory=list)
    events_subscribed: List[str] = field(default_factory=list)
    configuration_schema: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "dependencies": self.dependencies,
            "capabilities": self.capabilities,
            "permissions": self.permissions,
            "events_published": self.events_published,
            "events_subscribed": self.events_subscribed,
            "configuration_schema": self.configuration_schema,
        })
        return base


@dataclass(frozen=True)
class PluginMetadata(ComponentMetadata):
    """Metadata specification for dynamic plugins."""
    plugin_type: str = "general"
    entrypoint: str = ""
    required_permissions: List[str] = field(default_factory=list)
    sandbox_required: bool = True
    min_platform_version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "plugin_type": self.plugin_type,
            "entrypoint": self.entrypoint,
            "required_permissions": self.required_permissions,
            "sandbox_required": self.sandbox_required,
            "min_platform_version": self.min_platform_version,
        })
        return base


@dataclass(frozen=True)
class ServiceMetadata(ComponentMetadata):
    """Metadata specification for registered platform services."""
    module_owner: str = "core"
    endpoints: List[str] = field(default_factory=list)
    health_check_url: Optional[str] = None
    service_type: str = "internal"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base.update({
            "module_owner": self.module_owner,
            "endpoints": self.endpoints,
            "health_check_url": self.health_check_url,
            "service_type": self.service_type,
        })
        return base
