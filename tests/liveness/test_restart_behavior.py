"""
Tests for Orchestration Restart Behavior, Quality Scoring, and API Integration (Parts 10, 12, 13, 15, 16).
"""
import pytest
import os
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.liveness.recovery.automated_recovery_verifier import (
    AutomatedRecoveryVerifier,
)
from app.platform_verification.liveness.security.liveness_security_verifier import (
    LivenessSecurityVerifier,
)
from app.platform_verification.liveness.scheduler.scheduler_liveness_monitor import (
    SchedulerLivenessMonitor,
)
from app.platform_verification.liveness.runtime.liveness_runtime import (
    LivenessVerificationRuntime,
)
from app.platform_verification.liveness.domain.models import (
    LivenessTier,
)
from app.platform_verification.liveness.api.liveness_verification_api import (
    router as liveness_api_router,
)


@pytest.fixture
def test_app():
    app = FastAPI(title="Liveness Test App")
    app.include_router(liveness_api_router)
    return app


@pytest.fixture
def test_client(test_app):
    return TestClient(test_app)


def test_recovery_verifier():
    verifier = AutomatedRecoveryVerifier()
    report = verifier.verify_recovery()

    assert report.mttr_seconds < 30.0
    assert report.orchestrator_restart_verified is True
    assert len(report.cloud_runtimes_compatible) >= 4
    assert report.passed is True


def test_security_verifier():
    verifier = LivenessSecurityVerifier()
    report = verifier.verify_security()

    assert report.public_endpoint_leak_free is True
    assert report.credentials_leaked_count == 0
    assert report.passed is True


def test_scheduler_monitor():
    monitor = SchedulerLivenessMonitor()
    report = monitor.check_scheduler_liveness()

    assert report.scheduler_running is True
    assert report.scheduler_healthy is True
    assert report.missed_jobs_count == 0
    assert report.passed is True


def test_full_liveness_runtime_and_scoring(tmp_path):
    output_dir = str(tmp_path / "health_verification")
    runtime = LivenessVerificationRuntime(output_dir=output_dir)
    result = runtime.run_full_verification(export=True)

    assert result["success"] is True
    scorecard = result["scorecard"]
    assert scorecard.overall_liveness_score >= 95.0
    assert scorecard.certification_tier == LivenessTier.ENTERPRISE_READY
    assert scorecard.certification_verdict == "CERTIFIED"
    assert scorecard.auto_recovery_validated is True
    assert scorecard.passed is True

    exported = result["exported_files"]
    assert len(exported) == 10
    for fname in [
        "liveness_contract_report.json",
        "process_health_report.json",
        "event_loop_report.json",
        "deadlock_report.json",
        "worker_liveness_report.json",
        "resource_health_report.json",
        "failure_simulation_report.json",
        "recovery_report.json",
        "certification.json",
        "metadata.json",
    ]:
        assert fname in exported
        assert os.path.exists(exported[fname])


def test_liveness_fastapi_endpoints(test_client):
    res_live = test_client.get("/api/v1/liveness/live")
    assert res_live.status_code == 200
    assert res_live.json()["status"] == "alive"
    assert res_live.json()["service"] == "api"

    res_proc = test_client.get("/api/v1/liveness/process")
    assert res_proc.status_code == 200
    assert res_proc.json()["all_processes_alive"] is True

    res_loop = test_client.get("/api/v1/liveness/event-loop")
    assert res_loop.status_code == 200
    assert res_loop.json()["loop_healthy"] is True

    res_dl = test_client.get("/api/v1/liveness/deadlocks")
    assert res_dl.status_code == 200
    assert res_dl.json()["deadlock_detected"] is False

    res_sched = test_client.get("/api/v1/liveness/scheduler")
    assert res_sched.status_code == 200
    assert res_sched.json()["scheduler_healthy"] is True

    res_rec = test_client.get("/api/v1/liveness/recovery")
    assert res_rec.status_code == 200
    assert res_rec.json()["mttr_seconds"] < 30.0

    res_sec = test_client.get("/api/v1/liveness/security")
    assert res_sec.status_code == 200
    assert res_sec.json()["credentials_leaked_count"] == 0

    res_verify = test_client.get("/api/v1/liveness/verify")
    assert res_verify.status_code == 200
    data = res_verify.json()
    assert data["success"] is True
    assert data["scorecard"]["overall_liveness_score"] >= 95.0

    res_metrics = test_client.get("/api/v1/liveness/metrics")
    assert res_metrics.status_code == 200
    assert "service_liveness_status" in res_metrics.text
