"""Tests for Observability SDK, Decorators, and FastAPI REST API Endpoints."""

from app.observability.api.routes import (
    create_alert_rule,
    create_incident,
    get_dashboard_data,
    get_metrics_snapshot,
    get_observability_sdk,
    list_incidents,
    perform_rca,
    search_logs,
)
from app.observability.api.schemas import (
    AlertCreateRequest,
    IncidentCreateRequest,
    LogQueryRequest,
    RCARequest,
)
from app.observability.sdk.client import ObservabilitySDK
from app.observability.sdk.decorators import audit_log, metric_counter, profile, trace
from app.observability.tracing.spans import SpanKind


def test_observability_sdk_e2e():
    sdk = ObservabilitySDK(service_name="test-e2e-app")

    # Record heartbeat
    sdk.record_heartbeat("node-test-1", healthy=True)

    # Start trace
    with sdk.tracer.start_as_current_span("e2e_workflow") as span:
        span.set_attribute("tenant", "acme")
        sdk.logger.info("Executing workflow step")

    # Verify metrics
    metrics = sdk.metric_registry.dump_snapshot()
    assert "node_health_status" in str(metrics)

    # Verify logs
    logs = sdk.log_storage.search(service="test-e2e-app")
    assert len(logs) >= 1


def test_observability_decorators():
    @trace(operation="decorator_test_op", kind=SpanKind.INTERNAL)
    @metric_counter(name="decorator_calls_total")
    @profile(block_name="decorator_profile")
    @audit_log(action="test_action")
    def decorated_function(x: int) -> int:
        return x * 2

    res = decorated_function(21)
    assert res == 42


def test_fastapi_observability_routes():
    sdk = get_observability_sdk()

    # 1. Metrics snapshot
    metrics = get_metrics_snapshot(sdk=sdk)
    assert "counters" in metrics

    # 2. Write and search logs
    sdk.logger.info("Test log from FastAPI route test", extra_val=123)
    log_req = LogQueryRequest(query="FastAPI", limit=10)
    log_res = search_logs(log_req, sdk=sdk)
    assert len(log_res) >= 1

    # 3. Create and list alert rules
    rule_req = AlertCreateRequest(
        rule_id="rule-api-test",
        name="API Test Alert Rule",
        metric_name="node_cpu_usage_percent",
        operator=">",
        threshold_value=90.0,
    )
    rule_res = create_alert_rule(rule_req, sdk=sdk)
    assert rule_res["status"] == "created"

    # 4. Create and list incidents
    inc_req = IncidentCreateRequest(
        title="Test Incident from API",
        description="Testing incident creation via API",
        severity="SEV2_MAJOR",
        affected_services=["auth-svc"],
        commander="Alice SRE",
    )
    inc_res = create_incident(inc_req, sdk=sdk)
    assert inc_res.title == "Test Incident from API"
    assert inc_res.commander == "Alice SRE"

    inc_list = list_incidents(sdk=sdk)
    assert len(inc_list) >= 1

    # 5. Dashboard render
    db_res = get_dashboard_data("db-sre-golden-signals", sdk=sdk)
    assert "widgets" in db_res

    # 6. RCA analysis
    rca_req = RCARequest(
        service_name="payment-svc",
        metrics_snapshot={"node_cpu_usage_percent": 95.0, "runtime_queue_depth": 300.0},
    )
    rca_res = perform_rca(rca_req, sdk=sdk)
    assert rca_res.confidence_score >= 0.8
