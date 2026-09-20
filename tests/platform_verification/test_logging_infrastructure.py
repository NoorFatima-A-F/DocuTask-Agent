"""
Phase 3I.2: Enterprise Logging Infrastructure Verification - Unit and Integration Tests
"""
import os
import json
import pytest
import hashlib
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.logging_infrastructure.domain.models import (
    LogLevel,
    LoggingCertificationTier,
    LoggingServiceCoverage,
    ArchitectureReport,
    StructuredEventSample,
    StructuredLoggingReport,
    CorrelationTraceHop,
    CorrelationReport,
    AgentDecisionLogEntry,
    ErrorDiagnosticLogEntry,
    AgentLoggingReport,
    MaskedFieldRule,
    SecurityReport,
    RetentionTierSpec,
    PerformanceReport,
    FailureScenarioLogVerification,
    FailureTestReport,
    LoggingPillarScore,
    CertificationReport,
)
from app.platform_verification.logging_infrastructure.verifiers.logging_architecture_verifier import LoggingArchitectureVerifier
from app.platform_verification.logging_infrastructure.verifiers.structured_logging_verifier import StructuredLoggingVerifier
from app.platform_verification.logging_infrastructure.verifiers.correlation_verifier import CorrelationVerifier
from app.platform_verification.logging_infrastructure.verifiers.agent_execution_logging_verifier import AgentExecutionLoggingVerifier
from app.platform_verification.logging_infrastructure.verifiers.logging_security_verifier import LoggingSecurityVerifier
from app.platform_verification.logging_infrastructure.verifiers.logging_performance_verifier import LoggingPerformanceVerifier
from app.platform_verification.logging_infrastructure.verifiers.failure_simulation_logging_verifier import FailureSimulationLoggingVerifier
from app.platform_verification.logging_infrastructure.scoring.logging_quality_scorer import LoggingQualityScorer
from app.platform_verification.logging_infrastructure.exporter.logging_evidence_exporter import LoggingEvidenceExporter
from app.platform_verification.logging_infrastructure.runtime.logging_verification_runtime import LoggingVerificationRuntime
from app.platform_verification.logging_infrastructure.api.logging_verification_api import router as logging_api_router


# ─── 1. Domain Models Tests ───────────────────────────────────────────────────

def test_domain_models_instantiation():
    arch = ArchitectureReport(
        services_detected=8,
        services_covered=[
            LoggingServiceCoverage(service_name="api_gateway", log_format="JSON", centralized_delivery_latency_ms=25.0)
        ]
    )
    assert arch.services_detected == 8
    assert len(arch.services_covered) == 1
    assert arch.structured_logging is True

    sample = StructuredEventSample(
        level=LogLevel.INFO,
        service="document-worker",
        environment="production",
        event_name="invoice_extraction_completed",
        message="Extracted fields",
        request_id="REQ-123",
        trace_id="trace-456",
        task_id="task-789",
        duration_ms=1200.0,
        status="success"
    )
    assert sample.level == LogLevel.INFO
    assert sample.request_id == "REQ-123"

    struct_rep = StructuredLoggingReport(sample_event=sample)
    assert len(struct_rep.mandatory_fields) == 13
    assert struct_rep.schema_compliance_pct == 100.0

    corr_rep = CorrelationReport(
        trace_hops=[
            CorrelationTraceHop(hop_order=1, service="api-gateway", event="request_received")
        ]
    )
    assert corr_rep.end_to_end_correlated is True
    assert len(corr_rep.trace_hops) == 1

    cert_rep = CertificationReport(
        certification_tier=LoggingCertificationTier.ENTERPRISE_LOGGING_READY,
        overall_score_pct=98.5
    )
    assert cert_rep.certification_granted is True
    assert cert_rep.certification_tier == LoggingCertificationTier.ENTERPRISE_LOGGING_READY


# ─── 2. Architecture Verifier Tests ───────────────────────────────────────────

def test_logging_architecture_verifier():
    verifier = LoggingArchitectureVerifier()
    report = verifier.verify_logging_architecture()

    assert report.status == "PASS"
    assert report.services_detected == 8
    assert len(report.services_covered) == 8
    assert report.structured_logging is True
    assert report.centralized_collection is True

    service_names = [s.service_name for s in report.services_covered]
    assert "api_gateway" in service_names
    assert "gemini_llm_gateway" in service_names

    # Delivery latencies must all be under 5000ms
    for s in report.services_covered:
        assert s.centralized_delivery_latency_ms < 5000.0
        assert s.collector_attached is True


