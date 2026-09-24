"""Plugin Manifest Parser and Validator."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class PluginManifest:
    plugin_id: str
    name: str
    version: str
    author: str
    description: str
    entry_point: str
    capabilities_provided: List[str] = field(default_factory=list)
    capabilities_required: List[str] = field(default_factory=list)
    dependencies: Dict[str, str] = field(default_factory=dict)
    permission_scopes: List[str] = field(default_factory=list)
    default_config: Dict[str, Any] = field(default_factory=dict)
    schema_version: str = "2026.1"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plugin_id": self.plugin_id,
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "entry_point": self.entry_point,
            "capabilities_provided": self.capabilities_provided,
            "capabilities_required": self.capabilities_required,
            "dependencies": self.dependencies,
            "permission_scopes": self.permission_scopes,
            "default_config": self.default_config,
            "schema_version": self.schema_version,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> PluginManifest:
        return cls(
            plugin_id=data.get("plugin_id", "unknown_plugin"),
            name=data.get("name", "Unnamed Plugin"),
            version=data.get("version", "1.0.0"),
            author=data.get("author", "Community"),
            description=data.get("description", ""),
            entry_point=data.get("entry_point", "plugin.main"),
            capabilities_provided=data.get("capabilities_provided", []),
            capabilities_required=data.get("capabilities_required", []),
            dependencies=data.get("dependencies", {}),
            permission_scopes=data.get("permission_scopes", []),
            default_config=data.get("default_config", {}),
            schema_version=data.get("schema_version", "2026.1"),
        )
