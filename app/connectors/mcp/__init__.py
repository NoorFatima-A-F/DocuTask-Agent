"""
Enterprise Integration Fabric - MCP package.
"""

from app.connectors.mcp.gateway import MCPGateway, MCPServerRegistration

__all__ = [
    "MCPGateway",
    "MCPServerRegistration",
]