# ─── 3. Structured Logging Verifier Tests ─────────────────────────────────────

def test_structured_logging_verifier_compliance():
    verifier = StructuredLoggingVerifier()
    report = verifier.verify_structured_logging()

    assert report.structured_logging_passed is True
    assert report.schema_compliance_pct == 100.0
    assert report.plain_text_rejected is True
    assert report.level_classification_valid is True
    assert len(report.mandatory_fields) == 13
    assert "trace_id" in report.mandatory_fields
    assert "request_id" in report.mandatory_fields
    assert "duration" in report.mandatory_fields


# ─── 4. Correlation Verifier Tests ────────────────────────────────────────────

def test_correlation_verifier():
    verifier = CorrelationVerifier()
    report = verifier.verify_correlation()

    assert report.end_to_end_correlated is True
    assert report.correlation_capability_score == 100.0
    assert len(report.trace_hops) == 6

    # Verify order of hops
    services_in_order = [hop.service for hop in report.trace_hops]
    assert services_in_order == [
        "api-gateway",
        "redis-task-queue",
        "async-worker",
        "ocr-engine",
        "gemini-llm-gateway",
        "postgresql-db"
    ]

    for hop in report.trace_hops:
        assert hop.trace_id == "trace-abc123"
        assert hop.document_id == "doc-xyz789"
        assert hop.status == "SUCCESS"


# ─── 5. Agent Execution Logging Verifier Tests ────────────────────────────────

def test_agent_execution_logging_verifier():
    verifier = AgentExecutionLoggingVerifier()
    report = verifier.verify_agent_execution_logging()

    assert report.decision_reconstruction_possible is True
    assert report.ai_workflow_visibility_score == 100.0
    assert len(report.agent_lifecycle_stages_tracked) == 9

    # Verify decision entries
    decision_stages = [d.lifecycle_stage for d in report.sample_agent_decisions]
    assert "goal_created" in decision_stages
    assert "plan_generated" in decision_stages
    assert "llm_invoked" in decision_stages

    # Verify error diagnostics
    assert len(report.sample_error_diagnostics) >= 1
    for err in report.sample_error_diagnostics:
        assert err.error_code is not None
        assert err.recovery_action is not None
        assert err.stack_trace is not None


# ─── 6. Logging Security Verifier Tests ───────────────────────────────────────

def test_logging_security_verifier():
    verifier = LoggingSecurityVerifier()
    report = verifier.verify_security()

    assert report.secrets_prevented is True
    assert report.pii_masked is True
    assert report.medical_data_protected is True
    assert report.security_score_pct == 100.0
    assert len(report.masking_rules) >= 6

    categories = [r.data_category for r in report.masking_rules]
    assert "CNIC" in categories
    assert "Email" in categories
    assert "Phone" in categories
    assert "API Keys" in categories
    assert "Passwords" in categories
    assert "JWT Tokens" in categories


# ─── 7. Logging Performance Verifier Tests ────────────────────────────────────

def test_logging_performance_verifier():
    verifier = LoggingPerformanceVerifier()
    report = verifier.verify_performance()

    assert report.performance_compliant is True
    assert report.benchmark_documents_count == 10000
    assert report.overhead_pct < 5.0
    assert report.events_per_sec > 10000.0
    assert len(report.retention_tiers) == 3

    # Check retention policies: INFO 30d, ERROR 90d, CRITICAL/AUDIT/SECURITY 365d
    retention_map = {tier.log_level: tier.retention_days for tier in report.retention_tiers}
    assert retention_map.get("INFO") == 30
    assert retention_map.get("ERROR") == 90
    assert retention_map.get("SECURITY") == 365


# ─── 8. Failure Simulation Verifier Tests ─────────────────────────────────────

def test_failure_simulation_logging_verifier():
    verifier = FailureSimulationLoggingVerifier()
    report = verifier.verify_failure_simulation_logging()

    assert report.all_scenarios_verified is True
    assert len(report.scenarios) == 3

    scenario_ids = [s.scenario_id for s in report.scenarios]
    assert "CHAOS-LOG-001" in scenario_ids
    assert "CHAOS-LOG-002" in scenario_ids
    assert "CHAOS-LOG-003" in scenario_ids

    for sc in report.scenarios:
        assert sc.failure_correctly_logged is True
        assert sc.diagnostic_recovery_logged is True
        assert len(sc.actual_events_observed) == len(sc.expected_event_sequence)


# ─── 9. Scorer Tests ──────────────────────────────────────────────────────────

