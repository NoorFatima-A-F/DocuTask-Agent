"""
Comprehensive Test Suite for Orchestrated Scientific Experimentation Platform
(Phases 82B.1 through 82B.12)
"""

import pytest
from research_validation.scientific_execution.experiment_manifest import (
    ExperimentManifest, ExperimentParameters, DatasetFingerprint, ExperimentStatus
)
from research_validation.scientific_execution.experiment_registry import (
    ExperimentRegistry
)
from research_validation.scientific_execution.experiment_dependency_graph import (
    ExperimentDependencyGraph, PipelineStageType, NodeState
)
from research_validation.scientific_execution.experiment_runner import (
    ScientificExperimentRunner, ExperimentRunResult
)
from research_validation.scientific_execution.experiment_orchestrator import (
    ScientificExperimentOrchestrator
)
from research_validation.scientific_execution.experiment_replay import (
    ExperimentReplayEngine
)
from research_validation.scientific_execution.experiment_archive import (
    ExperimentArchiver
)
from research_validation.scientific_execution.experiment_versioning import (
    ExperimentVersionManager, VersionChangeType
)
from research_validation.scientific_execution.experiment_scheduler_v2 import (
    ExperimentSchedulerV2, PriorityLevel
)
from research_validation.scientific_execution.evidence_reconciliation import (
    EvidenceReconciliationEngine, ConflictSeverity
)
from research_validation.artifact_generation.paper_figures import (
    PaperFigureGenerator
)
from research_validation.artifact_generation.publication_tables import (
    PublicationTableGenerator
)
from research_validation.artifact_generation.latex_export import LatexExporter
from research_validation.artifact_generation.markdown_export import MarkdownExporter
from research_validation.artifact_generation.csv_export import CSVExporter
from research_validation.artifact_generation.parquet_export import ParquetDatasetExporter
from research_validation.artifact_generation.artifact_index import ArtifactIndexer
from research_validation.review.artifact_completeness_checker import (
    ArtifactCompletenessChecker
)
from research_validation.review.review_score_predictor import (
    ReviewVerdict
)
from research_validation.review.review_simulator import ReviewSimulator
from research_validation.review.review_readiness_matrix import (
    ReviewReadinessMatrixBuilder
)
from research_validation.uncertainty.uncertainty_propagation import (
    UncertaintyPropagationEngine
)
from research_validation.uncertainty.confidence_budget import (
    ConfidenceBudgetManager, BudgetStatus
)
from research_validation.uncertainty.evidence_weighting import (
    DynamicEvidenceWeightEngine, EvidenceQualityLevel
)
from research_validation.uncertainty.calibration import EmpiricalCalibrationEngine
from research_validation.reproducibility.cross_platform_runner import (
    CrossPlatformRunner
)
from research_validation.reproducibility.cross_architecture_runner import (
    CrossArchitectureRunner
)
from research_validation.reproducibility.environment_diff import EnvironmentDiffEngine
from research_validation.reproducibility.binary_reproducibility import BinaryReproducibilityAnalyzer


# Fixture: Sample Manifest
@pytest.fixture
def sample_manifest() -> ExperimentManifest:
    return ExperimentManifest.create(
        title="Document OCR Benchmark Experiment",
        description="Evaluates entity recognition on receipt and invoice datasets.",
        parameters=ExperimentParameters(sample_count=100, seed=42),
        dataset=DatasetFingerprint(
            dataset_name="FUNSD",
            dataset_version="1.0.0",
            expected_sample_count=100,
            sha256_checksum="a" * 64,
        ),
        environment={"os": "Windows", "python": "3.14.0"},
        quality_level=EvidenceQualityLevel.LEVEL_A,
        tags=("ocr", "funsd", "benchmark"),
    )


# 1. Phase 82B.1: Experiment Manifest & Registry
def test_experiment_manifest_sealing(sample_manifest):
    assert sample_manifest.experiment_id.startswith("exp_")
    assert len(sample_manifest.manifest_digest_sha256) == 64
    canonical = sample_manifest.to_canonical_dict()
    assert canonical["title"] == "Document OCR Benchmark Experiment"


