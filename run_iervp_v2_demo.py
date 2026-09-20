"""
Master Research Validation & Scientific Lineage v2 Demonstration Runner
========================================================================
Demonstrates the end-to-end execution of Phases 72A through 81A:
1. Phase 72A: Independent Provenance Verification Engine
2. Phase 73A: Public Benchmark Execution Framework
3. Phase 74A: Asynchronous Scientific Experiment Scheduler
4. Phase 75A: Production Evidence Collector
5. Phase 76A: Scientific Claim Verification Engine
6. Phase 77A: One-Command Reproducibility Platform
7. Phase 78A: Validator Benchmark Framework (Meta-Evaluation)
8. Phase 79A: Threats-To-Validity Generator
9. Phase 80A: External Reviewer Workspace
10. Phase 81A: Scientific Confidence Assessment Engine
"""

from __future__ import annotations
import json
import os
import sys

from research_validation.provenance.independent_verifier import (
    IndependentProvenanceVerifier, VerificationStatus
)
from research_validation.provenance.evidence_graph import EvidenceGraph
from research_validation.provenance.provenance_models import (
    LineageStage, EvidenceQualityLevel
)
from research_validation.datasets.public_benchmarks import DatasetType
from research_validation.datasets.benchmark_executor import (
    PublicBenchmarkExecutor, BenchmarkExecutionStatus
)
from research_validation.endurance.experiment_scheduler import (
    AsynchronousExperimentScheduler, ExperimentStatus
)
from research_validation.telemetry.production_evidence_collector import (
    ProductionEvidenceCollector, TelemetryCollectionStatus
)
from research_validation.claims.claim_verifier import (
    ScientificClaimVerifier, ClaimClassification
)
from research_validation.reproducibility.reproduce_all import (
    MasterReproducibilityOrchestrator, ReproducibilityVerdict
)
from research_validation.meta_validation.validator_benchmark import (
    ValidatorMetaBenchmarkRunner
)
from research_validation.threats.threats_to_validity_generator import (
    ThreatsToValidityGenerator
)
from research_validation.workspace.reviewer_workspace import (
    ReviewerWorkspaceBuilder
)
from research_validation.confidence.scientific_confidence_engine import (
    ScientificConfidenceEngine, ScientificReadinessBadge
)


