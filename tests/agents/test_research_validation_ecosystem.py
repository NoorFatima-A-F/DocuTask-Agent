"""
Comprehensive Unit & Integration Test Suite for the Research-Grade Validation Ecosystem (Phases 18–32).
Verifies:
- Phase 18: Independent Evaluation Layer & Metrics (CER, WER, F1)
- Phase 19: Enterprise Datasets, Dataset Cards & Synthetic Noise Models
- Phase 20: Human Evaluation & Inter-Rater Reliability (Cohen's Kappa, Fleiss' Kappa)
- Phase 21: Statistical Audit Framework & Hypothesis Testing
- Phase 22: Real Infrastructure Validation & Cloud Run/GKE Scenarios
- Phase 23: Continuous Benchmark Observatory & Regression Alerting
- Phase 24: Explainable Evidence 14-Dimension Provenance
- Phase 25: Threats to Validity 4-Pillar Matrix
- Phase 26: Research Reproducibility Package (ACM Guidelines)
- Phase 27: Continuous Evidence Lifecycle State Machine
- Phase 28: Scientific Benchmark Registry & Gatekeeper
- Phase 29: Confidence Calibration (ECE, MCE, Brier Score)
- Phase 30: Engineering Economics & Cloud Unit Cost Models
- Phase 31: Operational Readiness & Quantitative SRE Reliability (SLOs, RTO/RPO)
- Phase 32: Master Benchmark Self-Certification Engine
"""

import time
import pytest
from typing import Any, Dict, List

# Phase 18: Independent Evaluation & Metrics
from evaluation.metrics.evaluation_metrics import EvaluationMetrics, EvaluationMetricSummary
from evaluation.runner.independent_runner import (
    BlackBoxEvaluationResult,
    BlackBoxEvaluationTask,
    IndependentEvaluationRunner,
)

# Phase 19: Datasets & Noise
from evaluation.datasets.dataset_cards import DatasetCard
from evaluation.datasets.enterprise_datasets import EnterpriseDatasetCatalog
from evaluation.datasets.synthetic_noise import DegradationType, SyntheticNoiseEngine

# Phase 20: Human Evaluation
from evaluation.human_eval.inter_rater import (
    HumanEvaluationEngine,
    InterRaterReliabilityReport,
    ReviewerEvaluationScore,
)

# Phase 21: Statistical Audit
from app.evidence.benchmarking.statistical_audit import (
    AuditDecision,
    StatisticalAuditFramework,
    StatisticalAuditReport,
)

# Phase 22: Infrastructure Lab
from app.evidence.benchmarking.infrastructure_lab import (
    InfrastructureLabEngine,
    InfrastructureLabReport,
    InfrastructureTier,
)

# Phase 23: Continuous Observatory
from app.evidence.benchmarking.observatory import (
    ContinuousBenchmarkObservatory,
    HistoricalBenchmarkDataPoint,
    ObservatoryAnalysisReport,
    RegressionSeverity,
)

# Phase 24: Explainable Evidence
from app.evidence.traceability.explainable_evidence import (
    EvidenceExplanationCard,
    ExplainableEvidenceFramework,
)

# Phase 25: Threats to Validity
from app.evidence.benchmarking.threats_to_validity import (
    ThreatRiskLevel,
    ThreatsToValidityGenerator,
    ThreatsToValidityReport,
)

# Phase 26: Reproducibility Package
from app.evidence.reproducibility.research_package import (
    ResearchPackageManifest,
    ResearchReproducibilityPackageGenerator,
)

# Phase 27: Evidence Lifecycle
from app.evidence.governance.lifecycle import (
    EvidenceLifecycleManager,
    EvidenceLifecycleState,
    ManagedEvidenceMetadata,
)

# Phase 28: Benchmark Registry
from app.evidence.governance.benchmark_registry import (
    BenchmarkRegistrationSpec,
    ScientificBenchmarkRegistry,
)

# Phase 29: Confidence Calibration
from app.evidence.benchmarking.calibration import (
    CalibrationAnalysisReport,
    CalibrationStatus,
    ConfidenceCalibrationEngine,
)

# Phase 30: Engineering Economics
from app.evidence.benchmarking.economics import (
    EngineeringEconomicsEngine,
    UnitEconomicsReport,
)

# Phase 31: Operational Readiness
from app.evidence.benchmarking.operational_readiness import (
    OperationalMaturityTier,
    OperationalReadinessFramework,
    QuantitativeReadinessReport,
)

# Phase 32: Benchmark Certification
from app.evidence.benchmarking.certification import (
    BenchmarkCertificationEngine,
    BenchmarkCertificationReport,
    CertificationStatus,
)


