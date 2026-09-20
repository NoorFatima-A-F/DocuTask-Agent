"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - MCP Gateway.
Integrates Model Context Protocol (MCP) servers, tools, resources, and prompt templates
directly into the DocuTask Agent capability and tool registries.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from app.connectors.core.exceptions import MCPProtocolError
from app.connectors.core.models import ActionDescriptor, CapabilityDescriptor, ConnectorCategory
from app.connectors.registry.capability_registry import CapabilityRegistry

logger = logging.getLogger(__name__)


class MCPServerRegistration(BaseModel):
    """Metadata describing a registered Model Context Protocol (MCP) server."""
    server_id: str
    name: str
    endpoint_url: str
    transport: str = "sse"  # sse, stdio, websocket
    version: str = "1.0.0"
    authentication_token: Optional[str] = None
    tools_discovered: List[Dict[str, Any]] = Field(default_factory=list)
    resources_discovered: List[Dict[str, Any]] = Field(default_factory=list)
    prompts_discovered: List[Dict[str, Any]] = Field(default_factory=list)


class MCPGateway:
    """
    Gateway connecting DocuTask Agent runtime with external MCP servers.
    Seamlessly discovers MCP tools and promotes them into native platform capabilities.
    """

    def __init__(self, capability_registry: Optional[CapabilityRegistry] = None):
        self._capability_registry = capability_registry
        self._servers: Dict[str, MCPServerRegistration] = {}
        self._tool_handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    def register_server(
        self,
        server_id: str,
        name: str,
        endpoint_url: str,
        transport: str = "sse",
        auth_token: Optional[str] = None,
    ) -> MCPServerRegistration:
        """Registers an external MCP server."""
        reg = MCPServerRegistration(
            server_id=server_id,
            name=name,
            endpoint_url=endpoint_url,
            transport=transport,
            authentication_token=auth_token,
        )
        self._servers[server_id] = reg
        logger.info(f"Registered MCP server '{server_id}' ({endpoint_url})")
        return reg

    def discover_tools(
        self,
        server_id: str,
        tools_list: Optional[List[Dict[str, Any]]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Discovers tools exposed by an MCP server and binds them into platform capabilities.
        """
        server = self._servers.get(server_id)
        if not server:
            raise MCPProtocolError(f"MCP server '{server_id}' not found")

        # In real MCP, this queries JSON-RPC `tools/list`
        discovered = tools_list or [
            {
                "name": f"{server_id}_default_tool",
                "description": "Standard MCP tool execution",
                "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}}},
            }
        ]

        server.tools_discovered = discovered

        # Auto-bind into capability registry if attached
        if self._capability_registry:
            for t in discovered:
                cap_name = f"mcp.{server_id}.{t['name']}"
                self._capability_registry.register_capability(
                    CapabilityDescriptor(
                        name=cap_name,
                        category=ConnectorCategory.AI,
                        description=t.get("description", "MCP discovered tool"),
                        input_schema=t.get("inputSchema", {}),
                    )
                )

        logger.info(f"Discovered {len(discovered)} tools on MCP server '{server_id}'")
        return discovered

    def register_tool_handler(self, tool_name: str, handler: Callable[[Dict[str, Any]], Any]) -> None:
        """Registers an execution handler for an MCP tool."""
        self._tool_handlers[tool_name] = handler

    def invoke_mcp_tool(
        self,
        server_id: str,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Executes a tool on a registered MCP server.
        """
        server = self._servers.get(server_id)
        if not server:
            raise MCPProtocolError(f"MCP server '{server_id}' is not registered")

        if tool_name in self._tool_handlers:
            output = self._tool_handlers[tool_name](arguments)
            return {"status": "SUCCESS", "server_id": server_id, "tool": tool_name, "content": output}

        # Simulated standard MCP tool execution response
        return {
            "status": "SUCCESS",
            "server_id": server_id,
            "tool": tool_name,
            "content": [{"type": "text", "text": f"Executed MCP tool '{tool_name}' with args {arguments}"}],
        }
