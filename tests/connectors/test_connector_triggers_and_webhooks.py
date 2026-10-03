"""
Tests for TriggerEngine and WebhookEngine.
"""

import time
import pytest
from app.connectors.core.exceptions import WebhookVerificationError
from app.connectors.core.models import TriggerDescriptor, TriggerType
from app.connectors.triggers.engine import TriggerEngine, TriggerState
from app.connectors.webhooks.engine import WebhookConfig, WebhookEngine


def test_trigger_engine_lifecycle_and_subscription():
    events_received = []
    engine = TriggerEngine(event_sink=lambda e: events_received.append(e))

    engine.register_trigger(
        TriggerDescriptor(
            name="new_lead_created",
            connector_id="conn-hubspot",
            trigger_type=TriggerType.WEBHOOK,
        )
    )

    sub = engine.subscribe(
        trigger_name="new_lead_created",
        connector_id="conn-hubspot",
        organization_id="org-acme",
        workspace_id="ws-sales",
    )

    assert sub.state == TriggerState.LISTENING
    assert sub.connector_id == "conn-hubspot"

    # Ingest event
    raw_payload = {"lead_id": "lead-888", "email": "buyer@bigcorp.com"}
    norm_event = engine.process_incoming_event(
        subscription_id=sub.id,
        raw_event_payload=raw_payload,
        event_type="crm.lead.created",
    )

    assert norm_event.type == "crm.lead.created"
    assert norm_event.source == "connector.conn-hubspot"
    assert norm_event.organization == "org-acme"
    assert norm_event.payload["lead_id"] == "lead-888"
    assert len(events_received) == 1

    # Unsubscribe
    assert engine.unsubscribe(sub.id) is True
    assert sub.state == TriggerState.ARCHIVED


def test_webhook_engine_signature_and_replay_protection():
    webhook = WebhookEngine()
    secret = "super_secret_webhook_key_2026"

    webhook.register_endpoint(
        WebhookConfig(
            endpoint_id="ep-github-events",
            secret=secret,
            algorithm="sha256",
        )
    )

    payload_bytes = b'{"action": "opened", "pull_request": {"id": 42}}'

    # Compute valid signature
    valid_sig = webhook.sign_outgoing_payload(secret, payload_bytes, algorithm="sha256")

    # Verify signature passes
    assert webhook.verify_signature("ep-github-events", payload_bytes, valid_sig) is True

    # Bad signature fails
    with pytest.raises(WebhookVerificationError):
        webhook.verify_signature("ep-github-events", payload_bytes, "sha256=invalid_hex_digest")

    # Replay protection
    now = time.time()
    nonce = "nonce-abc-123"

    assert webhook.check_replay(nonce, now, window_seconds=300) is True

    # Replaying same nonce raises error
    with pytest.raises(WebhookVerificationError) as exc_info:
        webhook.check_replay(nonce, now, window_seconds=300)
    assert "Replay detected" in str(exc_info.value)

    # Stale timestamp outside window raises error
    with pytest.raises(WebhookVerificationError) as exc_info2:
        webhook.check_replay("new-nonce", now - 400, window_seconds=300)
    assert "freshness window" in str(exc_info2.value)


def test_outgoing_signed_webhook_dispatch():
    webhook = WebhookEngine()
    record = webhook.send_outgoing_webhook(
        url="https://partner.api/webhooks",
        payload={"event": "invoice.paid", "amount": 250.0},
        secret="outgoing_secret",
        event_type="invoice.paid",
    )

    assert record["status"] == "DELIVERED"
    assert "X-DocuTask-Signature" in record["headers"]
    assert record["headers"]["X-DocuTask-Event"] == "invoice.paid"
