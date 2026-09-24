"""Test Suite for Phase 3H.3.8 - AI Provider Health Verification Framework.

Tests all 15 parts, API routes, failure simulations, security redactions, and manifest generation.
"""

import os
import json
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.ai_provider_health.contract.ai_provider_health_contract import AIProviderHealthContractVerifier
from app.platform_verification.ai_provider_health.auth.ai_auth_verifier import AIAuthVerifier
from app.platform_verification.ai_provider_health.connectivity.ai_connectivity_verifier import AIConnectivityVerifier
from app.platform_verification.ai_provider_health.latency.ai_latency_verifier import AILatencyVerifier
from app.platform_verification.ai_provider_health.quota.ai_quota_verifier import AIQuotaVerifier
from app.platform_verification.ai_provider_health.integrity.ai_response_integrity_verifier import AIResponseIntegrityVerifier
from app.platform_verification.ai_provider_health.timeout.ai_timeout_verifier import AITimeoutVerifier
from app.platform_verification.ai_provider_health.taxonomy.ai_failure_classifier import AIFailureClassifier
from app.platform_verification.ai_provider_health.degraded.ai_degraded_mode_verifier import AIDegradedModeVerifier
from app.platform_verification.ai_provider_health.failover.ai_failover_verifier import AIFailoverVerifier
from app.platform_verification.ai_provider_health.monitoring.ai_monitoring_bridge import AIMonitoringBridge
from app.platform_verification.ai_provider_health.security.ai_security_auditor import AISecurityAuditor
from app.platform_verification.ai_provider_health.simulation.ai_failure_simulator import AIFailureSimulator
from app.platform_verification.ai_provider_health.runtime.ai_provider_health_runtime import AIProviderHealthRuntime
from app.platform_verification.ai_provider_health.api.ai_provider_health_api import router as ai_health_router
from app.platform_verification.ai_provider_health.domain.models import (
    AIProviderHealthState,
    AIFailureCategory,
    AIQualityCertificationTier,
)


def test_part_3h_3_8_1_provider_health_contract():
    verifier = AIProviderHealthContractVerifier()
    report = verifier.verify_provider_health()
    assert report.passed is True
    assert report.total_providers_monitored >= 2
    assert report.primary_provider == "gemini"
    assert report.primary_status == AIProviderHealthState.AVAILABLE
    for p in report.providers:
        assert p.latency_ms > 0
        assert p.authentication == "VALID"
        assert p.quota_status == "AVAILABLE"


def test_part_3h_3_8_2_auth_verifier():
    verifier = AIAuthVerifier()
    report = verifier.verify_authentication()
    assert report.passed is True
    assert report.all_authenticated is True
    assert report.total_providers_checked >= 2

    # Test invalid token handling
    fail_report = verifier.verify_authentication(mock_auth_data=[
        {"provider": "gemini", "key_token": "invalid_short_token", "permissions_sufficient": False, "expiration_detected": True}
    ])
    assert fail_report.all_authenticated is False
    assert fail_report.checks[0].authenticated is False
    assert fail_report.checks[0].status == "UNAVAILABLE_AUTH_FAILED"


def test_part_3h_3_8_3_connectivity_verifier():
    verifier = AIConnectivityVerifier()
    report = verifier.verify_connectivity()
    assert report.passed is True
    assert report.total_endpoints_tested >= 2
    assert report.avg_connection_success_rate_pct >= 99.0
    for ep in report.endpoints:
        assert ep.dns_resolved is True
        assert ep.tls_handshake_ms < 100.0


def test_part_3h_3_8_4_latency_verifier():
    verifier = AILatencyVerifier()
    report = verifier.verify_latency()
    assert report.passed is True
    assert report.total_models_measured >= 3
    assert report.all_within_thresholds is True
    for lat in report.latencies:
        assert lat.p95_latency_ms <= lat.threshold_p95_ms
        assert lat.degraded is False


def test_part_3h_3_8_5_quota_verifier():
    verifier = AIQuotaVerifier()
    report = verifier.verify_quota()
    assert report.passed is True
    assert report.total_providers_tracked >= 2
    assert report.quota_exhaustion_detected is False
    assert report.rate_limit_handling_verified is True
    for q in report.quotas:
        assert q.current_rpm_utilization_pct < 100.0
        assert q.current_tpm_utilization_pct < 100.0
        assert q.backoff_strategy_verified is True
        assert q.queue_preserved_under_burst is True


def test_part_3h_3_8_6_response_integrity_verifier():
    verifier = AIResponseIntegrityVerifier()
    report = verifier.verify_response_integrity()
    assert report.passed is True
    assert report.total_samples_evaluated >= 3
    assert report.schema_compliance_rate_pct >= 95.0
    assert report.avg_confidence_score >= 0.90
    assert report.invalid_response_rate_pct <= 5.0

    # Test payload validator helper
    valid_res = verifier.validate_raw_ai_payload('{"invoice_number": "INV-101", "total": 450.0}', ["invoice_number", "total"])
    assert valid_res["valid"] is True

    invalid_res = verifier.validate_raw_ai_payload('{"invoice_number": null}', ["invoice_number", "total"])
    assert invalid_res["valid"] is False


