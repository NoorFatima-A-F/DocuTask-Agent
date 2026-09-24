"""
Tests for ObservabilitySDK and FastAPI Observability REST API Endpoints.
"""


from app.infrastructure.observability.alerts.models import AlertRule, AlertSeverity
from app.infrastructure.observability.api.observability_routes import (
    LogEmitRequest,
    MetricRecordRequest,
    create_alert_rule,
    emit_log,
    get_dependencies,
    get_metrics,
    list_alerts,
    list_slos,
    record_metric,
    run_rca,
    search_logs,
)
from app.infrastructure.observability.logs.models import LogLevel
from app.infrastructure.observability.metrics.types import MetricType
from app.infrastructure.observability.sdk.observability import ObservabilitySDK
from app.infrastructure.observability.slo.objectives import SLIType, SLOObjective


def test_observability_sdk_methods():
    sdk = ObservabilitySDK()

    # 1. Metrics
    sdk.record_metric("test_gauge", 42.0)
    sdk.increment_counter("test_counter", 5.0)
    metrics = sdk.get_metrics(prefix="test_")
    assert len(metrics) >= 2

    # 2. Logs
    sdk.log(LogLevel.INFO, "SDK log event", tenant_id="tenant-sdk")
    logs = sdk.search_logs(tenant_id="tenant-sdk")
    assert len(logs) >= 1

    # 3. Traces
    with sdk.trace_span("sdk_operation", attributes={"tag": "val"}) as s:
        s.add_event("step_1")

    trace_id = s.trace_id
    report = sdk.analyze_trace(trace_id)
    assert report is not None
    assert report.trace_id == trace_id

    # 4. Alerts
    rule = AlertRule(
        rule_id="sdk-rule-1",
        name="SDK Test Alert",
        metric_name="sdk_metric",
        comparator=">",
        threshold_value=50.0,
        severity=AlertSeverity.MAJOR,
    )
    sdk.alert_evaluator.register_rule(rule)
    alt = sdk.evaluate_alert("sdk-rule-1", value=75.0)
    assert alt is not None
    assert alt.status.value == "FIRING"

    # 5. SLO
    slo = SLOObjective(
        slo_id="sdk-slo-1",
        name="SDK SLO",
        service_name="sdk-service",
        sli_type=SLIType.AVAILABILITY,
        target_percent=99.0,
    )
    sdk.error_budget_tracker.register_slo(slo)
    budget = sdk.record_slo_events("sdk-slo-1", good_count=99, bad_count=1)
    assert budget.current_compliance_percent == 99.0

    # 6. RCA
    rca = sdk.run_root_cause_analysis(trace_id=trace_id)
    assert rca is not None
    assert rca.report_id == "rca-latest"


def test_fastapi_observability_routes_direct():
    # 1. Record and Get Metric via API
    rec_req = MetricRecordRequest(name="api_metric_test", value=99.0, metric_type=MetricType.GAUGE)
    rec_res = record_metric(rec_req)
    assert rec_res["status"] == "RECORDED"

    metrics_res = get_metrics(prefix="api_metric_test")
    assert len(metrics_res) >= 1

    # 2. Emit and Search Logs via API
    log_req = LogEmitRequest(level=LogLevel.INFO, message="API emitted log", attributes={"user": "admin"})
    log_res = emit_log(log_req)
    assert log_res["level"] == "INFO"

    search_res = search_logs(keyword="API emitted log")
    assert len(search_res) >= 1

    # 3. Create Alert Rule and List Alerts via API
    rule_req = AlertRule(
        rule_id="api-alert-rule",
        name="API Memory Rule",
        metric_name="api_mem",
        threshold_value=90.0,
        severity=AlertSeverity.CRITICAL,
    )
    create_alert_rule(rule_req)
    alerts_res = list_alerts()
    assert isinstance(alerts_res, list)

    # 4. List SLOs via API
    slos_res = list_slos()
    assert isinstance(slos_res, list)

    # 5. Dependencies via API
    deps_res = get_dependencies()
    assert isinstance(deps_res, list)

    # 6. RCA via API
    rca_res = run_rca()
    assert "report_id" in rca_res
    assert "confidence_score" in rca_res
