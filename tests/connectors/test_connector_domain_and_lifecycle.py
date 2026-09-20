"""
Tests for Connector Platform Domain Models, Lifecycle State Machine, and Connector SDK.
"""

import pytest
from app.connectors.core.exceptions import InvalidConnectorStateError
from app.connectors.core.models import (
    ActionDescriptor,
    AuthType,
    CapabilityDescriptor,
    Connector,
    ConnectorCategory,
    ConnectorHealth,
    ConnectorStatus,
)
from app.connectors.lifecycle.manager import ConnectorLifecycleManager
from app.connectors.sdk.base import BaseConnector
from app.connectors.sdk.builder import ConnectorBuilder


def test_connector_domain_model_creation():
    connector = Connector(
        id="conn-test-crm",
        name="Test CRM",
        vendor="Acme",
        version="1.2.0",
        category=ConnectorCategory.CRM,
        capabilities=["crm.contact.create", "crm.contact.get"],
        authentication_types=[AuthType.OAUTH2, AuthType.API_KEY],
        supported_regions=["us-east-1", "eu-west-1"],
        status=ConnectorStatus.DISCOVERED,
    )

    assert connector.id == "conn-test-crm"
    assert connector.vendor == "Acme"
    assert len(connector.capabilities) == 2
    assert connector.health == ConnectorHealth.HEALTHY
    assert connector.status == ConnectorStatus.DISCOVERED


def test_connector_lifecycle_fsm_valid_flow():
    events_log = []
    manager = ConnectorLifecycleManager(event_listener=lambda e: events_log.append(e))

    connector = Connector(
        id="conn-lifecycle-test",
        name="Lifecycle Test",
        vendor="TestVendor",
        category=ConnectorCategory.COMMUNICATION,
    )

    assert connector.status == ConnectorStatus.DISCOVERED

    # DISCOVERED -> INSTALLED
    manager.transition(connector, ConnectorStatus.INSTALLED, reason="Installed from marketplace")
    assert connector.status == ConnectorStatus.INSTALLED

    # INSTALLED -> CONFIGURED
    manager.transition(connector, ConnectorStatus.CONFIGURED, reason="Tenant config provided")
    assert connector.status == ConnectorStatus.CONFIGURED

    # CONFIGURED -> AUTHENTICATED
    manager.transition(connector, ConnectorStatus.AUTHENTICATED, reason="OAuth tokens verified")
    assert connector.status == ConnectorStatus.AUTHENTICATED

    # AUTHENTICATED -> VALIDATED
    manager.transition(connector, ConnectorStatus.VALIDATED, reason="Ping test successful")
    assert connector.status == ConnectorStatus.VALIDATED

    # VALIDATED -> READY
    manager.transition(connector, ConnectorStatus.READY, reason="Ready for traffic")
    assert connector.status == ConnectorStatus.READY

    # READY -> ACTIVE
    manager.transition(connector, ConnectorStatus.ACTIVE, reason="Workflows actively executing")
    assert connector.status == ConnectorStatus.ACTIVE

    # ACTIVE -> DISABLED
    manager.transition(connector, ConnectorStatus.DISABLED, reason="Maintenance window")
    assert connector.status == ConnectorStatus.DISABLED

    # DISABLED -> ACTIVE
    manager.transition(connector, ConnectorStatus.ACTIVE, reason="Re-enabled")
    assert connector.status == ConnectorStatus.ACTIVE

    # Verify history & metrics
    history = manager.get_history(connector.id)
    assert len(history) == 8
    assert len(events_log) == 8

    metrics = manager.get_metrics()
    assert metrics[ConnectorStatus.ACTIVE.value] == 2
    assert metrics[ConnectorStatus.INSTALLED.value] == 1


def test_connector_lifecycle_illegal_transition():
    manager = ConnectorLifecycleManager()
    connector = Connector(
        id="conn-illegal-test",
        name="Illegal Test",
        vendor="TestVendor",
        status=ConnectorStatus.DISCOVERED,
    )

    # Cannot transition directly from DISCOVERED to ACTIVE
    with pytest.raises(InvalidConnectorStateError) as exc_info:
        manager.transition(connector, ConnectorStatus.ACTIVE)

    assert "Illegal transition" in str(exc_info.value)
    assert connector.status == ConnectorStatus.DISCOVERED


def test_connector_builder_sdk():
    builder = (
        ConnectorBuilder(connector_id="conn-slack-custom", name="Custom Slack")
        .with_vendor("Slack Technologies")
        .with_version("2.0.0")
        .with_category(ConnectorCategory.COMMUNICATION)
        .with_auth_type(AuthType.BEARER)
        .with_capability(
            name="message.send",
            category=ConnectorCategory.COMMUNICATION,
            description="Send a message to a channel",
            input_schema={"required": ["channel", "text"]},
        )
        .with_action(
            name="send_message",
            capability="message.send",
            handler=lambda inputs: {"sent": True, "channel": inputs.get("channel")},
            cost_usd=0.002,
        )
        .with_auth_validator(lambda creds: "token" in creds or "access_token" in creds)
        .with_connection_validator(lambda: True)
    )

    connector_plugin = builder.build()
    meta = connector_plugin.metadata()

    assert meta.id == "conn-slack-custom"
    assert meta.vendor == "Slack Technologies"
    assert meta.version == "2.0.0"
    assert "message.send" in meta.capabilities

    # Test authentication
    assert connector_plugin.authenticate({"token": "xoxb-12345"}) is True
    assert connector_plugin.authenticate({}) is False

    # Test connection validation & health check
    assert connector_plugin.validate_connection() is True
    assert connector_plugin.health_check() == ConnectorHealth.HEALTHY

    # Test action execution
    result = connector_plugin.execute("send_message", {"channel": "#general", "text": "Hello"})
    assert result == {"sent": True, "channel": "#general"}