def test_experiment_registry_duplicate_prevention(sample_manifest, tmp_path):
    registry = ExperimentRegistry(storage_dir=str(tmp_path))
    record = registry.register(sample_manifest)
    assert record.status == ExperimentStatus.REGISTERED
    assert record.manifest.experiment_id == sample_manifest.experiment_id

    # Overwriting is forbidden
    with pytest.raises(ValueError, match="already registered"):
        registry.register(sample_manifest)

    # Update status
    updated = registry.update_status(sample_manifest.experiment_id, ExperimentStatus.COMPLETED, run_hash="hash123")
    assert updated.status == ExperimentStatus.COMPLETED
    assert updated.execution_count == 1


# 2. Phase 82B.2: Experiment Dependency Graph & Invalidation
def test_experiment_dependency_graph_invalidation():
    dag = ExperimentDependencyGraph("test_dag")
    dag.add_node("raw", PipelineStageType.RAW_DATASET, "Raw Dataset")
    dag.add_node("prep", PipelineStageType.PREPROCESSING, "Preprocessing", ["raw"])
    dag.add_node("bench", PipelineStageType.BENCHMARK, "Benchmark", ["prep"])
    dag.add_node("vis", PipelineStageType.VISUALIZATION, "Visualization", ["bench"])

    order = dag.topological_sort()
    assert order == ["raw", "prep", "bench", "vis"]

    # Invalidate prep -> bench and vis must become INVALIDATED
    dag.update_node_output("raw", "hash_raw")
    dag.update_node_output("prep", "hash_prep")
    dag.update_node_output("bench", "hash_bench")
    dag.update_node_output("vis", "hash_vis")

    invalidated = dag.invalidate_node("prep")
    assert "prep" in invalidated
    assert "bench" in invalidated
    assert "vis" in invalidated
    assert "raw" not in invalidated
    assert dag.get_node("bench").state == NodeState.INVALIDATED


# 3. Phase 82B.3: Runner, Orchestrator, Replay, Archive, Versioning, Scheduler
def test_scientific_runner_and_orchestrator(sample_manifest):
    orchestrator = ScientificExperimentOrchestrator()
    mock_samples = [
        {"ground_truth_label": "header", "pred": {"label": "header"}},
        {"ground_truth_label": "total", "pred": {"label": "total"}},
        {"ground_truth_label": "date", "pred": {"label": "date"}},
    ]
    report = orchestrator.run_experiment(sample_manifest, mock_samples=mock_samples)
    assert report.status == ExperimentStatus.COMPLETED
    assert report.run_result.metrics["f1"] == 1.0
    assert report.run_result.is_measured is True
    assert len(report.provenance_graph_digest) == 64


def test_experiment_replay(sample_manifest):
    runner = ScientificExperimentRunner()
    mock_samples = [{"ground_truth_label": "total", "pred": {"label": "total"}}]
    orig_res = runner.execute(sample_manifest, mock_dataset_samples=mock_samples)

    replay_engine = ExperimentReplayEngine()
    rep_report = replay_engine.replay_and_compare(sample_manifest, orig_res, mock_samples=mock_samples)
    assert rep_report.is_reproduced is True
    assert rep_report.hash_match is True
    assert rep_report.metric_comparisons["f1"].within_tolerance is True


def test_experiment_archiver(sample_manifest, tmp_path):
    archiver = ExperimentArchiver(output_root=str(tmp_path))
    bundle = archiver.create_bundle(sample_manifest)
    assert bundle.experiment_id == sample_manifest.experiment_id
    assert "MANIFEST.json" in bundle.included_files
    assert len(bundle.bundle_sha256) == 64


def test_experiment_version_manager(sample_manifest):
    new_manifest = ExperimentManifest.create(
        title="Document OCR Benchmark Experiment v2",
        description="Updated parameters",
        parameters=ExperimentParameters(sample_count=200, seed=42),
        dataset=sample_manifest.dataset,
        environment=sample_manifest.environment,
        semantic_version="1.1.0",
    )
    diff = ExperimentVersionManager.diff_manifests(sample_manifest, new_manifest)
    assert diff.change_type == VersionChangeType.MINOR_FEATURE
    assert diff.is_backward_compatible is True


