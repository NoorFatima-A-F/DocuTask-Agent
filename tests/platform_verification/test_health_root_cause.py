"""Test Suite for Phase 3H.4.2 - Health Root Cause Analysis & Failure Attribution Framework.

Tests all 14 sub-parts of Phase 3H.4.2:
1. Dependency Graph Modeling
2. Health Event Correlation
3. Failure Classification
4. Root Cause Scoring Engine
5. Impact Analysis Engine
6. Incident Severity Classification
7. Failure Timeline Reconstruction
8. Cascading Failure Detection
9. False Positive Reduction
10. Historical Incident Memory
11. Health API Diagnosis Extensions
12. 5 Verification Scenarios
13. Evidence Generation (8 JSON manifests)
14. Quality Scoring (6-dimension weighted scorecard)
Plus FastAPI HTTP router endpoints.
"""

import os
import json
from fastapi.testclient import TestClient
from fastapi import FastAPI

from app.platform_verification.health_root_cause.topology.dependency_graph import (
    DependencyGraphEngine,
)
from app.platform_verification.health_root_cause.correlation.health_event_correlator import (
    HealthEventCorrelator,
)
from app.platform_verification.health_root_cause.classifier.failure_classifier import (
    FailureClassifier,
)
from app.platform_verification.health_root_cause.scoring.root_cause_scorer import (
    RootCauseScorer,
)
from app.platform_verification.health_root_cause.impact.impact_analyzer import (
    ImpactAnalyzer,
)
from app.platform_verification.health_root_cause.timeline.incident_timeline_reconstructor import (
    IncidentTimelineReconstructor,
)
from app.platform_verification.health_root_cause.cascade.cascade_detector import (
    CascadeDetector,
)
from app.platform_verification.health_root_cause.filters.false_positive_filter import (
    FalsePositiveFilter,
)
from app.platform_verification.health_root_cause.memory.incident_memory import (
    IncidentMemoryEngine,
)
from app.platform_verification.health_root_cause.scenarios.rca_scenarios_verifier import (
    RCAScenariosVerifier,
)
from app.platform_verification.health_root_cause.runtime.health_root_cause_runtime import (
    HealthRootCauseRuntime,
)
from app.platform_verification.health_root_cause.api.health_root_cause_api import (
    router as rca_router,
)
from app.platform_verification.health_root_cause.domain.models import (
    FailureCategory,
    IncidentSeverity,
    DiagnosisConfidenceTier,
    RCATier,
)


def test_part_3h_4_2_1_dependency_graph_topology():
    engine = DependencyGraphEngine()
    report = engine.build_graph_report()

    assert report.status == "PASS"
    assert report.total_nodes >= 6
    assert len(report.critical_path_nodes) >= 3
    assert "postgresql" in report.nodes
    assert "redis_queue" in report.nodes
    assert "worker_fleet" in report.nodes

    # Test downstream impact traversal
    downstream_from_pg = engine.get_downstream_dependents("postgresql")
    assert "worker_fleet" in downstream_from_pg
    assert "gemini_ai" in downstream_from_pg


def test_part_3h_4_2_2_health_event_correlator():
    correlator = HealthEventCorrelator()
    report = correlator.correlate_events()

    assert report.status == "PASS"
    assert report.total_clusters >= 3
    assert report.avg_correlation_confidence >= 0.90
    for cluster in report.clusters:
        assert cluster.correlated_signals_count >= 2
        assert cluster.correlation_score >= 0.90
        assert cluster.primary_component != ""


def test_part_3h_4_2_3_failure_and_severity_classification():
    classifier = FailureClassifier()

    cat_db = classifier.classify_category("postgresql", "database connection failed")
    assert cat_db == FailureCategory.DEPENDENCY

    cat_perf = classifier.classify_category("redis_queue", "queue backlog growing")
    assert cat_perf == FailureCategory.PERFORMANCE_DEGRADATION

    cat_ai = classifier.classify_category("gemini_ai", "model 503 error")
    assert cat_ai == FailureCategory.EXTERNAL_SERVICE

    sev_db = classifier.classify_severity("postgresql", FailureCategory.DEPENDENCY)
    assert sev_db == IncidentSeverity.SEV_1_CRITICAL

    sev_queue = classifier.classify_severity("redis_queue", FailureCategory.DEPENDENCY)
    assert sev_queue == IncidentSeverity.SEV_2_MAJOR


def test_part_3h_4_2_4_root_cause_scoring_engine():
    scorer = RootCauseScorer()
    report = scorer.diagnose_root_cause("INC-POSTGRES-001")

    assert report.status == "PASS"
    assert report.primary_root_cause.component == "postgresql"
    assert report.primary_root_cause.confidence >= 0.90
    assert report.primary_root_cause.recommended_action != ""
    assert report.confidence_tier == DiagnosisConfidenceTier.HIGH


