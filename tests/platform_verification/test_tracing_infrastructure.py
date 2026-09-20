"""
Phase 3I.4: Enterprise Distributed Tracing Infrastructure Verification - Unit and Integration Tests
"""
import os
import json
import pytest
import hashlib
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.tracing_infrastructure.domain.models import (
    SpanKind,
    TracingCertificationTier,
    TracingServiceInstrumentation,
    TracingArchitectureReport,
    TraceContextPropagationHop,
    ContextPropagationReport,
    SpanDetail,
    WorkflowTraceReport,
    AgentLifecycleSpan,
    AgentTraceReport,
    QueueWorkerSpanSummary,
    DatabaseSpanSummary,
    ExternalDependencySpan,
    DependencyTraceReport,
    FailedSpanDiagnostic,
    ErrorTraceReport,
    TraceCorrelationReport,
    SamplingRuleSpec,
    TraceSamplingReport,
    SpanSecurityAuditSpec,
    TraceSecurityReport,
    TracePerformanceReport,
    ChaosTraceScenarioSpec,
    ChaosTraceReport,
    TracingPillarScore,
    TracingCertificationReport,
)
from app.platform_verification.tracing_infrastructure.verifiers.tracing_architecture_verifier import TracingArchitectureVerifier
from app.platform_verification.tracing_infrastructure.verifiers.context_propagation_verifier import ContextPropagationVerifier
from app.platform_verification.tracing_infrastructure.verifiers.api_workflow_trace_verifier import WorkflowTraceVerifier
from app.platform_verification.tracing_infrastructure.verifiers.ai_agent_trace_verifier import AgentTraceVerifier
from app.platform_verification.tracing_infrastructure.verifiers.external_dependency_trace_verifier import ExternalDependencyTraceVerifier
from app.platform_verification.tracing_infrastructure.verifiers.error_diagnostic_trace_verifier import ErrorDiagnosticTraceVerifier
from app.platform_verification.tracing_infrastructure.verifiers.trace_log_metric_correlation_verifier import TraceCorrelationVerifier
from app.platform_verification.tracing_infrastructure.verifiers.sampling_strategy_verifier import SamplingStrategyVerifier
from app.platform_verification.tracing_infrastructure.verifiers.trace_security_verifier import TraceSecurityVerifier
from app.platform_verification.tracing_infrastructure.verifiers.trace_performance_verifier import TracePerformanceVerifier
from app.platform_verification.tracing_infrastructure.verifiers.failure_simulation_trace_verifier import FailureSimulationTraceVerifier
from app.platform_verification.tracing_infrastructure.scoring.tracing_quality_scorer import TracingQualityScorer
from app.platform_verification.tracing_infrastructure.exporter.tracing_evidence_exporter import TracingEvidenceExporter
from app.platform_verification.tracing_infrastructure.runtime.tracing_verification_runtime import TracingVerificationRuntime
from app.platform_verification.tracing_infrastructure.api.tracing_verification_api import router as tracing_api_router


# ─── 1. Domain Models Tests ───────────────────────────────────────────────────

def test_domain_models_instantiation():
    arch = TracingArchitectureReport(
        services_instrumented=8,
        services=[
            TracingServiceInstrumentation(service_name="api_gateway", sdk="OTel Python", backend="Tempo")
        ]
    )
    assert arch.services_instrumented == 8
    assert arch.collector == "OpenTelemetry"
    assert arch.backend == "Tempo"

    span = SpanDetail(
        span_id="span_123",
        parent_span_id=None,
        name="test_span",
        service="api_gateway",
        kind=SpanKind.SERVER,
        duration_ms=45.0
    )
    assert span.kind == SpanKind.SERVER

    cert_rep = TracingCertificationReport(
        certification_tier=TracingCertificationTier.ENTERPRISE_TRACING_READY,
        overall_score_pct=98.5
    )
    assert cert_rep.certification_granted is True
    assert cert_rep.certification_tier == TracingCertificationTier.ENTERPRISE_TRACING_READY


# ─── 2. Architecture Verifier Tests ───────────────────────────────────────────

def test_tracing_architecture_verifier():
    verifier = TracingArchitectureVerifier()
    report = verifier.verify_tracing_architecture()

    assert report.status == "PASS"
    assert report.services_instrumented == 8
    assert len(report.services) == 8
    assert report.collector == "OpenTelemetry"
    assert report.backend == "Tempo"

    service_names = [s.service_name for s in report.services]
    assert "api_gateway" in service_names
    assert "gemini_llm_gateway" in service_names
    assert "async_document_worker" in service_names


# ─── 3. Context Propagation Verifier Tests ────────────────────────────────────

def test_context_propagation_verifier():
    verifier = ContextPropagationVerifier()
    report = verifier.verify_context_propagation()

    assert report.context_propagation_passed is True
    assert report.context_integrity_pct == 100.0
    assert report.async_queue_propagation_valid is True
    assert len(report.propagation_hops) >= 7

    for hop in report.propagation_hops:
        assert hop.trace_id == report.sample_trace_id
        assert hop.propagation_valid is True


