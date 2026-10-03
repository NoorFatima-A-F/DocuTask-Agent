"""
Tests for ActionExecutor and ConnectorRuntime.
"""

import pytest
from app.connectors.actions.executor import ActionExecutor
from app.connectors.core.exceptions import (
    ActionExecutionError,
    PolicyViolationError,
)
from app.connectors.core.models import (
    ActionDescriptor,
    ConnectorCategory,
)
from app.connectors.runtime.runtime import ConnectorRuntime
from app.connectors.sdk.builder import ConnectorBuilder


def test_action_executor_validation_and_permissions():
    executor = ActionExecutor()

    plugin = (
        ConnectorBuilder("conn-doc-parser", "Doc Parser")
        .with_action(
            name="parse_invoice",
            capability="document.parse",
            handler=lambda inp: {"invoice_id": inp["doc_id"], "total": 1500.0},
            input_schema={"required": ["doc_id"]},
        )
        .build()
    )

    action = ActionDescriptor(
        name="parse_invoice",
        connector_id="conn-doc-parser",
        capability="document.parse",
        input_schema={"required": ["doc_id"]},
        permissions=["doc.read"],
    )

    # Valid execution
    res = executor.execute_action(
        connector=plugin,
        action=action,
        inputs={"doc_id": "INV-2026-001"},
        granted_permissions=["doc.read"],
    )
    assert res.status == "SUCCESS"
    assert res.output["invoice_id"] == "INV-2026-001"
    assert res.latency_ms > 0

    # Missing required field error
    with pytest.raises(ActionExecutionError):
        executor.execute_action(
            connector=plugin,
            action=action,
            inputs={},
            granted_permissions=["doc.read"],
        )

    # Missing permission error
    with pytest.raises(PolicyViolationError):
        executor.execute_action(
            connector=plugin,
            action=action,
            inputs={"doc_id": "INV-2026-001"},
            granted_permissions=["unrelated.permission"],
        )


def test_connector_runtime_end_to_end_flow():
    runtime = ConnectorRuntime()

    # Register connector via SDK
    email_plugin = (
        ConnectorBuilder("conn-smtp-enterprise", "Enterprise SMTP")
        .with_category(ConnectorCategory.COMMUNICATION)
        .with_capability(name="email.send", category=ConnectorCategory.COMMUNICATION)
        .with_action(
            name="send",
            capability="email.send",
            handler=lambda inp: {"delivered": True, "to": inp["to"], "msg_id": "msg-999"},
            cost_usd=0.005,
        )
        .build()
    )

    runtime.connector_registry.register(email_plugin)
    runtime.capability_registry.bind_provider("email.send", "conn-smtp-enterprise")

    # Execute capability through runtime
    result = runtime.execute_capability(
        capability_name="email.send",
        inputs={"to": "ceo@acme.com", "subject": "Quarterly Report", "body": "Attached."},
        organization_id="org-enterprise",
        workspace_id="ws-executive",
    )

    assert result.status == "SUCCESS"
    assert result.connector_id == "conn-smtp-enterprise"
    assert result.output["delivered"] is True
    assert result.cost_usd == 0.005

    # Check metrics recorded in observability
    metrics = runtime.observability.get_summary("conn-smtp-enterprise")
    assert metrics is not None
    assert metrics.total_calls == 1
    assert metrics.successful_calls == 1
    assert metrics.total_cost_usd == 0.005

    # Fleet analytics report
    fleet_rep = runtime.analytics.generate_fleet_report()
    assert fleet_rep.total_calls == 1
    assert fleet_rep.overall_success_rate == 1.0
