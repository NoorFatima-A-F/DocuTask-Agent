"""
Tests for MarketplaceRegistry, ConnectorCertification, MCPGateway, and ProtocolAdapters.
"""

import pytest
from app.connectors.adapters.base import GraphQLAdapter, RESTAdapter, SOAPAdapter, gRPCAdapter
from app.connectors.certification.framework import ConnectorCertification
from app.connectors.core.models import ConnectorCategory
from app.connectors.marketplace.registry import ConnectorPackageManifest, MarketplaceRegistry
from app.connectors.mcp.gateway import MCPGateway
from app.connectors.registry.capability_registry import CapabilityRegistry
from app.connectors.registry.connector_registry import ConnectorRegistry


def test_marketplace_browse_install_and_upgrade():
    conn_reg = ConnectorRegistry()
    marketplace = MarketplaceRegistry(conn_reg)

    # Browse packages
    pkgs = marketplace.browse(category=ConnectorCategory.COMMUNICATION)
    assert len(pkgs) >= 2

    # Install package
    installed_conn = marketplace.install("pkg-slack-collaboration", organization_id="org-acme")
    assert installed_conn.id == "conn-slack-collaboration"
    assert conn_reg.get("conn-slack-collaboration").name == "Slack Workspace"

    # Publish updated package
    marketplace.publish_package(
        ConnectorPackageManifest(
            package_id="pkg-slack-collaboration",
            name="Slack Workspace",
            vendor="Slack",
            version="1.9.0",
            category=ConnectorCategory.COMMUNICATION,
            capabilities=["message.send", "message.read"],
            permissions_required=["chat.write"],
        )
    )

    # Upgrade installed package
    upgraded = marketplace.upgrade("pkg-slack-collaboration")
    assert upgraded is not None
    assert upgraded.version == "1.9.0"


def test_connector_certification_audit_pipeline():
    cert = ConnectorCertification()

    # Valid package
    good_manifest = ConnectorPackageManifest(
        package_id="pkg-certified-hubspot",
        name="HubSpot Certified",
        vendor="HubSpot Inc",
        version="1.0.0",
        description="Comprehensive enterprise CRM connector supporting contact syncing.",
        capabilities=["crm.contact.create", "crm.contact.get"],
        permissions_required=["crm.objects.contacts.read", "crm.objects.contacts.write"],
    )
    report = cert.certify(good_manifest)
    assert report.certified is True
    assert report.score >= 80.0

    # Insecure package missing permissions
    bad_manifest = ConnectorPackageManifest(
        package_id="pkg-insecure-scraper",
        name="Scraper",
        vendor="Unknown",
        version="0.1.0",
        description="Short",
        capabilities=[],
        permissions_required=[],
    )
    bad_report = cert.certify(bad_manifest)
    assert bad_report.certified is False
    assert len(bad_report.findings) > 0


def test_mcp_gateway_discovery_and_invocation():
    cap_reg = CapabilityRegistry()
    mcp = MCPGateway(capability_registry=cap_reg)

    # Register external MCP server
    mcp.register_server(
        server_id="mcp-server-database",
        name="Postgres MCP Server",
        endpoint_url="http://localhost:8080/sse",
    )

    # Discover tools
    discovered = mcp.discover_tools(
        server_id="mcp-server-database",
        tools_list=[
            {
                "name": "query_records",
                "description": "Execute read-only SQL query",
                "inputSchema": {"type": "object", "required": ["sql"]},
            }
        ],
    )
    assert len(discovered) == 1

    # Verify capability was auto-registered
    cap = cap_reg.get_capability("mcp.mcp-server-database.query_records")
    assert cap is not None
    assert cap.name == "mcp.mcp-server-database.query_records"

    # Register execution handler and invoke tool
    mcp.register_tool_handler(
        "query_records",
        lambda args: {"rows": [{"id": 1, "name": "Document A"}]},
    )

    result = mcp.invoke_mcp_tool(
        server_id="mcp-server-database",
        tool_name="query_records",
        arguments={"sql": "SELECT * FROM docs;"},
    )
    assert result["status"] == "SUCCESS"
    assert len(result["content"]["rows"]) == 1


def test_protocol_adapters():
    rest = RESTAdapter()
    res_rest = rest.call("https://api.example.com/v1/users", {"user_id": 101})
    assert res_rest["protocol"] == "REST"
    assert res_rest["status_code"] == 200

    graphql = GraphQLAdapter()
    res_gql = graphql.call("https://api.example.com/graphql", {"query": "query { me { name } }"})
    assert res_gql["protocol"] == "GraphQL"

    soap = SOAPAdapter()
    res_soap = soap.call("https://ws.example.com/Service", {"soap_action": "GetCustomer", "body": {"id": 5}})
    assert res_soap["protocol"] == "SOAP"

    grpc = gRPCAdapter()
    res_grpc = grpc.call("grpc.example.com:50051", {"method": "UserService/GetUser", "message": {"id": 5}})
    assert res_grpc["protocol"] == "gRPC"