class TestResearchValidationEcosystem:
    """Test suite covering all research-grade validation platform enhancements."""

    # -------------------------------------------------------------------------
    # Phase 18: Independent Evaluation Runner & Metrics
    # -------------------------------------------------------------------------
    def test_independent_evaluation_runner(self):
        tasks = [
            BlackBoxEvaluationTask(
                task_id="T1",
                domain="Finance",
                document_type="Invoice",
                input_payload={"raw": "INV-100 TOTAL: 50.00"},
                ground_truth_extracted={"inv_num": "INV-100", "total": "50.00"},
                difficulty_level="EASY",
            )
        ]

        def mock_blackbox_agent(payload: Dict[str, Any]) -> Dict[str, Any]:
            return {"inv_num": "INV-100", "total": "50.00"}

        result = IndependentEvaluationRunner.evaluate_endpoint("invoice_eval", tasks, mock_blackbox_agent)
        assert isinstance(result, BlackBoxEvaluationResult)
        assert result.total_tasks == 1
        assert result.metrics.exact_match_ratio == 1.0
        assert result.metrics.f1_score == 1.0
        assert result.metrics.mean_cer == 0.0

    def test_evaluation_metrics_cer_wer(self):
        cer = EvaluationMetrics.compute_cer("HELLO WORLD", "HELL0 W0RLD")
        assert 0.0 < cer < 0.25

        wer = EvaluationMetrics.compute_wer("the quick brown fox", "the fast brown fox")
        assert wer == pytest.approx(0.25)

    # -------------------------------------------------------------------------
    # Phase 19: Enterprise Datasets, Dataset Cards & Noise Injection
    # -------------------------------------------------------------------------
    def test_dataset_cards_and_enterprise_datasets(self):
        card = EnterpriseDatasetCatalog.get_dataset_card("Healthcare")
        assert isinstance(card, DatasetCard)
        assert card.domain == "Healthcare"
        assert card.annotation_protocol.inter_annotator_agreement_kappa > 0.90
        assert len(card.known_biases) > 0

        tasks = EnterpriseDatasetCatalog.get_evaluation_tasks("Healthcare")
        assert len(tasks) >= 2
        assert tasks[0].domain == "Healthcare"

    def test_synthetic_noise_engine(self):
        clean_text = "PATIENT: Johnathan Doe 1982-04-12 AETNA HEALTH $250.00"
        degraded = SyntheticNoiseEngine.degrade_document(
            clean_text,
            degradations=[DegradationType.OCR_CHARACTER_SUBSTITUTION, DegradationType.PARTIAL_PAGE_TRUNCATION],
            error_rate=0.20,
            random_seed=42,
        )

        assert degraded.original_text == clean_text
        assert len(degraded.applied_degradations) == 2
        assert degraded.degraded_text != clean_text

    # -------------------------------------------------------------------------
    # Phase 20: Human Evaluation & Inter-Rater Reliability
    # -------------------------------------------------------------------------
    def test_human_evaluation_inter_rater_reliability(self):
        evals = [
            ReviewerEvaluationScore("rev1", "sample1", 5, 5, False, 5, 5),
            ReviewerEvaluationScore("rev2", "sample1", 5, 5, False, 5, 5),
            ReviewerEvaluationScore("rev3", "sample1", 5, 5, False, 5, 5),
            ReviewerEvaluationScore("rev1", "sample2", 2, 2, True, 2, 2),
            ReviewerEvaluationScore("rev2", "sample2", 2, 2, True, 2, 2),
            ReviewerEvaluationScore("rev3", "sample2", 2, 2, True, 2, 2),
            ReviewerEvaluationScore("rev1", "sample3", 4, 4, False, 4, 4),
            ReviewerEvaluationScore("rev2", "sample3", 4, 4, False, 4, 4),
            ReviewerEvaluationScore("rev3", "sample3", 4, 4, False, 4, 4),
        ]

        report = HumanEvaluationEngine.evaluate_evaluations(evals)
        assert isinstance(report, InterRaterReliabilityReport)
        assert report.total_samples == 3
        assert report.total_reviewers == 3
        assert report.mean_cohens_kappa >= 0.80
        assert report.fleiss_kappa >= 0.80
        assert report.agreement_interpretation == "ALMOST_PERFECT"

    # -------------------------------------------------------------------------
    # Phase 21: Statistical Audit Framework
    # -------------------------------------------------------------------------
    def test_statistical_audit_framework(self):
        treatment = [12.0 + (i % 3) * 0.5 for i in range(25)]
        baseline = [15.0 + (i % 3) * 0.5 for i in range(25)]

        audit = StatisticalAuditFramework.audit_benchmark(
            benchmark_name="kernel_event_dispatch",
            treatment_samples=treatment,
            baseline_samples=baseline,
        )

        assert isinstance(audit, StatisticalAuditReport)
        assert audit.all_assumptions_met is True
        assert audit.decision == AuditDecision.REJECT_NULL_STATISTICALLY_SIGNIFICANT
        assert audit.statistical_power >= 0.80

    # -------------------------------------------------------------------------
    # Phase 22: Infrastructure Lab
    # -------------------------------------------------------------------------
    def test_infrastructure_lab(self):
        def sample_work():
            _ = [x ** 2 for x in range(100)]

        lab_rep = InfrastructureLabEngine.run_infrastructure_lab(sample_work)
        assert isinstance(lab_rep, InfrastructureLabReport)
        assert lab_rep.total_scenarios >= 3
        assert lab_rep.cold_start_overhead_ratio >= 1.0
        assert lab_rep.recommended_deployment_target == InfrastructureTier.GCP_CLOUD_RUN_SERVERLESS

    # -------------------------------------------------------------------------
    # Phase 23: Continuous Benchmark Observatory
    # -------------------------------------------------------------------------
    def test_continuous_benchmark_observatory(self):
        obs = ContinuousBenchmarkObservatory()
        # Record commit history
        obs.record_data_point("doc_pipeline", HistoricalBenchmarkDataPoint("c1", "sha1", 10.0, 12.0, 40.0, 0.98, 0.001))
        obs.record_data_point("doc_pipeline", HistoricalBenchmarkDataPoint("c2", "sha2", 10.2, 12.1, 40.5, 0.98, 0.001))
        obs.record_data_point("doc_pipeline", HistoricalBenchmarkDataPoint("c3", "sha3", 10.1, 12.0, 40.2, 0.99, 0.001))

        rep = obs.analyze_trends("doc_pipeline")
        assert isinstance(rep, ObservatoryAnalysisReport)
        assert rep.total_campaigns_analyzed == 3
        assert rep.has_critical_regression is False

        # Add regressed data point (+50% latency)
        obs.record_data_point("doc_pipeline", HistoricalBenchmarkDataPoint("c4", "sha4", 16.0, 20.0, 55.0, 0.85, 0.002))
        rep_regressed = obs.analyze_trends("doc_pipeline")
        assert rep_regressed.has_critical_regression is True
        assert len(rep_regressed.alerts) >= 1

    # -------------------------------------------------------------------------
    # Phase 24: Explainable Evidence Framework
    # -------------------------------------------------------------------------
    def test_explainable_evidence_framework(self):
        card = ExplainableEvidenceFramework.generate_explanation_card(
            evidence_id="EVI-PLAN-001",
            why_objective="Verify planner latency under complex DAG decomposition.",
            how_execution="Executed 50 iterations with TimerCalibrationEngine deduction.",
            statistical_method="Welch's t-test with BCa bootstrap (B=2000)",
        )

        assert isinstance(card, EvidenceExplanationCard)
        assert card.evidence_id == "EVI-PLAN-001"
        assert len(card.assumptions) >= 4
        assert len(card.to_dict()) == 16

    # -------------------------------------------------------------------------
    # Phase 25: Threats to Validity Generator
    # -------------------------------------------------------------------------
    def test_threats_to_validity_generator(self):
        threats_rep = ThreatsToValidityGenerator.generate_threats_matrix("autonomous_planner_benchmark")
        assert isinstance(threats_rep, ThreatsToValidityReport)
        assert len(threats_rep.threats) == 4
        assert threats_rep.highest_residual_risk == ThreatRiskLevel.LOW

    # -------------------------------------------------------------------------
    # Phase 26: Research Reproducibility Package
    # -------------------------------------------------------------------------
    def test_research_reproducibility_package(self):
        package = ResearchReproducibilityPackageGenerator.generate_reproducibility_package()
        assert isinstance(package, ResearchPackageManifest)
        assert package.package_id == "ACM-ARTIFACT-AAOS-2026-V1"
        assert len(package.included_files) >= 5
        assert len(package.bundle_hash) == 64

    # -------------------------------------------------------------------------
    # Phase 27: Evidence Lifecycle Governance
    # -------------------------------------------------------------------------
    def test_evidence_lifecycle_governance(self):
        mgr = EvidenceLifecycleManager()
        meta = mgr.register_draft("EVI-TEST-100", author="alice")
        assert meta.state == EvidenceLifecycleState.DRAFT

        # Transition to CANDIDATE
        mgr.transition_state("EVI-TEST-100", EvidenceLifecycleState.CANDIDATE, "alice", "Completed generation.")
        # Transition to VERIFIED
        verified = mgr.transition_state("EVI-TEST-100", EvidenceLifecycleState.VERIFIED, "taskmaster-judge", "Approved.")
        assert verified.state == EvidenceLifecycleState.VERIFIED
        assert verified.reviewer == "taskmaster-judge"
        assert len(verified.history) == 2

    # -------------------------------------------------------------------------
    # Phase 28: Scientific Benchmark Registry
    # -------------------------------------------------------------------------
    def test_scientific_benchmark_registry(self):
        reg = ScientificBenchmarkRegistry()
        spec = BenchmarkRegistrationSpec(
            benchmark_id="BM-PLANNER-01",
            purpose="Benchmark Autonomous Planner Latency",
            owner="architect@google.com",
            reviewers=["judge1@hackathon.ai"],
            scientific_rationale="Evaluates DAG generation latency.",
            acceptance_criteria="P95 <= 50ms, Error <= 5%",
            minimum_sample_size=30,
            minimum_statistical_power=0.80,
            required_confidence_level=0.95,
            required_reproducibility_tier="DETERMINISTIC",
            dataset_card_id="DATASET-LEGAL-001",
            hardware_requirements="4 cores, 8GB RAM",
            expiration_timestamp=time.time() + 86400 * 30,  # 30 days
            review_frequency_days=90,
        )
        reg.register(spec)

        # Validate eligible run
        is_ok, errs = reg.validate_execution_eligibility("BM-PLANNER-01", actual_sample_size=50, achieved_power=0.85)
        assert is_ok is True
        assert len(errs) == 0

        # Validate underpowered run
        is_ok2, errs2 = reg.validate_execution_eligibility("BM-PLANNER-01", actual_sample_size=10, achieved_power=0.60)
        assert is_ok2 is False
        assert len(errs2) >= 2

    # -------------------------------------------------------------------------
    # Phase 29: Confidence Calibration Engine
    # -------------------------------------------------------------------------
    def test_confidence_calibration_engine(self):
        # Well-calibrated synthetic predictions
        confidences = [0.9, 0.9, 0.8, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2]
        labels = [True, True, True, False, True, True, False, False, False, False]

        calib = ConfidenceCalibrationEngine.evaluate_calibration("planner_calibration", confidences, labels)
        assert isinstance(calib, CalibrationAnalysisReport)
        assert calib.total_samples == 10
        assert 0.0 <= calib.expected_calibration_error_ece <= 0.40
        assert 0.0 <= calib.brier_score <= 0.50
        assert len(calib.confidence_bins) == 10

    # -------------------------------------------------------------------------
    # Phase 30: Engineering Economics
    # -------------------------------------------------------------------------
    def test_engineering_economics_engine(self):
        econ = EngineeringEconomicsEngine.calculate_unit_economics(
            workflow_name="medical_claim_audit",
            avg_duration_sec=0.40,
            vcpu_allocated=2.0,
            ram_gb_allocated=4.0,
            input_tokens=2000,
            output_tokens=400,
        )

        assert isinstance(econ, UnitEconomicsReport)
        assert econ.cost_per_document_usd > 0.0
        assert econ.cost_per_document_usd < 0.01  # Sub-cent document processing
        assert econ.gross_margin_pct_at_25_cents > 95.0
        assert econ.breakdown.compute_cloud_run_usd > 0.0
        assert econ.breakdown.vertex_ai_llm_tokens_usd > 0.0

    # -------------------------------------------------------------------------
    # Phase 31: Operational Readiness Framework
    # -------------------------------------------------------------------------
    def test_operational_readiness_framework(self):
        readiness = OperationalReadinessFramework.evaluate_readiness(
            service_name="AAOS_Kernel",
            observed_success_rate=0.9998,
            p99_latency_ms=120.0,
        )

        assert isinstance(readiness, QuantitativeReadinessReport)
        assert readiness.maturity_tier == OperationalMaturityTier.TIER_3_PRODUCTION_ENTERPRISE
        assert readiness.is_production_certified is True
        assert len(readiness.slos) == 3
        assert readiness.disaster_recovery.tested_rto_seconds <= 30.0

    # -------------------------------------------------------------------------
    # Phase 32: Benchmark Certification Engine
    # -------------------------------------------------------------------------
    def test_benchmark_certification_engine(self):
        cert = BenchmarkCertificationEngine.certify_campaign(
            campaign_id="CAMP-2026-Q3-01",
            timer_calibrated=True,
            framework_self_validated=True,
            repeatability_passed=True,
            power_adequate=True,
            distribution_tested=True,
            bootstrap_converged=True,
            integrity_passed=True,
            provenance_verified=True,
        )

        assert isinstance(cert, BenchmarkCertificationReport)
        assert cert.status == CertificationStatus.CERTIFIED_RESEARCH_GRADE
        assert cert.criteria_passed_count == 10
        assert cert.total_criteria_count == 10
        assert cert.overall_certification_score == 100.0
