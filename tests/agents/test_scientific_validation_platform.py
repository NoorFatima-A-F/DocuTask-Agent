"""
Comprehensive Unit & Integration Test Suite for the Scientific Validation Platform (SVP).
Tests all 17 research-grade phases:
1. DistributionValidationEngine
2. BootstrapValidationEngine
3. TimerValidationLab
4. EnvironmentManifestGenerator
5. EvidenceSigningEngine
6. SteadyStateValidationEngine
7. QueueingTheoryValidationEngine
8. BenchmarkWorkloadLibrary
9. StatisticalPowerEngine
10. BenchmarkVisualizationPlatform
11. GarbageCollectionValidationEngine
12. RepeatabilityFramework
13. CrossPlatformValidationEngine
14. BenchmarkIntegrityEngine
15. EvidenceSchemaVersioning
16. FrameworkValidationSuite
17. BenchmarkGovernanceEngine
"""

import random

from app.evidence.benchmarking.distribution_validation import (
    CandidateDistribution,
    DistributionValidationEngine,
    TestDecision,
)
from app.evidence.benchmarking.bootstrap_engine import (
    BootstrapConvergenceStatus,
    BootstrapType,
    BootstrapValidationEngine,
    BootstrapValidationResult,
)
from app.evidence.benchmarking.timer_lab import (
    TimerValidationLab,
    TimerValidationLabReport,
    WorkloadType,
)
from app.evidence.benchmarking.environment_manifest import (
    EnvironmentManifest,
    EnvironmentManifestGenerator,
)
from app.evidence.benchmarking.evidence_signer import (
    DSSEEnvelope,
    EvidenceSigningEngine,
    VerificationCertificate,
)
from app.evidence.benchmarking.steady_state_validator import (
    ConvergenceState,
    SteadyStateValidationEngine,
)
from app.evidence.benchmarking.queueing_theory import (
    QueueingTheoryValidationEngine,
    QueueValidationStatus,
)
from app.evidence.benchmarking.workload_library import (
    BenchmarkWorkloadLibrary,
    WorkloadSpecification,
)
from app.evidence.benchmarking.power_analysis import (
    PowerAdequacyStatus,
    StatisticalPowerEngine,
)
from app.evidence.benchmarking.visualization import (
    BenchmarkVisualizationPlatform,
)
from app.evidence.benchmarking.gc_validation import (
    GarbageCollectionValidationEngine,
    GCValidationReport,
    RecommendedGCMode,
)
from app.evidence.benchmarking.repeatability import (
    RepeatabilityFramework,
    RepeatabilityReport,
    RepeatabilityStatus,
)
from app.evidence.benchmarking.cross_platform import (
    CrossPlatformReport,
    CrossPlatformValidationEngine,
    PlatformEnvironment,
    PortabilityVerdict,
)
from app.evidence.benchmarking.integrity_engine import (
    BenchmarkIntegrityAuditReport,
    BenchmarkIntegrityEngine,
    IntegrityCheckStatus,
)
from app.evidence.benchmarking.schema_versioning import (
    EvidenceSchemaVersioning,
    SchemaType,
)
from app.evidence.benchmarking.framework_validation import (
    FrameworkSelfValidationReport,
    FrameworkValidationSuite,
)
from app.evidence.benchmarking.governance import (
    BenchmarkGovernanceEngine,
    BenchmarkReviewStatus,
    ScientificChecklist,
)


