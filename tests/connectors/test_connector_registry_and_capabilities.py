"""
Tests for ConnectorRegistry and CapabilityRegistry.
"""

import pytest
from app.connectors.core.exceptions import CapabilityNotFoundError, ConnectorNotFoundError
from app.connectors.core.models import (
    CapabilityDescriptor,
    Connector,
    ConnectorCategory,
    ConnectorHealth,
    ConnectorStatus,
)
from app.connectors.registry.capability_registry import CapabilityRegistry
from app.connectors.registry.connector_registry import ConnectorRegistry


def test_connector_registry_crud_and_search():
    registry = ConnectorRegistry()

    c1 = Connector(
        id="conn-sendgrid",
        name="SendGrid Email",
        vendor="Twilio",
        version="1.0.0",
        category=ConnectorCategory.COMMUNICATION,
        capabilities=["email.send"],
    )
    c2 = Connector(
        id="conn-s3",
        name="AWS S3",
        vendor="Amazon",
        version="2.1.0",
        category=ConnectorCategory.STORAGE,
        capabilities=["storage.upload", "storage.download"],
    )

    registry.register(c1)
    registry.register(c2)

    # Retrieval
    assert registry.get("conn-sendgrid").name == "SendGrid Email"
    assert registry.get("conn-s3").vendor == "Amazon"

    with pytest.raises(ConnectorNotFoundError):
        registry.get("non-existent")

    # Search
    search_email = registry.search("email")
    assert len(search_email) == 1
    assert search_email[0].id == "conn-sendgrid"

    search_aws = registry.search("Amazon")
    assert len(search_aws) == 1
    assert search_aws[0].id == "conn-s3"

    # Health update
    registry.update_health("conn-sendgrid", ConnectorHealth.DEGRADED)
    assert registry.get("conn-sendgrid").health == ConnectorHealth.DEGRADED


def test_capability_discovery_and_ranking():
    conn_reg = ConnectorRegistry()
    cap_reg = CapabilityRegistry(conn_reg)

    gmail = Connector(
        id="conn-gmail",
        name="Gmail",
        vendor="Google",
        category=ConnectorCategory.COMMUNICATION,
        capabilities=["email.send"],
        status=ConnectorStatus.READY,
        health=ConnectorHealth.HEALTHY,
    )
    sendgrid = Connector(
        id="conn-sendgrid",
        name="SendGrid",
        vendor="Twilio",
        category=ConnectorCategory.COMMUNICATION,
        capabilities=["email.send"],
        status=ConnectorStatus.READY,
        health=ConnectorHealth.HEALTHY,
    )

    conn_reg.register(gmail)
    conn_reg.register(sendgrid)

    cap_reg.bind_provider("email.send", "conn-gmail")
    cap_reg.bind_provider("email.send", "conn-sendgrid")

    # Discover providers
    providers = cap_reg.find_providers("email.send")
    assert len(providers) == 2

    # Preferred vendor ordering
    preferred_providers = cap_reg.find_providers("email.send", preferred_vendor="Twilio")
    assert preferred_providers[0].vendor == "Twilio"

    # Capability not found error
    with pytest.raises(CapabilityNotFoundError):
        cap_reg.find_providers("quantum.teleport")


def test_standard_capabilities_preseeded():
    cap_reg = CapabilityRegistry()
    caps = cap_reg.list_capabilities()
    names = [c.name for c in caps]

    assert "email.send" in names
    assert "message.send" in names
    assert "storage.upload" in names
    assert "crm.contact.create" in names
