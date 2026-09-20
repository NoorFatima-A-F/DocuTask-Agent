"""Tests for the Governance Python SDK Client and Exceptions."""

import pytest
from app.governance.platform.sdk.python.client import GovernanceClient
from app.governance.platform.sdk.python.exceptions import (
    AuthenticationError,
    PolicyDeniedError,
)


def test_sdk_initialization_and_evaluation():
    client = GovernanceClient(api_key="gov_test_key_123")

    decision = client.evaluate(
        action="agent.execute",
        resource="doc_parser",
        context={"risk_level": "low"},
    )
    assert decision.allowed is True
    assert decision.decision == "ALLOW"
    assert decision.decision_id.startswith("dec_")

    # List decisions
    decisions = client.list_decisions()
    assert len(decisions) >= 1


def test_sdk_policy_lifecycle():
    client = GovernanceClient(api_key="gov_test_key_123")

    # Create policy
    policy = client.create_policy(
        name="SDK Test Policy",
        description="Created via SDK test",
        policy_type="operational",
        severity="MEDIUM",
        enforcement_action="DENY",
    )
    assert policy.name == "SDK Test Policy"
    assert policy.status == "DRAFT"

    # Get policy
    fetched = client.get_policy(policy.policy_id)
    assert fetched.policy_id == policy.policy_id

    # Publish policy
    published = client.publish_policy(policy.policy_id, version="1.0.1")
    assert published.status == "ACTIVE"
    assert published.version == "1.0.1"


def test_sdk_report_generation_and_events():
    client = GovernanceClient(api_key="gov_test_key_123")

    report = client.generate_report(report_type="executive")
    assert report.governance_health_score > 90.0
    assert report.report_type == "executive"

    # Event subscription
    events_caught = []
    client.subscribe_events("SDK_EVENT", lambda e: events_caught.append(e))
    # Emit internal event to verify
    from app.governance.platform.api.internal.events import internal_event_bridge
    internal_event_bridge.publish("SDK_EVENT", "tenant_default", {"msg": "sdk test"})
    assert len(events_caught) == 1


def test_sdk_exception_handling():
    with pytest.raises(AuthenticationError):
        GovernanceClient(api_key="")

    client = GovernanceClient(api_key="gov_test_key_123")
    with pytest.raises(PolicyDeniedError):
        client.evaluate(
            action="model.invoke",
            resource="unauthorized_model",
            raise_on_deny=True,
        )