# ─── 4. Workflow Trace Verifier Tests ─────────────────────────────────────────

def test_workflow_trace_verifier():
    verifier = WorkflowTraceVerifier()
    report = verifier.verify_workflow_trace()

    assert report.workflow_trace_passed is True
    assert report.total_trace_duration_ms > 0
    assert report.slowest_component == "gemini_structured_extraction"
    assert report.slowest_duration_ms == 2400.0
    assert len(report.spans) >= 8

    # Verify span kinds exist
    kinds = {s.kind for s in report.spans}
    assert SpanKind.SERVER in kinds
    assert SpanKind.CLIENT in kinds
    assert SpanKind.PRODUCER in kinds
    assert SpanKind.CONSUMER in kinds
    assert SpanKind.INTERNAL in kinds


# ─── 5. AI Agent Trace Verifier Tests ─────────────────────────────────────────

def test_ai_agent_trace_verifier():
    verifier = AgentTraceVerifier()
    report = verifier.verify_agent_trace()

    assert report.ai_observability_score == 100.0
    assert report.decision_reconstruction_complete is True
    assert len(report.agent_spans) >= 8

    stages = [s.stage for s in report.agent_spans]
    assert "Goal" in stages
    assert "Planning" in stages
    assert "Tool Selection" in stages
    assert "OCR Execution" in stages
    assert "LLM Extraction" in stages
    assert "Validation" in stages
    assert "Reflection" in stages


# ─── 6. External Dependency Trace Verifier Tests ──────────────────────────────

def test_external_dependency_trace_verifier():
    verifier = ExternalDependencyTraceVerifier()
    report = verifier.verify_dependency_trace()

    assert report.external_tracing_passed is True
    assert len(report.dependencies) >= 4
    assert report.bottleneck_service == "Google Gemini 1.5 Pro"

    dep_names = [d.dependency_name for d in report.dependencies]
    assert "Google Gemini 1.5 Pro" in dep_names
    assert "Tesseract OCR Daemon" in dep_names
    assert "Cloud Object Storage" in dep_names


# ─── 7. Error Diagnostic Trace Verifier Tests ─────────────────────────────────

def test_error_diagnostic_trace_verifier():
    verifier = ErrorDiagnosticTraceVerifier()
    report = verifier.verify_error_trace()

    assert report.error_trace_passed is True
    assert report.error_diagnosable is True
    assert len(report.failed_spans) >= 3

    for fail in report.failed_spans:
        assert fail.exception_type is not None
        assert fail.error_message is not None
        assert fail.stack_trace_ref is not None
        assert fail.recovery_action is not None


# ─── 8. Correlation & Sampling Verifier Tests ─────────────────────────────────

def test_trace_correlation_verifier():
    verifier = TraceCorrelationVerifier()
    report = verifier.verify_correlation()

    assert report.trace_to_log_linking_verified is True
    assert report.metric_to_trace_jump_verified is True
    assert report.red_metrics_correlated is True
    assert report.correlation_score_pct == 100.0


def test_sampling_strategy_verifier():
    verifier = SamplingStrategyVerifier()
    report = verifier.verify_sampling_strategy()

    assert report.sampling_passed is True
    assert report.zero_error_loss is True
    assert report.cost_controlled is True
    assert len(report.sampling_rules) == 3

    prod_rule = next(r for r in report.sampling_rules if r.environment == "production")
    assert prod_rule.sample_rate_normal_traffic_pct == 10.0
    assert prod_rule.sample_rate_errors_pct == 100.0


# ─── 9. Security & Performance Verifier Tests ─────────────────────────────────

def test_trace_security_verifier():
    verifier = TraceSecurityVerifier()
    report = verifier.verify_trace_security()

    assert report.security_score_pct == 100.0
    assert report.forbidden_attributes_prevented is True
    assert report.no_pii_in_spans is True
    for audit in report.audits:
        assert audit.pii_exposed is False
        assert audit.passwords_exposed is False
        assert audit.raw_document_payload_exposed is False
        assert audit.status == "SECURE"


def test_trace_performance_verifier():
    verifier = TracePerformanceVerifier()
    report = verifier.verify_trace_performance()

    assert report.latency_impact_acceptable is True
    assert report.overhead_pct < 5.0
    assert report.benchmark_traces_count == 100000


# ─── 10. Failure Simulation Verifier Tests ────────────────────────────────────

def test_failure_simulation_trace_verifier():
    verifier = FailureSimulationTraceVerifier()
    report = verifier.verify_failure_simulation_traces()

    assert report.all_scenarios_verified is True
    assert len(report.scenarios) == 3

    scenario_ids = [s.scenario_id for s in report.scenarios]
    assert "CHAOS-TRACE-001" in scenario_ids
    assert "CHAOS-TRACE-002" in scenario_ids
    assert "CHAOS-TRACE-003" in scenario_ids

    for sc in report.scenarios:
        assert sc.root_cause_isolated is True
        assert sc.recovery_span_recorded is True


