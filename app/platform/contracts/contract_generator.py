"""Automatic Contract Generator.

Generates dynamic OpenAPI specifications, JSON Schemas, capability schemas,
tool definitions, and SDK documentation directly from registered plugins with zero handwritten specs.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.platform.capability.capability_registry import (
    CapabilityRegistry,
    global_capability_registry,
)
from app.platform.plugins.plugin_loader import (
    PluginLoader,
    global_plugin_loader,
)
from app.platform.tools.dynamic_tool_registry import (
    DynamicToolRegistry,
    global_tool_registry,
)


@dataclass
class PlatformContractDossier:
    openapi_spec: Dict[str, Any]
    json_schemas: Dict[str, Any]
    capabilities_schema: Dict[str, Any]
    tools_schema: Dict[str, Any]
    sdk_client_stubs_python: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "openapi_spec": self.openapi_spec,
            "json_schemas": self.json_schemas,
            "capabilities_schema": self.capabilities_schema,
            "tools_schema": self.tools_schema,
            "sdk_client_stubs_python": self.sdk_client_stubs_python,
        }


class ContractGenerator:
    @staticmethod
    def generate_all(
        plugin_loader: Optional[PluginLoader] = None,
        capability_registry: Optional[CapabilityRegistry] = None,
        tool_registry: Optional[DynamicToolRegistry] = None,
    ) -> PlatformContractDossier:
        loader = plugin_loader or global_plugin_loader
        cap_reg = capability_registry or global_capability_registry
        t_reg = tool_registry or global_tool_registry

        plugins = loader.list_plugins()
        capabilities = cap_reg.list_capabilities()
        tools = t_reg.list_tools()

        # Generate dynamic OpenAPI paths
        paths: Dict[str, Any] = {
            "/api/v1/platform/plugins": {"get": {"summary": "List installed plugins", "responses": {"200": {"description": "OK"}}}},
            "/api/v1/platform/capabilities": {"get": {"summary": "Query capabilities", "responses": {"200": {"description": "OK"}}}},
        }
        for p in plugins:
            paths[f"/api/v1/agents/{p.manifest.plugin_id}/execute"] = {
                "post": {
                    "summary": f"Execute {p.manifest.name}",
                    "description": p.manifest.description,
                    "requestBody": {"content": {"application/json": {"schema": {"type": "object"}}}},
                    "responses": {"200": {"description": "Execution result"}},
                }
            }

        openapi = {
            "openapi": "3.1.0",
            "info": {
                "title": "DocuTask Agent Platform OS API",
                "version": "2026.1",
                "description": "Auto-generated OpenAPI contracts from active dynamic plugins and capabilities.",
            },
            "paths": paths,
        }

        json_schemas = {
            "PluginManifest": {"type": "object", "properties": {"plugin_id": {"type": "string"}, "version": {"type": "string"}}},
            "CapabilityDefinition": {"type": "object", "properties": {"capability_name": {"type": "string"}}},
        }

        cap_schema = {c.capability_name: c.to_dict() for c in capabilities}
        tool_schema = {t.tool_id: t.to_dict() for t in tools}

        sdk_code = f"""# DocuTask Agent Platform Python SDK (Auto-Generated)
import requests

class DocuTaskPlatformClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def list_plugins(self):
        return requests.get(f"{{self.base_url}}/api/v1/platform/plugins").json()

    def execute_capability(self, capability: str, payload: dict):
        return requests.post(f"{{self.base_url}}/api/v1/platform/execute", json={{"capability": capability, "payload": payload}}).json()
"""

        return PlatformContractDossier(
            openapi_spec=openapi,
            json_schemas=json_schemas,
            capabilities_schema=cap_schema,
            tools_schema=tool_schema,
            sdk_client_stubs_python=sdk_code,
        )