def test_logging_quality_scorer():
    arch = LoggingArchitectureVerifier().verify_logging_architecture()
    struct = StructuredLoggingVerifier().verify_structured_logging()
    corr = CorrelationVerifier().verify_correlation()
    agent = AgentExecutionLoggingVerifier().verify_agent_execution_logging()
    sec = LoggingSecurityVerifier().verify_security()
    perf = LoggingPerformanceVerifier().verify_performance()
    fail = FailureSimulationLoggingVerifier().verify_failure_simulation_logging()

    scorer = LoggingQualityScorer()
    certification = scorer.calculate_certification_score(
        arch_report=arch,
        struct_report=struct,
        corr_report=corr,
        agent_report=agent,
        sec_report=sec,
        perf_report=perf,
        failure_report=fail,
    )

    assert certification.overall_score_pct >= 95.0
    assert certification.certification_tier == LoggingCertificationTier.ENTERPRISE_LOGGING_READY
    assert certification.certification_granted is True
    assert len(certification.pillar_scores) == 6

    # Verify pillar weights sum to 100%
    total_weight = sum(p.weight_pct for p in certification.pillar_scores)
    assert abs(total_weight - 100.0) < 0.001


# ─── 10. Evidence Exporter Tests ──────────────────────────────────────────────

def test_logging_evidence_exporter(tmp_path):
    out_dir = str(tmp_path / "observability_verification" / "logging")
    exporter = LoggingEvidenceExporter()

    runtime = LoggingVerificationRuntime()
    result = runtime.run_full_verification(export_dir=out_dir)

    metadata = result["metadata"]
    assert metadata["services_detected"] == 8
    assert metadata["total_artifacts"] == 8  # 8 report files listed in manifest

    # Verify metadata.json and SHA-256 signatures
    metadata_path = os.path.join(out_dir, "metadata.json")
    assert os.path.exists(metadata_path)

    with open(metadata_path, "r", encoding="utf-8") as f:
        meta_loaded = json.load(f)

    assert "manifest_sha256" in meta_loaded
    for filename, recorded_hash in meta_loaded["manifest_sha256"].items():
        file_path = os.path.join(out_dir, filename)
        assert os.path.exists(file_path)
        with open(file_path, "r", encoding="utf-8") as rf:
            content_str = rf.read()
        computed_hash = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
        assert computed_hash == recorded_hash


# ─── 11. Verification Runtime & API Tests ─────────────────────────────────────

def test_logging_verification_runtime(tmp_path):
    out_dir = str(tmp_path / "obs_test")
    runtime = LoggingVerificationRuntime()
    result = runtime.run_full_verification(export_dir=out_dir)

    assert result["certification_report"].overall_score_pct >= 95.0
    assert result["certification_report"].certification_tier == LoggingCertificationTier.ENTERPRISE_LOGGING_READY
    assert result["certification_report"].certification_granted is True


def test_logging_verification_api_endpoints():
    app = FastAPI()
    app.include_router(logging_api_router)
    client = TestClient(app)

    # Health endpoint
    resp = client.get("/api/v1/logging-verification/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "HEALTHY"

    # Architecture endpoint
    resp = client.get("/api/v1/logging-verification/architecture")
    assert resp.status_code == 200
    assert resp.json()["services_detected"] == 8

    # Correlation endpoint
    resp = client.get("/api/v1/logging-verification/correlation")
    assert resp.status_code == 200
    assert resp.json()["end_to_end_correlated"] is True

    # Agent execution endpoint
    resp = client.get("/api/v1/logging-verification/agent-execution")
    assert resp.status_code == 200
    assert resp.json()["decision_reconstruction_possible"] is True

    # Security endpoint
    resp = client.get("/api/v1/logging-verification/security")
    assert resp.status_code == 200
    assert resp.json()["secrets_prevented"] is True

    # Performance endpoint
    resp = client.get("/api/v1/logging-verification/performance")
    assert resp.status_code == 200
    assert resp.json()["performance_compliant"] is True

    # Failures endpoint
    resp = client.get("/api/v1/logging-verification/failures")
    assert resp.status_code == 200
    assert resp.json()["all_scenarios_verified"] is True

    # Scorecard endpoint
    resp = client.get("/api/v1/logging-verification/scorecard")
    assert resp.status_code == 200
    assert resp.json()["overall_score_pct"] >= 95.0

    # Verification run POST endpoint
    resp = client.post("/api/v1/logging-verification/verify")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "COMPLETED"
    assert data["certification_tier"] == "Enterprise Logging Ready"
