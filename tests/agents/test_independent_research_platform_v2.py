"""
Unit and Integration Tests for Research Validation & Scientific Lineage v2
(Phases 72A - 81A)
"""

import json
from research_validation.provenance.independent_verifier import (
    IndependentProvenanceVerifier, VerificationStatus
)
from research_validation.provenance.evidence_graph import EvidenceGraph
from research_validation.provenance.provenance_models import (
    LineageStage, EvidenceQualityLevel
)
from research_validation.datasets.public_benchmarks import DatasetType
from research_validation.datasets.benchmark_executor import (
    PublicBenchmarkExecutor, BenchmarkExecutionStatus, compute_wilson_ci, compute_anls
)
from research_validation.endurance.experiment_scheduler import (
    AsynchronousExperimentScheduler, ExperimentStatus
)
from research_validation.telemetry.production_evidence_collector import (
    ProductionEvidenceCollector, TelemetryCollectionStatus
)
from research_validation.claims.claim_verifier import (
    ScientificClaimVerifier
)
from research_validation.reproducibility.reproduce_all import (
    MasterReproducibilityOrchestrator, ReproducibilityVerdict
)
from research_validation.meta_validation.validator_benchmark import (
    ValidatorMetaBenchmarkRunner
)
from research_validation.threats.threats_to_validity_generator import (
    ThreatsToValidityGenerator, ValidityDimension
)
from research_validation.workspace.reviewer_workspace import ReviewerWorkspaceBuilder
from research_validation.confidence.scientific_confidence_engine import (
    ScientificConfidenceEngine, ScientificReadinessBadge
)


# 1. Phase 72A: Independent Provenance Verification Engine
def test_independent_provenance_verifier_jsonld_valid():
    valid_jsonld = json.dumps({
        "@context": {"prov": "http://www.w3.org/ns/prov#"},
        "@graph": [
            {"@id": "ent:1", "@type": "prov:Entity", "prov:generatedAtTime": "2026-09-08T00:00:00Z"},
            {"@id": "act:1", "@type": "prov:Activity", "prov:startedAtTime": "2026-09-08T00:00:00Z", "prov:endedAtTime": "2026-09-08T00:01:00Z"},
            {"@id": "ag:1", "@type": "prov:Agent"}
        ]
    })
    res = IndependentProvenanceVerifier.verify_w3c_prov_jsonld(valid_jsonld)
    assert res.is_valid is True
    assert res.status == VerificationStatus.CONSISTENT
    assert res.checked_entities == 1
    assert res.checked_activities == 1
    assert res.checked_agents == 1


def test_independent_provenance_verifier_conflict_detection():
    graph = EvidenceGraph("audit_graph")
    valid_jsonld = json.dumps({
        "@context": {"prov": "http://www.w3.org/ns/prov#"},
        "@graph": [{"@id": "e1", "@type": "prov:Entity"}]
    })
    bad_xml = "<invalid xml"
    consensus = IndependentProvenanceVerifier.multi_strategy_consensus(
        graph,
        serializations={"jsonld": valid_jsonld, "prov_xml": bad_xml}
    )
    assert consensus.consensus_status == VerificationStatus.VALIDATION_CONFLICT
    assert consensus.agreement_ratio == 0.5


def test_independent_provenance_dag_replay():
    graph = EvidenceGraph("replay_test")
    graph.record_node("n1", LineageStage.RAW_OBSERVATION, "Input", "Input observation", {"data": 123}, [], EvidenceQualityLevel.LEVEL_C)

    steps = [{"id": "n1", "content": {"entity_name": "Input"}, "parent_ids": []}]
    comparison = IndependentProvenanceVerifier.replay_and_compare(graph, steps)
    assert comparison.matched_nodes == 1
    assert comparison.status == VerificationStatus.CONSISTENT



# 2. Phase 73A: Public Benchmark Execution Framework
def test_public_benchmark_executor_dataset_unavailable():
    executor = PublicBenchmarkExecutor(data_root_dir="non_existent_path_xyz")
    res = executor.execute_benchmark(DatasetType.FUNSD)
    assert res.status == BenchmarkExecutionStatus.DATASET_UNAVAILABLE
    assert res.is_measured is False
    assert "Dataset unavailable" in res.diagnostic_message


def test_public_benchmark_executor_with_samples():
    executor = PublicBenchmarkExecutor()
    samples = [
        {"ground_truth_label": "header", "pred": {"label": "header"}},
        {"ground_truth_label": "question", "pred": {"label": "question"}},
        {"ground_truth_label": "answer", "pred": {"label": "other"}},
    ]
    res = executor.execute_benchmark(DatasetType.FUNSD, mock_samples_for_test=samples)
    assert res.status == BenchmarkExecutionStatus.COMPLETED
    assert res.is_measured is True
    assert res.sample_count == 3
    assert res.precision > 0.0
    assert res.recall > 0.0
    assert res.f1_score > 0.0
    assert len(res.merkle_evidence_hash) == 64


def test_wilson_ci_and_anls():
    ci = compute_wilson_ci(90, 100, confidence=0.95)
    assert 0.80 < ci.lower < 0.90
    assert 0.90 < ci.upper < 1.00

    anls = compute_anls("Total: $100.00", "Total: $100.00")
    assert anls == 1.0
    anls_partial = compute_anls("Total: $100.00", "Total: $100.0")
    assert 0.8 < anls_partial < 1.0