def test_part_3h_3_8_7_timeout_verifier():
    verifier = AITimeoutVerifier()
    report = verifier.verify_timeouts()
    assert report.passed is True
    assert report.total_timeout_tests >= 2
    assert report.all_timeouts_handled_safely is True
    for t in report.tests:
        assert t.timeout_triggered is True
        assert t.cancellation_clean is True
        assert t.task_state_preserved is True


def test_part_3h_3_8_8_failure_classifier():
    classifier = AIFailureClassifier()
    report = classifier.classify_failures()
    assert report.passed is True
    assert report.total_failure_patterns_classified >= 4
    assert report.all_categories_covered is True

    # Test individual error classification
    cat503 = classifier.classify_error(503, "Service Unavailable")
    assert cat503.category == AIFailureCategory.PROVIDER_UNAVAILABLE
    assert cat503.operator_alert_required is True

    cat401 = classifier.classify_error(401, "Unauthorized")
    assert cat401.category == AIFailureCategory.AUTHENTICATION_FAILURE

    cat429 = classifier.classify_error(429, "Too Many Requests")
    assert cat429.category == AIFailureCategory.QUOTA_EXHAUSTION


def test_part_3h_3_8_9_degraded_mode_verifier():
    verifier = AIDegradedModeVerifier()
    report = verifier.verify_degraded_mode()
    assert report.passed is True
    assert report.graceful_degradation_active is True
    assert report.task_persistence_verified is True
    assert report.fallback_routing_ready is True
    assert report.user_alerting_verified is True


def test_part_3h_3_8_10_failover_verifier():
    verifier = AIFailoverVerifier()
    report = verifier.verify_failover()
    assert report.passed is True
    assert report.total_failover_scenarios >= 2
    assert report.avg_failover_latency_ms <= 300.0
    for fo in report.failovers:
        assert fo.success_rate_pct >= 99.0
        assert fo.data_consistency_verified is True


def test_part_3h_3_8_11_monitoring_bridge():
    bridge = AIMonitoringBridge()
    report = bridge.verify_monitoring_integration()
    assert report.passed is True
    assert report.prometheus_metrics_exposed >= 5
    assert report.alert_rules_configured >= 2
    assert report.opentelemetry_traces_active is True


def test_part_3h_3_8_12_security_auditor():
    auditor = AISecurityAuditor()
    report = auditor.audit_security()
    assert report.passed is True
    assert report.sensitive_data_exposed is False
    assert report.total_checks >= 3

    # Test detection of leaked tokens
    leaks = auditor.scan_for_leaks("Failed request: auth=bearer " + "x" * 25)
    assert len(leaks) > 0


def test_part_3h_3_8_13_failure_simulator():
    simulator = AIFailureSimulator()
    report = simulator.run_simulations()
    assert report.passed is True
    assert report.total_simulations >= 4
    assert report.all_recovered is True
    for sim in report.simulations:
        assert sim.recovered_successfully is True
        assert sim.passed is True


def test_part_3h_3_8_14_evidence_exporter_and_8_manifests(tmp_path):
    output_dir = str(tmp_path / "ai_verification_out")
    runtime = AIProviderHealthRuntime(export_dir=output_dir)
    runtime.run_full_verification()

    assert os.path.exists(output_dir)
    expected_files = [
        "provider_health_report.json",
        "authentication_report.json",
        "latency_report.json",
        "quota_report.json",
        "response_quality_report.json",
        "failure_simulation_report.json",
        "failover_report.json",
        "metadata.json",
    ]
    for fname in expected_files:
        fpath = os.path.join(output_dir, fname)
        assert os.path.exists(fpath), f"Missing expected file {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data is not None


def test_part_3h_3_8_15_health_scorer_and_certification():
    runtime = AIProviderHealthRuntime()
    res = runtime.run_full_verification()
    scorecard = res["scorecard"]

    assert scorecard.passed is True
    assert scorecard.overall_score >= 95.0
    assert scorecard.certification_tier == AIQualityCertificationTier.AI_RELIABILITY_CERTIFIED
    assert scorecard.certification_verdict == "CERTIFIED"


def test_ai_provider_health_fastapi_endpoints():
    app = FastAPI()
    app.include_router(ai_health_router)
    client = TestClient(app)

    endpoints = [
        "/health/ai/status",
        "/health/ai/auth",
        "/health/ai/connectivity",
        "/health/ai/latency",
        "/health/ai/quota",
        "/health/ai/integrity",
        "/health/ai/failover",
        "/health/ai/simulations",
        "/health/ai/scorecard",
    ]

    for ep in endpoints:
        resp = client.get(ep)
        assert resp.status_code == 200, f"Endpoint {ep} failed with status {resp.status_code}"
        assert resp.json() is not None

    post_resp = client.post("/health/ai/verify")
    assert post_resp.status_code == 200
    data = post_resp.json()
    assert data["passed"] is True
    assert data["scorecard"]["overall_score"] >= 95.0
