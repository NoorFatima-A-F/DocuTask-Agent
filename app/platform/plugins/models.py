"""
Platform Plugin Domain Models and Manifest Specification.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from ..kernel.versioning import SemanticVersion


class PluginType(str, Enum):
    """Plugin categories."""
    CONNECTOR = "CONNECTOR"
    AI = "AI"
    WORKFLOW = "WORKFLOW"
    SECURITY = "SECURITY"
    ANALYTICS = "ANALYTICS"
    UI = "UI"
    GENERAL = "GENERAL"


class PluginStatus(str, Enum):
    REGISTERED = "REGISTERED"
    VALIDATED = "VALIDATED"
    LOADED = "LOADED"
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    ERROR = "ERROR"


@dataclass
class PluginManifest:
    """Plugin declarative manifest descriptor."""
    id: str
    name: str
    version: SemanticVersion
    plugin_type: PluginType = PluginType.GENERAL
    author: str = ""
    description: str = ""
    entrypoint: str = ""
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    config_schema: Dict[str, Any] = field(default_factory=dict)
    min_platform_version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "version": str(self.version),
            "type": self.plugin_type.value,
            "author": self.author,
            "description": self.description,
            "entrypoint": self.entrypoint,
            "dependencies": self.dependencies,
            "capabilities": self.capabilities,
            "permissions": self.permissions,
            "config_schema": self.config_schema,
            "min_platform_version": self.min_platform_version,
        }


@dataclass
class PluginRecord:
    """Runtime tracking record of a plugin."""
    manifest: PluginManifest
    status: PluginStatus = PluginStatus.REGISTERED
    instance: Optional[Any] = None
    loaded_at: Optional[datetime] = None
    error_message: Optional[str] = None
    configuration: Dict[str, Any] = field(default_factory=dict)