class TestScientificValidationPlatform:
    """Consolidated test suite verifying the complete Scientific Validation Platform."""

    # -------------------------------------------------------------------------
    # Phase 1: Distribution Validation
    # -------------------------------------------------------------------------
    def test_distribution_validation_normal(self):
        rng = random.Random(42)
        normal_samples = [rng.gauss(100.0, 5.0) for _ in range(50)]
        results = DistributionValidationEngine.evaluate_all(normal_samples)

        assert CandidateDistribution.NORMAL in results
        norm_rep = results[CandidateDistribution.NORMAL]
        assert len(norm_rep.tests) == 3
        assert norm_rep.overall_decision == TestDecision.ACCEPT

        best_fit = DistributionValidationEngine.find_best_fit(normal_samples)
        assert best_fit.candidate in (CandidateDistribution.NORMAL, CandidateDistribution.UNIFORM)

    def test_distribution_validation_bimodal(self):
        rng = random.Random(42)
        # Bimodal mixture: 50% at 20.0, 50% at 100.0
        bimodal_samples = [rng.gauss(20.0, 2.0) for _ in range(30)] + [rng.gauss(100.0, 2.0) for _ in range(30)]
        bimodal_rep = DistributionValidationEngine.test_bimodal(bimodal_samples)

        assert bimodal_rep.overall_decision == TestDecision.ACCEPT
        assert bimodal_rep.overall_confidence > 0.60

    # -------------------------------------------------------------------------
    # Phase 2: Bootstrap Validation
    # -------------------------------------------------------------------------
    def test_bootstrap_bca_and_convergence(self):
        samples = [10.0, 10.5, 9.8, 10.2, 10.1, 9.9, 10.4, 10.3, 10.0, 9.7]
        result = BootstrapValidationEngine.run_bootstrap(
            samples=samples,
            bootstrap_type=BootstrapType.BCA,
            resamples=500,
            confidence_level=0.95,
            random_seed=42,
        )

        assert isinstance(result, BootstrapValidationResult)
        assert result.bootstrap_type == BootstrapType.BCA
        assert result.lower_bound <= result.point_estimate <= result.upper_bound
        assert len(result.reproducibility_hash) == 64
        assert len(result.convergence_curve) >= 4
        assert result.convergence_status in (BootstrapConvergenceStatus.CONVERGED, BootstrapConvergenceStatus.INCONCLUSIVE)

    def test_bootstrap_percentile_and_basic(self):
        samples = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        res_perc = BootstrapValidationEngine.run_bootstrap(samples, bootstrap_type=BootstrapType.PERCENTILE, resamples=200)
        res_basic = BootstrapValidationEngine.run_bootstrap(samples, bootstrap_type=BootstrapType.BASIC, resamples=200)
        res_stud = BootstrapValidationEngine.run_bootstrap(samples, bootstrap_type=BootstrapType.STUDENTIZED, resamples=200)

        assert res_perc.lower_bound <= res_perc.upper_bound
        assert res_basic.lower_bound <= res_basic.upper_bound
        assert res_stud.lower_bound <= res_stud.upper_bound

    # -------------------------------------------------------------------------
    # Phase 3: Timer Validation Laboratory
    # -------------------------------------------------------------------------
    def test_timer_validation_lab(self):
        lab_report = TimerValidationLab.run_full_laboratory(iterations_per_workload=15)

        assert isinstance(lab_report, TimerValidationLabReport)
        assert len(lab_report.evaluations) == 24  # 8 workloads * 3 clocks
        assert len(lab_report.recommended_timer_by_workload) == 8
        # Ensure sleep / network I/O rejects process_time_ns
        sleep_rejections = lab_report.rejected_timer_by_workload.get(WorkloadType.SLEEP.value, [])
        assert any("process_time_ns" in r for r in sleep_rejections)

    # -------------------------------------------------------------------------
    # Phase 4: Environment Manifest Generator
    # -------------------------------------------------------------------------
    def test_environment_manifest_generator(self):
        manifest = EnvironmentManifestGenerator.generate_manifest()

        assert isinstance(manifest, EnvironmentManifest)
        assert manifest.logical_cores >= 1
        assert manifest.ram_total_gb > 0.0
        assert len(manifest.manifest_hash) == 64
        assert len(manifest.dependencies) >= 0

        m_dict = manifest.to_dict()
        assert "manifest_hash" in m_dict
        assert "system" in m_dict
        assert "provenance" in m_dict

    # -------------------------------------------------------------------------
    # Phase 5: Evidence Signing Engine
    # -------------------------------------------------------------------------
    def test_evidence_signing_and_verification(self):
        payload = {"benchmark": "autonomous_planner", "mean_ms": 12.4, "p95_ms": 15.1}
        envelope = EvidenceSigningEngine.sign_evidence_item(
            evidence_id="EVI-PLANNER-001",
            evidence_payload=payload,
            workflow_id="wf_ci_test",
            git_sha="c0ffee123456",
        )

        assert isinstance(envelope, DSSEEnvelope)
        assert len(envelope.signatures) == 1
        assert envelope.signatures[0].algorithm == "HMAC-SHA256"

        cert = EvidenceSigningEngine.verify_envelope(envelope)
        assert isinstance(cert, VerificationCertificate)
        assert cert.signature_valid is True
        assert cert.evidence_id == "EVI-PLANNER-001"
        assert cert.slsa_level_achieved == "SLSA_BUILD_LEVEL_3"
        assert len(cert.certificate_digest) == 64

    # -------------------------------------------------------------------------
    # Phase 6: Steady-State Validation Engine
    # -------------------------------------------------------------------------
    def test_steady_state_validation(self):
        # 1. Converged steady-state samples (low CV)
        steady_samples = [100.0 + (i % 3) * 0.5 for i in range(60)]
        rep_steady = SteadyStateValidationEngine.validate_convergence(steady_samples, window_size=10, max_cv=0.12)
        assert rep_steady.state == ConvergenceState.CONVERGED_STEADY_STATE
        assert rep_steady.stability_confidence > 0.0

        # 2. Non-convergent drifting samples
        drift_samples = [10.0 + i * 10.0 for i in range(60)]
        rep_drift = SteadyStateValidationEngine.validate_convergence(drift_samples, window_size=10, max_cv=0.12)
        assert rep_drift.state == ConvergenceState.INVALID_NON_CONVERGENT

    # -------------------------------------------------------------------------
    # Phase 7: Queueing Theory Validation
    # -------------------------------------------------------------------------
    def test_queueing_theory_validation(self):
        # Stable arrival rates around 100 ops/sec, queue depth stable around 5
        arr_rates = [100.0, 99.0, 101.0, 100.5, 99.5, 100.2]
        q_depths = [5, 5, 6, 5, 5, 6]
        mean_lat_ms = 50.0  # 0.05s -> L = 100 * 0.05 = 5.0

        rep = QueueingTheoryValidationEngine.validate_system(
            concurrency=5,
            arrival_rates_windowed=arr_rates,
            queue_depths_windowed=q_depths,
            mean_latency_ms=mean_lat_ms,
        )

        assert rep.status == QueueValidationStatus.VALIDATED
        assert rep.assumptions_satisfied is True
        assert rep.relative_error_pct <= 5.0

    def test_queueing_theory_not_applicable_on_drift(self):
        # Exploding queue (growing slope)
        arr_rates = [10.0, 20.0, 40.0, 80.0, 160.0]
        q_depths = [5, 50, 150, 400, 1000]

        rep = QueueingTheoryValidationEngine.validate_system(
            concurrency=10,
            arrival_rates_windowed=arr_rates,
            queue_depths_windowed=q_depths,
            mean_latency_ms=100.0,
        )

        assert rep.status == QueueValidationStatus.NOT_APPLICABLE
        assert rep.assumptions_satisfied is False

    # -------------------------------------------------------------------------
    # Phase 8: Benchmark Workload Library
    # -------------------------------------------------------------------------
    def test_workload_library_catalog(self):
        workloads = BenchmarkWorkloadLibrary.get_all_workloads()
        assert len(workloads) == 12

        # Verify all workloads are executable and return expected data
        for cat, spec in workloads.items():
            assert isinstance(spec, WorkloadSpecification)
            assert spec.category == cat
            assert spec.algorithmic_complexity in ("O(1)", "O(N)", "O(N log N)", "O(N^2)")
            res = spec.target_function()
            assert res is not None

    # -------------------------------------------------------------------------
    # Phase 9: Statistical Power Analysis
    # -------------------------------------------------------------------------
    def test_statistical_power_analysis(self):
        n_req = StatisticalPowerEngine.estimate_required_sample_size(effect_size_d=0.5, alpha=0.05, desired_power=0.80)
        assert n_req >= 30

        # Sample size 50 with clear effect -> ADEQUATE
        treatment = [15.0 + (i % 3) for i in range(50)]
        baseline = [10.0 + (i % 3) for i in range(50)]
        rep = StatisticalPowerEngine.analyze_power(treatment, baseline, desired_power=0.80)

        assert rep.adequacy_status == PowerAdequacyStatus.ADEQUATE
        assert rep.achieved_power >= 0.80
        assert rep.is_underpowered is False

    # -------------------------------------------------------------------------
    # Phase 10: Benchmark Visualization Platform
    # -------------------------------------------------------------------------
    def test_visualization_platform(self):
        samples = [10.0, 12.0, 15.0, 11.0, 13.0, 14.0, 10.5, 12.5]
        svg_hist = BenchmarkVisualizationPlatform.generate_histogram_svg(samples)
        assert "<svg" in svg_hist and "</svg>" in svg_hist
        assert "Latency Distribution Histogram" in svg_hist

        svg_ecdf = BenchmarkVisualizationPlatform.generate_ecdf_svg(samples)
        assert "<svg" in svg_ecdf and "</svg>" in svg_ecdf

        curve_pts = [(1, 100.0, 10.0), (10, 800.0, 12.0), (50, 2000.0, 25.0)]
        svg_curve = BenchmarkVisualizationPlatform.generate_saturation_curve_svg(curve_pts)
        assert "<svg" in svg_curve and "</svg>" in svg_curve

    # -------------------------------------------------------------------------
    # Phase 11: Garbage Collection Validation
    # -------------------------------------------------------------------------
    def test_gc_validation_engine(self):
        def alloc_heavy():
            _ = [f"obj_{i}" for i in range(100)]

        rep = GarbageCollectionValidationEngine.evaluate_workload("alloc_micro", alloc_heavy, iterations=50)
        assert isinstance(rep, GCValidationReport)
        assert rep.recommended_mode in (RecommendedGCMode.GC_DISABLED_DETERMINISTIC, RecommendedGCMode.GC_ENABLED_REALISTIC_PRODUCTION)

    # -------------------------------------------------------------------------
    # Phase 12: Repeatability Framework
    # -------------------------------------------------------------------------
    def test_repeatability_framework(self):
        def work():
            _ = sum(i ** 2 for i in range(500))

        rep = RepeatabilityFramework.execute_campaign("math_loop", work, total_runs=3, iterations_per_run=25, pause_between_runs_ms=5.0)
        assert isinstance(rep, RepeatabilityReport)
        assert rep.total_runs == 3
        assert 0.0 <= rep.repeatability_coefficient <= 1.0
        assert rep.status in (RepeatabilityStatus.HIGHLY_REPRODUCIBLE, RepeatabilityStatus.MODERATE_DRIFT)

    # -------------------------------------------------------------------------
    # Phase 13: Cross-Platform Validation
    # -------------------------------------------------------------------------
    def test_cross_platform_validation(self):
        platform_data = {
            PlatformEnvironment.LINUX_POSIX: [10.0, 10.2, 9.8],
            PlatformEnvironment.WINDOWS_DESKTOP: [11.5, 11.8, 11.2],
            PlatformEnvironment.GCP_CLOUD_RUN: [12.0, 12.5, 11.9],
        }
        rep = CrossPlatformValidationEngine.compare_platforms("cross_bench", platform_data)
        assert isinstance(rep, CrossPlatformReport)
        assert rep.verdict in (PortabilityVerdict.PORTABLE_CONSISTENT, PortabilityVerdict.PORTABLE_SCALED)
        assert rep.max_divergence_ratio >= 1.0

    # -------------------------------------------------------------------------
    # Phase 14: Benchmark Integrity Engine
    # -------------------------------------------------------------------------
    def test_integrity_engine_audits(self):
        preflight = BenchmarkIntegrityEngine.run_preflight_audit("audit_test")
        assert isinstance(preflight, BenchmarkIntegrityAuditReport)
        assert preflight.overall_status in (IntegrityCheckStatus.PASSED, IntegrityCheckStatus.WARNING)
        assert preflight.is_valid_for_evidence is True

        in_flight = BenchmarkIntegrityEngine.validate_in_flight_samples("in_flight_test", [100.0, 101.0, 99.0, 100.5])
        assert in_flight.overall_status == IntegrityCheckStatus.PASSED
        assert in_flight.is_valid_for_evidence is True

    # -------------------------------------------------------------------------
    # Phase 15: Evidence Schema Versioning
    # -------------------------------------------------------------------------
    def test_schema_versioning_and_migration(self):
        valid_v2_payload = {
            "evidence_id": "EVI-001",
            "title": "Title",
            "evidence_type": "BENCHMARK",
            "source": "kernel",
            "item_hash": "a" * 64,
            "reproducibility": "DETERMINISTIC",
        }
        is_valid, errors = EvidenceSchemaVersioning.validate_payload(SchemaType.EVIDENCE_ITEM, "2.0.0", valid_v2_payload)
        assert is_valid is True
        assert len(errors) == 0

        # Migration test
        v1_payload = {"evidence_id": "EVI-OLD", "title": "Old", "evidence_type": "UNIT_TEST", "source": "pytest"}
        migrated = EvidenceSchemaVersioning.migrate_v1_to_v2_evidence_item(v1_payload)
        assert migrated["reproducibility"] == "DETERMINISTIC"
        assert migrated["schema_version"] == "2.0.0"

    # -------------------------------------------------------------------------
    # Phase 16: Framework Self-Validation ("Verification of the Verification")
    # -------------------------------------------------------------------------
    def test_framework_self_validation(self):
        self_val = FrameworkValidationSuite.run_self_validation()
        assert isinstance(self_val, FrameworkSelfValidationReport)
        assert self_val.total_algorithms_tested == 4
        assert self_val.algorithms_passed >= 3
        assert self_val.overall_confidence > 0.70

    # -------------------------------------------------------------------------
    # Phase 17: Benchmark Governance Platform
    # -------------------------------------------------------------------------
    def test_benchmark_governance(self):
        gov = BenchmarkGovernanceEngine()
        rec = gov.register_benchmark("autonomous_planner_benchmark")
        assert rec.review_status == BenchmarkReviewStatus.PENDING_REVIEW

        # Complete valid checklist
        checklist = ScientificChecklist(
            has_formal_distribution_hypothesis_test=True,
            has_statistical_power_analysis=True,
            is_power_adequate=True,
            has_environment_manifest_bound=True,
            has_cryptographic_signature=True,
            has_steady_state_validation=True,
            has_multi_run_repeatability_audit=True,
        )

        evaluated = gov.audit_and_evaluate("autonomous_planner_benchmark", checklist)
        assert evaluated.review_status == BenchmarkReviewStatus.APPROVED_CERTIFIED
        assert evaluated.quality_score == 100.0
        assert "taskmaster-judge@hackathon.ai" in evaluated.approved_by