def test_part_3h_4_2_5_impact_analysis_engine():
    analyzer = ImpactAnalyzer()
    report = analyzer.analyze_impact("postgresql")

    assert report.status == "PASS"
    assert report.total_assessments >= 1
    assessment = report.assessments[0]
    assert assessment.severity == IncidentSeverity.SEV_1_CRITICAL
    assert len(assessment.affected_services) >= 2
    assert len(assessment.unaffected_services) >= 1
    assert assessment.estimated_blast_radius_pct > 50.0


def test_part_3h_4_2_7_failure_timeline_reconstruction():
    reconstructor = IncidentTimelineReconstructor()
    report = reconstructor.reconstruct_timeline("INC-POSTGRES-001")

    assert report.status == "PASS"
    assert report.timeline_duration_seconds > 0
    assert len(report.milestones) >= 5
    offsets = [m.time_offset for m in report.milestones]
    assert "T+00:00" in offsets
    assert "T+01:30" in offsets


def test_part_3h_4_2_8_cascading_failure_detection():
    detector = CascadeDetector()
    report = detector.detect_cascade("INC-CASCADE-001")

    assert report.status == "PASS"
    assert report.primary_origin_component == "redis_queue"
    assert report.propagation_depth >= 3
    assert report.cascade_prevented is True
    assert report.cascade_chain[0].is_primary_root_cause is True


def test_part_3h_4_2_9_false_positive_reduction():
    filter_engine = FalsePositiveFilter()
    report = filter_engine.audit_false_positive_control()

    assert report.status == "PASS"
    assert report.transient_spikes_damped >= 10
    assert report.false_positive_rate_pct == 0.0


def test_part_3h_4_2_10_historical_incident_memory():
    memory = IncidentMemoryEngine()
    report = memory.get_memory_report()

    assert report.status == "PASS"
    assert report.total_known_signatures >= 4
    for sig in report.signatures:
        assert sig.historical_occurrences > 0
        assert len(sig.matching_indicators) >= 1


def test_part_3h_4_2_12_automated_rca_verification_scenarios():
    verifier = RCAScenariosVerifier()
    report = verifier.verify_scenarios()

    assert report.status == "PASS"
    assert report.total_scenarios == 5
    assert report.passed_scenarios == 5
    assert report.accuracy_rate_pct == 100.0


def test_part_3h_4_2_13_evidence_exporter_and_8_manifests(tmp_path):
    output_dir = str(tmp_path / "test_rca_manifests")
    runtime = HealthRootCauseRuntime(export_dir=output_dir)
    runtime.run_full_verification()

    assert os.path.exists(output_dir)
    expected_files = [
        "dependency_graph_report.json",
        "event_correlation_report.json",
        "failure_classification_report.json",
        "root_cause_report.json",
        "impact_analysis_report.json",
        "incident_timeline_report.json",
        "cascade_detection_report.json",
        "metadata.json",
    ]
    for fname in expected_files:
        fpath = os.path.join(output_dir, fname)
        assert os.path.exists(fpath), f"Missing manifest {fname}"
        with open(fpath, "r", encoding="utf-8") as f:
            data = json.load(f)
            assert data is not None


def test_part_3h_4_2_14_rca_scorer_and_enterprise_tier():
    runtime = HealthRootCauseRuntime()
    res = runtime.run_full_verification()
    scorecard = res["scorecard"]

    assert scorecard.passed is True
    assert scorecard.overall_score >= 95.0
    assert scorecard.certification_tier == RCATier.ENTERPRISE_INCIDENT_DIAGNOSIS_READY
    assert scorecard.certification_verdict == "CERTIFIED"
    assert scorecard.root_cause_accuracy_score >= 95.0
    assert scorecard.dependency_analysis_score >= 95.0
    assert scorecard.impact_prediction_score >= 95.0


def test_health_root_cause_fastapi_endpoints():
    app = FastAPI()
    app.include_router(rca_router)
    client = TestClient(app)

    endpoints = [
        "/health/diagnosis",
        "/health/rca/topology",
        "/health/rca/correlation",
        "/health/rca/impact",
        "/health/rca/cascade",
        "/health/rca/memory",
        "/health/rca/scorecard",
    ]

    for ep in endpoints:
        resp = client.get(ep)
        assert resp.status_code == 200, f"Endpoint {ep} failed with status {resp.status_code}"
        assert resp.json() is not None

    post_resp = client.post("/health/rca/verify")
    assert post_resp.status_code == 200
    data = post_resp.json()
    assert data["scorecard"]["overall_score"] >= 95.0
