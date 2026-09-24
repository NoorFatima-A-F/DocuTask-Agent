"""
Pytest Test Suite for Phase 13.15: Autonomous Real-World Execution Platform (ARWE-UTOCOP).
Covers all 15 backend subsystems, mathematical CPM algorithms, Saga rollbacks, cryptographic ledgers, and REST endpoints.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.runtime.execution.events import (
    ConnectorCategory,
    CredentialType,
    ExecutionEvent,
    ExecutionEventType,
    PolicyDecision,
    RiskLevel,
    ToolType,
    execution_event_bus,
)
from app.runtime.execution.tool_registry.tool_registry_engine import (
    ToolDefinition,
    ToolParameter,
    tool_registry_engine,
)
from app.runtime.execution.connectors.connector_engine import (
    ConnectorConfig,
    connector_engine,
)
from app.runtime.execution.browser.browser_engine import (
    browser_engine,
)
from app.runtime.execution.workflow.workflow_engine import (
    WorkflowDefinition,
    WorkflowStep,
    workflow_engine,
)
from app.runtime.execution.planner.execution_planner import execution_planner
from app.runtime.execution.credential.credential_engine import credential_engine
from app.runtime.execution.policy.policy_engine import policy_engine
from app.runtime.execution.simulation.execution_simulation import execution_simulation_engine
from app.runtime.execution.verification.verification_engine import verification_engine
from app.runtime.execution.rollback.rollback_engine import rollback_engine
from app.runtime.execution.monitoring.monitoring_engine import monitoring_engine
from app.runtime.execution.audit.audit_engine import audit_engine
from app.runtime.execution.runtime.execution_runtime import execution_runtime

client = TestClient(app)


# 1. Event Bus Tests
def test_execution_event_bus():
    received = []

    def handler(ev):
        received.append(ev)

    execution_event_bus.subscribe(ExecutionEventType.MISSION_STARTED.value, handler)
    execution_event_bus.publish(
        ExecutionEvent(
            event_type=ExecutionEventType.MISSION_STARTED,
            source="test",
            payload={"test_key": "val"},
        )
    )
    assert len(received) >= 1
    assert received[-1].payload.get("test_key") == "val"
    history = execution_event_bus.get_history(limit=5)
    assert len(history) > 0


# 2. Tool Registry Tests
def test_tool_registry_crud_and_validation():
    param = ToolParameter(
        name="target_ip",
        param_type="string",
        description="Target IP address",
        required=True,
    )
    valid, err = param.validate("192.168.1.1")
    assert valid is True

    valid_invalid, err_msg = param.validate(12345)
    assert valid_invalid is False
    assert "must be a string" in err_msg

    tool = ToolDefinition(
        tool_id="test_custom_ping_tool",
        name="Network Ping Diagnostic",
        version="1.0.0",
        description="Pings remote cyber-physical node",
        tool_type=ToolType.CYBER_PHYSICAL,
        category="infrastructure",
        parameters=[param],
    )
    registered = tool_registry_engine.register_tool(tool)
    assert registered.tool_id == "test_custom_ping_tool"

    found = tool_registry_engine.get_tool("test_custom_ping_tool")
    assert found is not None
    assert found.name == "Network Ping Diagnostic"

    tools_list = tool_registry_engine.list_tools(category="infrastructure")
    assert len(tools_list) >= 1


# 3. Connector Engine Tests
def test_connector_engine():
    conn = ConnectorConfig(
        connector_id="conn_test_mock_iot",
        name="Mock IoT Telemetry Gateway",
        category=ConnectorCategory.INFRASTRUCTURE,
        protocol="mqtt",
        endpoint_url="mqtt://broker.test.internal:1883",
    )
    created = connector_engine.create_connector(conn)
    assert created.connector_id == "conn_test_mock_iot"

    test_res = connector_engine.test_connection("conn_test_mock_iot")
    assert test_res["success"] is True
    assert test_res["status"] == "connected"
    assert test_res["latency_ms"] > 0


# 4. Browser Automation Tests
def test_browser_automation_engine():
    sess = browser_engine.create_session(viewport_width=1280, viewport_height=720)
    assert sess.session_id is not None
    assert sess.viewport_width == 1280

    nav_res = browser_engine.execute_action(sess.session_id, "navigate", value="https://dashboard.example.com")
    assert nav_res["success"] is True
    assert nav_res["current_url"] == "https://dashboard.example.com"

    act_res = browser_engine.execute_action(sess.session_id, "click", selector="button.submit")
    assert act_res["success"] is True

    shot_res = browser_engine.execute_action(sess.session_id, "screenshot")
    assert shot_res["action"]["screenshot_ref"] is not None

    closed = browser_engine.close_session(sess.session_id)
    assert closed is True


# 5. Workflow Engine & DAG Validation Tests
def test_workflow_engine_dag_and_interpolation():
    step1 = WorkflowStep(step_id="step_a", name="A", tool_id="postgres_execute_query", depends_on=[])
    step2 = WorkflowStep(step_id="step_b", name="B", tool_id="slack_send_channel_message", depends_on=["step_a"])
    step3 = WorkflowStep(step_id="step_c", name="C", tool_id="aws_s3_upload_artifact", depends_on=["step_b"])

    wf = WorkflowDefinition(
        workflow_id="wf_test_valid_dag",
        name="Valid Pipeline",
        description="Linear pipeline",
        steps=[step1, step2, step3],
    )
    valid, err = wf.validate_dag()
    assert valid is True
    assert err is None

    tiers = wf.get_execution_order()
    assert len(tiers) == 3
    assert tiers[0] == ["step_a"]
    assert tiers[1] == ["step_b"]
    assert tiers[2] == ["step_c"]

    # Test cycle detection
    step_cycle = WorkflowStep(step_id="step_cycle_a", name="Cycle A", tool_id="test", depends_on=["step_cycle_b"])
    step_cycle_2 = WorkflowStep(step_id="step_cycle_b", name="Cycle B", tool_id="test", depends_on=["step_cycle_a"])
    wf_invalid = WorkflowDefinition(
        workflow_id="wf_cycle",
        name="Cycle Pipeline",
        description="Invalid cycle",
        steps=[step_cycle, step_cycle_2],
    )
    valid_c, err_c = wf_invalid.validate_dag()
    assert valid_c is False
    assert "Cycle detected" in err_c

    # Test variable interpolation
    raw_inputs = {"url": "${steps.step_a.output.server_url}", "tag": "prod-${vars.env}"}
    ctx = {"steps": {"step_a": {"output": {"server_url": "https://api.internal"}}}, "vars": {"env": "us-east-1"}}
    interpolated = workflow_engine.interpolate_inputs(raw_inputs, ctx)
    assert interpolated["url"] == "https://api.internal"
    assert interpolated["tag"] == "prod-us-east-1"


# 6. Execution Planner & CPM Tests
def test_execution_planner_cpm():
    goal = "Deploy autonomous hotfix to production kubernetes cluster"
    wf, plan = execution_planner.plan_mission(goal)
    assert wf is not None
    assert plan is not None
    assert len(plan.nodes) >= 3
    assert len(plan.critical_path_steps) >= 1
    assert plan.total_estimated_duration_ms > 0
    assert plan.overall_risk in [RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]


# 7. Credential Engine Tests
def test_credential_engine():
    rec = credential_engine.add_credential(
        name="Test API Token",
        cred_type=CredentialType.API_KEY,
        target_system="api.test.corp",
        raw_secret="test_secret_key_1234567890",
        scopes=["read", "write"],
    )
    assert rec.credential_id is not None
    assert "••••••••••••" in rec.masked_value

    rotated = credential_engine.rotate_credential(rec.credential_id, "new_secret_key_0987654321")
    assert rotated is True

    valid_info = credential_engine.validate_credential(rec.credential_id)
    assert valid_info["valid"] is True


# 8. Policy & Governance Tests
def test_policy_engine_rules_and_approvals():
    # Test destructive query denial
    decision, reason = policy_engine.evaluate_step(
        tool_id="postgres_execute_query",
        inputs={"query": "DROP TABLE users CASCADE;"},
        tool_risk=RiskLevel.HIGH,
    )
    assert decision == PolicyDecision.DENY
    assert "Destructive SQL queries are strictly denied" in reason

    # Test high financial threshold
    decision_inv, reason_inv = policy_engine.evaluate_step(
        tool_id="stripe_create_customer_invoice",
        inputs={"amount_cents": 500000},
        tool_risk=RiskLevel.HIGH,
    )
    assert decision_inv == PolicyDecision.REQUIRE_APPROVAL

    # Test HITL approval lifecycle
    req = policy_engine.request_approval(
        mission_id="mission_test_approval",
        step_id="step_1",
        tool_id="stripe_create_customer_invoice",
        requester="billing_bot",
        risk_level=RiskLevel.HIGH,
        reason="Exceeds $1000 threshold",
    )
    assert req.status == "pending"

    resolved = policy_engine.resolve_approval(req.approval_id, approved=True, approver="cfo_agent")
    assert resolved.status == "approved"
    assert resolved.approver == "cfo_agent"


# 9. Simulation & Digital Twin Tests
def test_simulation_engine():
    wf, _ = execution_planner.plan_mission("Issue monthly customer invoice and store receipt")
    report = execution_simulation_engine.simulate_workflow(wf)
    assert report.simulation_passed is True
    assert report.total_steps == len(wf.steps)
    assert report.total_predicted_duration_ms > 0
    assert report.total_predicted_cost_usd >= 0.0


# 10. Verification & Cryptographic Proof Tests
def test_verification_engine():
    cert = verification_engine.verify_step_execution(
        mission_id="mission_ver_test",
        step_id="step_k8s",
        tool_id="k8s_scale_deployment",
        inputs={"deployment_name": "api-service", "replicas": 3, "namespace": "production"},
        output={"new_replicas": 3, "namespace": "production"},
    )
    assert cert.passed is True
    assert len(cert.checks) >= 1
    assert len(cert.state_signature_sha256) == 64  # SHA-256 hex length


# 11. Rollback & Saga Compensation Tests
def test_rollback_engine():
    executed_steps = [
        {
            "step_id": "step_pr",
            "tool_id": "github_create_pull_request",
            "status": "success",
            "is_compensable": True,
            "compensation_tool_id": "github_close_pull_request",
            "inputs": {"repo": "enterprise-corp/core-api", "pr_number": 1042},
        },
        {
            "step_id": "step_k8s",
            "tool_id": "k8s_scale_deployment",
            "status": "success",
            "is_compensable": True,
            "compensation_tool_id": "k8s_scale_deployment",
            "inputs": {"replicas": 1, "namespace": "production"},
        },
    ]

    session = rollback_engine.initiate_rollback(
        mission_id="mission_failed_test",
        trigger_reason="Canary health check regression",
        executed_steps=executed_steps,
    )
    assert session.status == "completed"
    assert session.completed_compensations == 2
    # Verify LIFO execution: k8s first, then github PR
    assert session.steps_to_compensate[0].original_step_id == "step_k8s"
    assert session.steps_to_compensate[1].original_step_id == "step_pr"


# 12. Monitoring Engine Tests
def test_monitoring_telemetry_and_anomalies():
    monitoring_engine.record_metric("conn_aws_us_east_1", "latency_ms", 450.0)
    alerts = monitoring_engine.list_alerts(resolved=False)
    assert len(alerts) >= 1
    assert alerts[0].metric_name == "latency_ms"
    assert alerts[0].observed_value == 450.0

    resolved = monitoring_engine.resolve_alert(alerts[0].alert_id)
    assert resolved is True

    snap = monitoring_engine.get_telemetry_snapshot()
    assert snap.total_executions_24h > 0


# 13. Audit Ledger & Cryptographic Chaining Tests
def test_audit_ledger_integrity():
    entry1 = audit_engine.record_entry(
        mission_id="mission_audit_1",
        action_type="mission_started",
        actor="system",
        risk_level=RiskLevel.LOW,
        payload_summary={"action": "start"},
    )
    entry2 = audit_engine.record_entry(
        mission_id="mission_audit_1",
        action_type="step_executed",
        actor="system",
        risk_level=RiskLevel.LOW,
        payload_summary={"action": "step_1"},
    )
    assert entry2.prev_hash == entry1.hash_signature

    valid, err = audit_engine.verify_ledger_integrity()
    assert valid is True
    assert err is None


# 14. Master Execution Runtime End-to-End Test
def test_master_execution_runtime_end_to_end():
    result = execution_runtime.execute_goal_end_to_end(
        goal="Scale kubernetes canary and notify ops",
        dry_run=False,
    )
    assert result["mission_id"] is not None
    assert result["status"] == "completed"
    assert result["steps_executed"] >= 3
    assert result["audit_trail_valid"] is True

    overview = execution_runtime.get_executive_overview()
    assert overview["system_status"] == "OPERATIONAL"
    assert overview["total_tools"] >= 5
    assert overview["total_connectors"] >= 5


# 15. REST API Client Tests
def test_rest_api_endpoints():
    # Overview
    r_ov = client.get("/api/v1/execution/overview")
    assert r_ov.status_code == 200
    assert r_ov.json()["system_status"] == "OPERATIONAL"

    # Tools
    r_tools = client.get("/api/v1/execution/tools")
    assert r_tools.status_code == 200
    assert len(r_tools.json()["tools"]) >= 5

    # Connectors
    r_conn = client.get("/api/v1/execution/connectors")
    assert r_conn.status_code == 200
    assert len(r_conn.json()["connectors"]) >= 5

    # Connector Test
    r_test = client.post("/api/v1/execution/connectors/conn_github_enterprise/test")
    assert r_test.status_code == 200
    assert r_test.json()["success"] is True

    # Browser Sessions
    r_bs = client.post("/api/v1/execution/browser/sessions")
    assert r_bs.status_code == 200
    sess_id = r_bs.json()["session"]["session_id"]

    r_act = client.post(f"/api/v1/execution/browser/sessions/{sess_id}/actions", json={"action_type": "navigate", "value": "https://enterprise.internal"})
    assert r_act.status_code == 200

    # Planner
    r_plan = client.post("/api/v1/execution/planner/plan", json={"mission_goal": "Issue enterprise invoice and store receipt"})
    assert r_plan.status_code == 200
    assert "plan" in r_plan.json()

    # Policy rules & approvals
    r_rules = client.get("/api/v1/execution/policies/rules")
    assert r_rules.status_code == 200

    # Execute Goal
    r_exec = client.post("/api/v1/execution/missions/execute-goal", json={"goal": "Scrape portal status and notify ops", "dry_run": False})
    assert r_exec.status_code == 200
    assert r_exec.json()["status"] == "completed"

    # Audit verify
    r_audit = client.get("/api/v1/execution/audit/verify")
    assert r_audit.status_code == 200
    assert r_audit.json()["ledger_valid"] is True