# 3. Phase 74A: Asynchronous Scientific Experiment Scheduler
def test_experiment_scheduler_lifecycle():
    scheduler = AsynchronousExperimentScheduler()
    job = scheduler.schedule_experiment("Soak 72h Test", planned_duration_seconds=10.0)
    assert job.status == ExperimentStatus.SCHEDULED

    job = scheduler.start_experiment(job.job_id)
    assert job.status == ExperimentStatus.RUNNING

    ckpt = scheduler.record_checkpoint(job.job_id, elapsed_delta_seconds=5.0, metrics={"rss_mb": 128.0})
    assert ckpt.step_index == 1
    assert job.actual_elapsed_seconds == 5.0

    # Trigger completion
    scheduler.record_checkpoint(job.job_id, elapsed_delta_seconds=6.0, metrics={"rss_mb": 130.0})
    assert job.status == ExperimentStatus.COMPLETED
    assert job.actual_elapsed_seconds == 11.0

    state_json = scheduler.export_state_json()
    assert "Soak 72h Test" in state_json


# 4. Phase 75A: Production Evidence Collector
def test_production_evidence_collector():
    collector = ProductionEvidenceCollector(gcp_project_id="test-project")
    # Live measured telemetry
    cr_snap = collector.collect_cloud_run_metrics(
        service_name="doc-processor-api",
        live_telemetry_dict={"cpu_throttling_seconds": 0.02, "cold_start_count": 1.0}
    )
    assert cr_snap.is_measured is True
    assert cr_snap.status == TelemetryCollectionStatus.MEASURED_LIVE

    # Uncollected fallback
    sql_snap = collector.collect_cloud_sql_metrics(instance_name="doc-db-primary")
    assert sql_snap.is_measured is False
    assert sql_snap.status == TelemetryCollectionStatus.NOT_COLLECTED

    report = collector.generate_report([cr_snap, sql_snap])
    assert report.total_services_audited == 2
    assert report.measured_live_services == 1
    assert report.uncollected_services == 1
    assert report.measured_ratio == 0.5


# 5. Phase 76A: Scientific Claim Verification Engine
def test_claim_verification_engine():
    graph = EvidenceGraph("claim_graph")
    graph.record_node("n1", LineageStage.RAW_OBSERVATION, "Benchmark F1 Measurement", "Empirical measurement", {"precision": 0.985}, [], EvidenceQualityLevel.LEVEL_A)

    verifier = ScientificClaimVerifier(graph)
    text = (
        "We observed and benchmarked a 98.5% precision score across tests.\n"
        "According to CVPR prior work, baseline accuracy is 82.0%.\n"
        "Our system achieves infinite speed with zero memory."
    )
    audit = verifier.audit_document_claims(text)
    assert audit.total_claims == 3
    assert audit.claim_groundedness_index >= 0.33
    assert len(audit.unsupported_claims) >= 1
    assert len(audit.merkle_claim_root) == 64



# 6. Phase 77A: One-Command Reproducibility Platform
def test_master_reproducibility_orchestrator():
    orchestrator = MasterReproducibilityOrchestrator()
    mock_samples = {
        DatasetType.FUNSD: [{"ground_truth_label": "header", "pred": {"label": "header"}}],
        DatasetType.CORD: [{"ground_truth_label": "total", "pred": {"label": "total"}}],
    }
    report = orchestrator.run_all(mock_benchmark_samples=mock_samples)
    assert report.total_stages == 6
    assert report.passed_stages == 6
    assert report.verdict in (ReproducibilityVerdict.RESULTS_REPRODUCED, ReproducibilityVerdict.PARTIALLY_REPRODUCED)
    assert len(report.reproducibility_hash) == 64


# 7. Phase 78A: Validator Benchmark Framework
def test_validator_meta_benchmark():
    runner = ValidatorMetaBenchmarkRunner()
    report = runner.run_benchmark()
    assert report.total_mutations_evaluated >= 5
    assert report.sensitivity_recall >= 0.80
    assert report.specificity >= 0.80
    assert report.f1_score >= 0.80
    assert report.roc_auc >= 0.80


# 8. Phase 79A: Threats-To-Validity Generator
def test_threats_to_validity_generator():
    generator = ThreatsToValidityGenerator()
    doc = generator.synthesize_document()
    assert doc.total_threats >= 7
    assert doc.mitigated_threats >= 7
    assert doc.mitigation_ratio == 1.0
    assert ValidityDimension.INTERNAL_VALIDITY.value in doc.threats_by_dimension
    assert ValidityDimension.EXTERNAL_VALIDITY.value in doc.threats_by_dimension
    assert "# Threats to Scientific Validity" in doc.markdown_report


# 9. Phase 80A: External Reviewer Workspace
def test_reviewer_workspace_builder(tmp_path):
    builder = ReviewerWorkspaceBuilder()
    manifest = builder.build_workspace(output_dir=str(tmp_path))
    assert manifest.ready_for_acm_artifacts_evaluated is True
    assert manifest.ready_for_mlcommons_submission is True
    assert (tmp_path / "REPRODUCE.md").exists()
    assert (tmp_path / "ACM_CHECKLIST.md").exists()
    assert (tmp_path / "MANIFEST.json").exists()


# 10. Phase 81A: Scientific Confidence Assessment Engine
def test_scientific_confidence_engine():
    engine = ScientificConfidenceEngine()
    report = engine.compute_assessment(
        evidence_quality_score=0.92,
        statistical_rigor_score=0.88,
        provenance_completeness_score=0.95,
        reproducibility_score=0.90,
        threat_mitigation_score=0.90,
        meta_validation_score=0.92,
        quality_level_counts={
            EvidenceQualityLevel.LEVEL_A: 10,
            EvidenceQualityLevel.LEVEL_B: 5,
        }
    )
    assert report.arithmetic_mean_score >= 0.85
    assert report.geometric_mean_score >= 0.85
    assert report.harmonic_mean_score >= 0.85
    assert ScientificReadinessBadge.READY_FOR_ACM_ARTIFACT_SUBMISSION in report.awarded_badges
    assert report.is_ready_for_submission is True
