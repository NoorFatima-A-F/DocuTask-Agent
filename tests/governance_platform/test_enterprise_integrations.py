"""Tests for Enterprise Integration Connectors and Adapters."""

from app.governance.platform.integrations.adapters import IntegrationAdapter
from app.governance.platform.integrations.connectors import (
    GRCPlatformConnector,
    SIEMConnector,
    SlackNotificationConnector,
)


def test_siem_connector_and_adapter():
    connector = SIEMConnector(endpoint_url="https://siem.corp.internal", api_token="siem_token")
    assert connector.connect() is True

    raw_event = {
        "event_type": "SECURITY_VIOLATION",
        "severity": "HIGH",
        "tenant_id": "tenant_enterprise",
        "payload": {"prompt_injection_detected": True},
        "timestamp": "2026-09-19T12:00:00Z",
    }

    adapted = IntegrationAdapter.to_siem_event(raw_event)
    assert adapted["source"] == "DocuTask-Governance-Platform"
    assert adapted["event_type"] == "SECURITY_VIOLATION"

    assert connector.send(adapted) is True
    assert len(connector.sent_events) == 1


def test_slack_connector_and_adapter():
    connector = SlackNotificationConnector(webhook_url="https://hooks.slack.com/services/test")
    assert connector.connect() is True

    payload = {
        "action": "model.invoke",
        "decision": "DENY",
        "risk_level": "CRITICAL",
        "reason": "Jailbreak signature detected",
    }
    slack_msg = IntegrationAdapter.to_slack_message("PolicyViolation", payload)
    assert ":shield:" in slack_msg["text"]
    assert slack_msg["attachments"][0]["color"] == "#D32F2F"

    assert connector.send(slack_msg) is True
    assert len(connector.sent_messages) == 1


def test_grc_connector():
    connector = GRCPlatformConnector(
        grc_type="OneTrust",
        base_url="https://onetrust.corp.internal",
        credentials={"client_id": "c1", "client_secret": "s1"},
    )
    assert connector.connect() is True
    assert connector.send({"evidence_id": "ev_123", "control": "EU_AI_ACT_ART_14"}) is True
    assert len(connector.synced_evidence) == 1
