# ADR-048: Model Context Protocol (MCP) Gateway Integration

## Status
Accepted

## Context
Anthropic's Model Context Protocol (MCP) has emerged as an open standard for AI models to discover tools, query resources, and access structured prompts. DocuTask Agent must support MCP servers natively without fragmenting its existing capability and tool registries.

## Decision
We implement the `MCPGateway` within the Universal Connector Platform. The gateway:
1. Connects to external MCP servers over SSE, stdio, or WebSocket transports.
2. Discovers MCP tools and maps them directly into the platform `CapabilityRegistry` and `ToolRegistry` with `mcp.<server>.<tool>` naming taxonomy.
3. Dispatches agent tool calls through the standardized MCP JSON-RPC protocol.

## Consequences
- AI agents and workflows can seamlessly discover and invoke any MCP-compliant server.
- Standardizes both traditional enterprise APIs and modern LLM MCP tools under a single governance plane.