# ─── 11. Quality Scorer Tests ─────────────────────────────────────────────────

def test_tracing_quality_scorer():
    runtime = TracingVerificationRuntime()
    arch = runtime.arch_verifier.verify_tracing_architecture()
    prop = runtime.prop_verifier.verify_context_propagation()
    wf = runtime.wf_verifier.verify_workflow_trace()
    agent = runtime.agent_verifier.verify_agent_trace()
    dep = runtime.dep_verifier.verify_dependency_trace()
    err = runtime.err_verifier.verify_error_trace()
    corr = runtime.corr_verifier.verify_correlation()
    sample = runtime.sample_verifier.verify_sampling_strategy()
    sec = runtime.sec_verifier.verify_trace_security()
    perf = runtime.perf_verifier.verify_trace_performance()
    chaos = runtime.chaos_verifier.verify_failure_simulation_traces()

    scorer = TracingQualityScorer()
    certification = scorer.calculate_certification_score(
        arch_report=arch,
        prop_report=prop,
        wf_report=wf,
        agent_report=agent,
        dep_report=dep,
        err_report=err,
        corr_report=corr,
        sample_report=sample,
        sec_report=sec,
        perf_report=perf,
        chaos_report=chaos,
    )

    assert certification.overall_score_pct >= 95.0
    assert certification.certification_tier == TracingCertificationTier.ENTERPRISE_TRACING_READY
    assert certification.certification_granted is True
    assert len(certification.pillar_scores) == 6

    total_weight = sum(p.weight_pct for p in certification.pillar_scores)
    assert abs(total_weight - 100.0) < 0.001


# ─── 12. Exporter & Runtime Tests ─────────────────────────────────────────────

def test_tracing_evidence_exporter(tmp_path):
    out_dir = str(tmp_path / "observability_verification" / "tracing")
    runtime = TracingVerificationRuntime()
    result = runtime.run_full_verification(export_dir=out_dir)

    metadata = result["metadata"]
    assert metadata["services_instrumented"] == 8
    assert metadata["total_artifacts"] == 10

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


# ─── 13. FastAPI Router Tests ─────────────────────────────────────────────────

def test_tracing_verification_api_endpoints():
    app = FastAPI()
    app.include_router(tracing_api_router)
    client = TestClient(app)

    # Health endpoint
    resp = client.get("/api/v1/tracing-verification/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "HEALTHY"

    # Architecture endpoint
    resp = client.get("/api/v1/tracing-verification/architecture")
    assert resp.status_code == 200
    assert resp.json()["services_instrumented"] == 8

    # Propagation endpoint
    resp = client.get("/api/v1/tracing-verification/propagation")
    assert resp.status_code == 200
    assert resp.json()["context_integrity_pct"] == 100.0

    # Workflow endpoint
    resp = client.get("/api/v1/tracing-verification/workflow")
    assert resp.status_code == 200
    assert resp.json()["workflow_trace_passed"] is True

    # AI Agent endpoint
    resp = client.get("/api/v1/tracing-verification/ai-agent")
    assert resp.status_code == 200
    assert resp.json()["ai_observability_score"] == 100.0

    # Dependencies endpoint
    resp = client.get("/api/v1/tracing-verification/dependencies")
    assert resp.status_code == 200
    assert resp.json()["external_tracing_passed"] is True

    # Errors endpoint
    resp = client.get("/api/v1/tracing-verification/errors")
    assert resp.status_code == 200
    assert resp.json()["error_diagnosable"] is True

    # Correlation endpoint
    resp = client.get("/api/v1/tracing-verification/correlation")
    assert resp.status_code == 200
    assert resp.json()["trace_to_log_linking_verified"] is True

    # Sampling endpoint
    resp = client.get("/api/v1/tracing-verification/sampling")
    assert resp.status_code == 200
    assert resp.json()["sampling_passed"] is True

    # Security endpoint
    resp = client.get("/api/v1/tracing-verification/security")
    assert resp.status_code == 200
    assert resp.json()["security_score_pct"] == 100.0

    # Performance endpoint
    resp = client.get("/api/v1/tracing-verification/performance")
    assert resp.status_code == 200
    assert resp.json()["latency_impact_acceptable"] is True

    # Chaos endpoint
    resp = client.get("/api/v1/tracing-verification/chaos")
    assert resp.status_code == 200
    assert resp.json()["all_scenarios_verified"] is True

    # Scorecard endpoint
    resp = client.get("/api/v1/tracing-verification/scorecard")
    assert resp.status_code == 200
    assert resp.json()["overall_score_pct"] >= 95.0

    # Verification run POST endpoint
    resp = client.post("/api/v1/tracing-verification/verify")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "COMPLETED"
    assert data["certification_tier"] == "Enterprise Tracing Ready"
