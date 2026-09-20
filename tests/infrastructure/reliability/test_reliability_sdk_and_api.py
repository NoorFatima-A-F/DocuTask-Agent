"""
Tests for ReliabilitySDK and FastAPI Reliability REST API Endpoints.
"""

import pytest

from app.infrastructure.api.reliability_routes import (
    FailoverExecuteRequest,
    FailoverPlanRequest,
    IncidentCreateRequest,
    IncidentTransitionRequest,
    ProbeRegisterRequest,
    create_incident,
    execute_failover,
    execute_probe,
    execute_recovery,
    get_component_health,
    get_failover_status,
    get_replication_lag,
    get_system_health,
    list_incidents,
    plan_failover,
    register_probe,
    transition_incident,
)
from app.infrastructure.failover.planner import FailoverScope, FailoverType
from app.infrastructure.health.probes import ProbeType
from app.infrastructure.incidents.models import IncidentStatus
from app.infrastructure.recovery.checkpoints import CheckpointType
from app.infrastructure.recovery.workflows import build_database_corruption_workflow
from app.infrastructure.reliability.models import SeverityLevel
from app.infrastructure.sdk.reliability import ReliabilitySDK


def test_reliability_sdk_methods():
    sdk = ReliabilitySDK()

    # 1. Probe & Health
    probe = sdk.register_probe("sdk-probe-1", "sdk-service", ProbeType.LIVENESS, handler=lambda: True)
    assert probe.probe_id == "sdk-probe-1"

    res = sdk.execute_probe("sdk-probe-1")
    assert res.status.value == "HEALTHY"

    health = sdk.get_component_health("sdk-service")
    assert health.score == 100.0

    sys_health = sdk.get_system_health()
    assert sys_health.healthy_count >= 1

    # 2. Checkpoint & Recovery
    cp = sdk.create_checkpoint("sdk-cp-1", CheckpointType.STATE_SNAPSHOT, "sdk-service", "us-east-1", {"k": "v"})
    assert cp.status.value == "VERIFIED"

    wf = build_database_corruption_workflow("sdk-wf-1", "sdk-db", "sdk-cp-1")
    report = sdk.execute_recovery_workflow(wf)
    assert report.success

    # 3. Failover
    plan = sdk.plan_failover("sdk-plan-1", "us-east-1", "us-west-2")
    assert plan.status.value == "PROPOSED"
    exec_res = sdk.execute_failover("sdk-plan-1")
    assert exec_res.success

    # 4. Replication Lag
    metric = sdk.record_replication_lag("sdk-stream-1", lag_seconds=2.5)
    assert metric.lag_seconds == 2.5

    # 5. Incident
    inc = sdk.create_incident("sdk-inc-1", "SDK Test Incident", SeverityLevel.WARNING)
    assert inc.incident_id == "sdk-inc-1"
    assert len(sdk.list_active_incidents()) == 1


def test_fastapi_reliability_routes_direct():
    # 1. Register Probe via API
    reg_req = ProbeRegisterRequest(
        probe_id="api-probe-01",
        component_id="api-ocr",
        probe_type=ProbeType.LIVENESS,
        interval_seconds=15.0,
        timeout_seconds=2.0,
    )
    reg_resp = register_probe(reg_req)
    assert reg_resp["status"] == "REGISTERED"
    assert reg_resp["probe"]["probe_id"] == "api-probe-01"

    # 2. Execute Probe via API
    exec_resp = execute_probe("api-probe-01")
    assert exec_resp["status"] == "HEALTHY"

    # 3. Get Health via API
    health_resp = get_system_health()
    assert "total_components" in health_resp

    comp_health = get_component_health("api-ocr")
    assert comp_health["component_id"] == "api-ocr"

    # 4. Plan and Execute Failover via API
    plan_req = FailoverPlanRequest(
        plan_id="api-plan-01",
        source_region="us-east-1",
        target_region="us-west-2",
        failover_type=FailoverType.AUTOMATIC,
        scope=FailoverScope.REGION,
    )
    plan_resp = plan_failover(plan_req)
    assert plan_resp["plan_id"] == "api-plan-01"

    exec_fo_req = FailoverExecuteRequest(plan_id="api-plan-01")
    exec_fo_resp = execute_failover(exec_fo_req)
    assert exec_fo_resp["success"] is True

    fo_status = get_failover_status("api-plan-01")
    assert fo_status["plan"]["status"] == "COMPLETED"

    # 5. Recovery via API
    wf = build_database_corruption_workflow("api-wf-01", "api-db", "cp-api-01")
    rec_report = execute_recovery(wf)
    assert rec_report["success"] is True

    # 6. Incident Lifecycle via API
    inc_req = IncidentCreateRequest(
        incident_id="api-inc-01",
        title="API Gateway Degradation",
        severity=SeverityLevel.CRITICAL,
        impacted_components=["api-gateway"],
    )
    inc_resp = create_incident(inc_req)
    assert inc_resp["incident_id"] == "api-inc-01"

    trans_req = IncidentTransitionRequest(
        target_status=IncidentStatus.INVESTIGATING,
        actor="sre-bot",
        message="Investigating logs",
    )
    trans_resp = transition_incident("api-inc-01", trans_req)
    assert trans_resp["status_change"] == IncidentStatus.INVESTIGATING.value

    all_incs = list_incidents()
    assert len(all_incs) >= 1

    # 7. Replication Lag via API
    lags = get_replication_lag()
    assert isinstance(lags, list)