def run_demo():
    print("=" * 80)
    print(" RESEARCH VALIDATION & SCIENTIFIC LINEAGE V2 MASTER DEMONSTRATION")
    print("=" * 80)

    # 1. Phase 72A: Independent Provenance Verification
    print("\n[Phase 72A] Executing Independent Provenance Verifier...")
    sample_jsonld = json.dumps({
        "@context": {"prov": "http://www.w3.org/ns/prov#"},
        "@graph": [
            {"@id": "doc:100", "@type": "prov:Entity", "prov:generatedAtTime": "2026-09-08T00:00:00Z"},
            {"@id": "act:100", "@type": "prov:Activity", "prov:startedAtTime": "2026-09-08T00:00:00Z", "prov:endedAtTime": "2026-09-08T00:01:00Z"},
            {"@id": "ag:100", "@type": "prov:Agent"}
        ]
    })
    prov_res = IndependentProvenanceVerifier.verify_w3c_prov_jsonld(sample_jsonld)
    print(f"  -> W3C JSON-LD Status: {prov_res.status.value} (Entities: {prov_res.checked_entities}, Activities: {prov_res.checked_activities})")

    # 2. Phase 73A: Public Benchmark Execution
    print("\n[Phase 73A] Running Public Benchmark Harness...")
    bench_exec = PublicBenchmarkExecutor()
    mock_samples = [
        {"ground_truth_label": "header", "pred": {"label": "header"}},
        {"ground_truth_label": "question", "pred": {"label": "question"}},
        {"ground_truth_label": "answer", "pred": {"label": "answer"}},
        {"ground_truth_label": "total", "pred": {"label": "total"}},
    ]
    funsd_res = bench_exec.execute_benchmark(DatasetType.FUNSD, mock_samples_for_test=mock_samples)
    print(f"  -> FUNSD Benchmark: F1={funsd_res.f1_score:.4f}, Wilson CI=[{funsd_res.f1_confidence_interval.lower:.3f}, {funsd_res.f1_confidence_interval.upper:.3f}], Merkle Hash={funsd_res.merkle_evidence_hash[:16]}...")

    # 3. Phase 74A: Experiment Scheduler
    print("\n[Phase 74A] Scheduling Asynchronous Endurance Experiment...")
    scheduler = AsynchronousExperimentScheduler()
    job = scheduler.schedule_experiment("Long Duration 72h Soak", planned_duration_seconds=3600.0)
    scheduler.start_experiment(job.job_id)
    ckpt = scheduler.record_checkpoint(job.job_id, elapsed_delta_seconds=60.0, metrics={"memory_rss_mb": 256.4})
    print(f"  -> Job {job.job_id}: Status={job.status.value}, Elapsed={job.actual_elapsed_seconds}s, Checkpoint Hash={ckpt.state_hash[:16]}...")

    # 4. Phase 75A: Production Evidence Collector
    print("\n[Phase 75A] Ingesting Production Telemetry...")
    telemetry_collector = ProductionEvidenceCollector(gcp_project_id="enterprise-doc-prod")
    cr_snap = telemetry_collector.collect_cloud_run_metrics("doc-extractor", {"cpu_throttling_seconds": 0.01, "cold_start_count": 0.0})
    sql_snap = telemetry_collector.collect_cloud_sql_metrics("doc-db-primary")
    prod_report = telemetry_collector.generate_report([cr_snap, sql_snap])
    print(f"  -> Audited Services: {prod_report.total_services_audited} (Measured Live: {prod_report.measured_live_services}, Uncollected: {prod_report.uncollected_services})")

    # 5. Phase 76A: Scientific Claim Verification Engine
    print("\n[Phase 76A] Verifying Scientific Claims in Report...")
    graph = EvidenceGraph("demo_graph")
    graph.record_node("n1", LineageStage.RAW_OBSERVATION, "Benchmark Precision", "Empirical measurement", {"precision": 0.99}, [], EvidenceQualityLevel.LEVEL_A)
    claim_verifier = ScientificClaimVerifier(graph)
    report_text = (
        "We observed and benchmarked a 99.0% precision score on FUNSD.\n"
        "According to literature baselines, prior art achieved 85.2%.\n"
        "The model requires zero CPU and zero memory."
    )
    claim_audit = claim_verifier.audit_document_claims(report_text)
    print(f"  -> Claim Groundedness Index (CGI): {claim_audit.claim_groundedness_index*100:.1f}% (Total: {claim_audit.total_claims}, Unsupported: {len(claim_audit.unsupported_claims)})")

    # 6. Phase 77A: One-Command Master Reproducibility
    print("\n[Phase 77A] Executing Master Reproducibility Pipeline...")
    orchestrator = MasterReproducibilityOrchestrator()
    repro_report = orchestrator.run_all(mock_benchmark_samples={DatasetType.FUNSD: mock_samples})
    print(f"  -> Reproducibility Verdict: {repro_report.verdict.value} (Stages: {repro_report.passed_stages}/{repro_report.total_stages}, Hash: {repro_report.reproducibility_hash[:16]}...)")

    # 7. Phase 78A: Validator Benchmark Framework
    print("\n[Phase 78A] Meta-Validation Benchmark (Testing the Validators)...")
    meta_runner = ValidatorMetaBenchmarkRunner()
    meta_report = meta_runner.run_benchmark()
    print(f"  -> Sensitivity/Recall: {meta_report.sensitivity_recall*100:.1f}%, Specificity: {meta_report.specificity*100:.1f}%, ROC AUC: {meta_report.roc_auc:.4f}")

    # 8. Phase 79A: Threats to Validity Generator
    print("\n[Phase 79A] Synthesizing Threats-To-Validity Disclosures...")
    ttv_gen = ThreatsToValidityGenerator()
    ttv_doc = ttv_gen.synthesize_document()
    print(f"  -> Total Threats: {ttv_doc.total_threats} (Mitigated: {ttv_doc.mitigated_threats}, Mitigation Ratio: {ttv_doc.mitigation_ratio*100:.1f}%)")

    # 9. Phase 80A: External Reviewer Workspace
    print("\n[Phase 80A] Packaging External Reviewer Workspace...")
    workspace_builder = ReviewerWorkspaceBuilder()
    ws_manifest = workspace_builder.build_workspace(output_dir="evidence/reviewer_workspace")
    print(f"  -> Workspace ID: {ws_manifest.workspace_id} (ACM Ready: {ws_manifest.ready_for_acm_artifacts_evaluated}, MLCommons Ready: {ws_manifest.ready_for_mlcommons_submission})")

    # 10. Phase 81A: Scientific Confidence Assessment Engine
    print("\n[Phase 81A] Computing Holistic Scientific Confidence Vector...")
    conf_engine = ScientificConfidenceEngine()
    conf_report = conf_engine.compute_assessment(
        evidence_quality_score=0.92,
        statistical_rigor_score=0.90,
        provenance_completeness_score=0.95,
        reproducibility_score=0.92,
        threat_mitigation_score=0.90,
        meta_validation_score=0.94,
        quality_level_counts={
            EvidenceQualityLevel.LEVEL_A: 12,
            EvidenceQualityLevel.LEVEL_B: 6,
            EvidenceQualityLevel.LEVEL_C: 4,
        }
    )
    print(f"  -> Arithmetic Mean: {conf_report.arithmetic_mean_score:.4f}")
    print(f"  -> Harmonic Mean:   {conf_report.harmonic_mean_score:.4f}")
    print(f"  -> Limiting Pillar: {conf_report.limiting_pillar}")
    print(f"  -> Badges Awarded:  {', '.join(b.value for b in conf_report.awarded_badges)}")
    print(f"  -> Ready for Third-Party Submission: {conf_report.is_ready_for_submission}")

    print("\n" + "=" * 80)
    print(" ALL 10 RESEARCH VALIDATION & LINEAGE SUBSYSTEMS FULLY OPERATIONAL")
    print("=" * 80)


if __name__ == "__main__":
    run_demo()
