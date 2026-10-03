"""Tests for Webhooks HMAC Signatures, Event Subscriptions, and Dispatcher."""

from app.governance.platform.webhooks.dispatcher import WebhookDispatcher
from app.governance.platform.webhooks.handlers import GovernanceEventHandler
from app.governance.platform.webhooks.subscriptions import (
    WebhookEventType,
    WebhookSubscriptionManager,
)


def test_webhook_registration_and_signature_generation():
    sub_mgr = WebhookSubscriptionManager()
    ep = sub_mgr.register(
        tenant_id="tenant_delta",
        url="https://client.example.com/governance-events",
        events=[WebhookEventType.POLICY_VIOLATION],
        secret="test_secret_key_123",
    )

    assert ep.webhook_id.startswith("wh_")
    assert ep.events == [WebhookEventType.POLICY_VIOLATION]

    # Verify signature generator
    sig = WebhookDispatcher.generate_signature(b'{"test": 1}', ep.secret_key)
    assert sig.startswith("sha256=")


def test_webhook_dispatcher_and_delivery_attempts():
    sub_mgr = WebhookSubscriptionManager()
    sub_mgr.register(
        tenant_id="tenant_delta",
        url="https://client.example.com/webhook",
        events=["*"],
        secret="test_secret",
    )

    calls = []

    def mock_poster(url: str, headers: dict, body: str) -> int:
        calls.append({"url": url, "headers": headers, "body": body})
        return 200

    dispatcher = WebhookDispatcher(subscription_mgr=sub_mgr, http_poster=mock_poster)
    deliveries = dispatcher.dispatch_event(
        tenant_id="tenant_delta",
        event_type=WebhookEventType.POLICY_VIOLATION,
        payload={"action": "model.invoke", "reason": "unauthorized"},
    )

    assert len(deliveries) == 1
    assert deliveries[0].success is True
    assert deliveries[0].status_code == 200
    assert len(calls) == 1
    assert "X-Governance-Signature" in calls[0]["headers"]


def test_event_handler_local_and_webhook_fanout():
    handler = GovernanceEventHandler()
    received_local = []

    handler.subscribe(WebhookEventType.APPROVAL_REQUIRED, lambda e: received_local.append(e))
    handler.publish_and_notify(
        tenant_id="tenant_delta",
        event_type=WebhookEventType.APPROVAL_REQUIRED,
        payload={"request_id": "req_1"},
    )

    assert len(received_local) == 1
    assert received_local[0]["payload"]["request_id"] == "req_1"