def test_experiment_scheduler_v2(sample_manifest):
    scheduler = ExperimentSchedulerV2(max_concurrency=2)
    job1 = scheduler.submit_job(sample_manifest, priority=PriorityLevel.CRITICAL)
    job2 = scheduler.submit_job(sample_manifest, priority=PriorityLevel.LOW, dependencies=[job1.job_id])

    # job1 should be ready
    runnable = scheduler.get_next_runnable_job()
    assert runnable.job_id == job1.job_id

    # job2 should NOT be runnable yet because job1 is running
    assert scheduler.get_next_runnable_job() is None

    # Mark job1 complete
    scheduler.mark_job_completed(job1.job_id, is_success=True)

    # Now job2 should be runnable
    runnable2 = scheduler.get_next_runnable_job()
    assert runnable2.job_id == job2.job_id


# 4. Phase 82B.4: Evidence Reconciliation Engine
def test_evidence_reconciliation():
    r1 = ExperimentRunResult(
        run_id="r1", experiment_id="exp1", status=ExperimentStatus.COMPLETED,
        start_time_utc="", end_time_utc="", duration_ms=100.0,
        metrics={"f1": 0.950, "precision": 0.960},
        intermediate_hashes={}, final_output_digest="h1", is_measured=True
    )
    r2 = ExperimentRunResult(
        run_id="r2", experiment_id="exp1", status=ExperimentStatus.COMPLETED,
        start_time_utc="", end_time_utc="", duration_ms=102.0,
        metrics={"f1": 0.952, "precision": 0.958},
        intermediate_hashes={}, final_output_digest="h2", is_measured=True
    )
    reconciler = EvidenceReconciliationEngine()
    consensus = reconciler.reconcile_runs([r1, r2])
    assert consensus.is_consensus_reached is True
    assert consensus.overall_severity in (ConflictSeverity.NONE, ConflictSeverity.NEGLIGIBLE)
    assert 0.950 <= consensus.reconciled_metrics["f1"] <= 0.952


# 5. Phase 82B.5: Artifact Generators & Indexer
def test_artifact_generation_pipeline(sample_manifest):
    # Figures
    fig = PaperFigureGenerator.generate_benchmark_bar_chart_svg(
        benchmark_metrics={"FUNSD": 0.92, "CORD": 0.95, "DocVQA": 0.88},
        originating_exp_id=sample_manifest.experiment_id,
    )
    assert "<svg" in fig.content
    assert sample_manifest.experiment_id in fig.content

    # Tables
    tbl = PublicationTableGenerator.create_benchmark_comparison_table(
        dataset_results=[
            {"dataset": "FUNSD", "samples": 199, "precision": 0.92, "recall": 0.91, "f1_score": 0.915, "p99_latency_ms": 42.0, "evidence_level": "LEVEL_A"}
        ],
        originating_exp_id=sample_manifest.experiment_id,
    )
    latex_code = LatexExporter.export_table(tbl)
    assert r"\begin{table}" in latex_code

    md_code = MarkdownExporter.export_table(tbl)
    assert "| Dataset |" in md_code

    csv_data, csv_sha = CSVExporter.export_table_to_csv(tbl)
    assert "Dataset,Samples" in csv_data
    assert len(csv_sha) == 64

    col_data = ParquetDatasetExporter.export_table_columnar(tbl)
    assert col_data.row_count == 1

    # Indexer
    indexer = ArtifactIndexer()
    indexer.register_figure(fig, "figures/benchmark.svg")
    indexer.register_table(tbl, "tables/benchmark.tbl")
    idx = indexer.build_master_index()
    assert idx.total_artifacts == 2
    assert len(idx.master_index_root_hash) == 64


# 6. Phase 82B.6 & 82B.7: Reproducibility & Binary Checks
def test_cross_platform_and_architecture_runners():
    cp_rep = CrossPlatformRunner.evaluate_platforms(
        experiment_id="exp_cp_test",
        current_metrics={"f1": 0.94},
    )
    assert len(cp_rep.executed_platforms) >= 1
    assert cp_rep.is_cross_platform_reproducible is True

    ca_rep = CrossArchitectureRunner.evaluate_architectures(
        experiment_id="exp_ca_test",
        current_f1=0.94,
    )
    assert len(ca_rep.measured_architectures) >= 1
    assert ca_rep.is_ieee754_consistent is True


def test_environment_and_binary_diff():
    env1 = {"os": "Linux", "python": "3.14.0", "package_versions": {"fastapi": "0.110.0"}}
    env2 = {"os": "Linux", "python": "3.14.0", "package_versions": {"fastapi": "0.110.0"}}
    diff = EnvironmentDiffEngine.diff_environments(env1, env2)
    assert diff.is_identical is True

    bin_rep = BinaryReproducibilityAnalyzer.audit_environment_binaries()
    assert bin_rep.bit_identical_count >= 1


# 7. Phase 82B.8 & 82B.9: Uncertainty & Calibration
def test_uncertainty_propagation_and_budget():
    stages = [
        ("Observation", 100.0, 1.0),
        ("Preprocessing", 98.0, 0.8),
        ("Aggregation", 95.0, 0.5),
    ]
    unc_report = UncertaintyPropagationEngine.propagate_chain("pipe_1", "accuracy", stages)
    assert unc_report.nominal_value == 95.0
    assert unc_report.total_propagated_standard_error > 0.0

    b_mgr = ConfidenceBudgetManager(max_allowed_std_error=0.10)
    b_report = b_mgr.audit_budget([("Stage1", 0.02), ("Stage2", 0.01)])
    assert b_report.status == BudgetStatus.WITHIN_BUDGET


def test_dynamic_evidence_weights_and_calibration():
    counts = {
        EvidenceQualityLevel.LEVEL_A: 50,
        EvidenceQualityLevel.LEVEL_B: 20,
        EvidenceQualityLevel.LEVEL_C: 10,
    }
    weights_scheme = DynamicEvidenceWeightEngine.compute_dynamic_weights(counts)
    assert weights_scheme.weights[EvidenceQualityLevel.LEVEL_A] > 0.0

    sens_rep = DynamicEvidenceWeightEngine.evaluate_weight_sensitivity(counts)
    assert sens_rep.is_robust is True

    calib_rep = EmpiricalCalibrationEngine.evaluate_calibration(
        confidences=[0.9, 0.8, 0.7, 0.6, 0.5],
        ground_truths=[1, 1, 1, 0, 0],
        num_bins=5,
    )
    assert calib_rep.expected_calibration_error >= 0.0


# 8. Phase 82B.10 - 82B.12: Review Simulation & Readiness Matrix
def test_review_simulation_and_completeness():
    complete_payload = {
        "raw_evidence": [{"sample_id": 1, "score": 0.95}],
        "provenance_chain": {"root": "hash123"},
        "uncertainty_bounds": {"f1_ci": [0.91, 0.99]},
        "methodology": "Zero-trust empirical benchmarking with monotonic clock instrumentation.",
        "assumptions": ["Host CPU is not throttled during run."],
        "limitations": ["Evaluated on English language documents only."],
        "dataset_references": ["https://guillaumejaume.github.io/FUNSD/"],
        "environment_manifest": {"os": "Windows", "python": "3.14.0"},
        "reproduction_command": "poetry run python -m research_validation.reproducibility.reproduce_all",
        "version_information": "1.0.0",
    }
    comp_rep = ArtifactCompletenessChecker.audit_artifact("art_001", complete_payload)
    assert comp_rep.is_fully_complete is True
    assert comp_rep.completeness_ratio == 1.0

    review_sim = ReviewSimulator.simulate_review("art_001", complete_payload)
    assert review_sim.verdict == ReviewVerdict.ACCEPT_ARTIFACT_REPRODUCED
    assert review_sim.predicted_score >= 4.5


def test_review_readiness_matrix():
    matrix_rep = ReviewReadinessMatrixBuilder.build_matrix()
    assert matrix_rep.total_dimensions == 6
    assert matrix_rep.complete_dimensions_count == 6
    assert matrix_rep.is_ready_for_submission is True
    assert "| Evaluation Dimension |" in matrix_rep.markdown_table
