"""
Unit and Integration Tests for Phase 3H.6: Enterprise Service Level Objectives (SLO), SLI, Error Budget & Reliability Compliance
"""
import os
import json
import pytest

from app.platform_verification.service_reliability.domain.models import (
    ReliabilityTier,
    BurnRateSeverity,
    DeploymentGateDecision,
)
from app.platform_verification.service_reliability.verifiers import (
    SLOArchitectureVerifier,
    SLICollectorVerifier,
    AvailabilitySLOVerifier,
    LatencySLOVerifier,
    ErrorBudgetVerifier,
    BurnRateVerifier,
    ReliabilityComplianceVerifier,
    DeploymentGateVerifier,
    ExecutiveDashboardVerifier,
    HistoricalTrendVerifier,
    AIWorkloadReliabilityVerifier,
)
from app.platform_verification.service_reliability.scoring import ServiceReliabilityScorer
from app.platform_verification.service_reliability.exporter import ServiceReliabilityExporter
from app.platform_verification.service_reliability.runtime import ServiceReliabilityRuntime
from app.platform_verification.service_reliability.api.service_reliability_api import (
    get_reliability_status,
    run_reliability_verification,
    get_slo_architecture,
    get_deployment_gate_status,
)


class TestServiceReliabilityVerification:
    @pytest.fixture
    def test_output_dir(self, tmp_path):
        return str(tmp_path / "service_reliability_evidence")

    def test_01_slo_architecture_verifier(self):
        verifier = SLOArchitectureVerifier()
        report = verifier.verify_slo_architecture()

        assert report.total_slos_defined >= 8
        assert len(report.subsystems_covered) >= 8
        assert report.architecture_compliant is True

        for slo in report.active_slos:
            assert slo.target_pct > 90.0
            assert len(slo.sli_formula) > 0
            assert len(slo.owner) > 0

    def test_02_sli_collector_verifier(self):
        verifier = SLICollectorVerifier()
        report = verifier.collect_subsystem_slis()

        assert report.total_subsystems >= 7
        assert report.collection_active is True
        assert report.telemetry_pipeline_healthy is True

        for s in report.subsystems:
            assert s.current_sli_pct >= s.target_slo_pct
            assert s.meeting_slo is True

    def test_03_availability_slo_verifier(self):
        verifier = AvailabilitySLOVerifier()
        report = verifier.verify_availability_slo()

        assert report.measured_availability_pct >= 99.90
        assert report.slo_satisfied is True
        assert len(report.profiles) >= 4

        for profile in report.profiles:
            assert profile.availability_pct >= 99.90
            assert profile.slo_satisfied is True

    def test_04_latency_slo_verifier(self):
        verifier = LatencySLOVerifier()
        report = verifier.verify_latency_slos()

        assert report.total_endpoints_evaluated >= 6
        assert report.all_latency_slos_satisfied is True

        for benchmark in report.benchmarks:
            assert benchmark.p95_ms <= benchmark.target_p95_ms
            assert benchmark.latency_slo_satisfied is True

    def test_05_error_budget_verifier(self):
        verifier = ErrorBudgetVerifier()
        report = verifier.verify_error_budgets()

        assert report.overall_remaining_budget_pct >= 70.0
        assert report.error_budget_policy_healthy is True
        assert len(report.subsystem_budgets) >= 5

        for b in report.subsystem_budgets:
            assert b.remaining_budget_pct > 75.0
            assert b.is_budget_healthy is True

    def test_06_burn_rate_verifier(self):
        verifier = BurnRateVerifier()
        report = verifier.analyze_burn_rates()

        assert len(report.evaluated_windows) >= 4
        assert report.fast_burn_detected is False
        assert report.slow_burn_detected is False
        assert report.overall_burn_rate_status == BurnRateSeverity.SAFE

    def test_07_reliability_compliance_verifier(self):
        verifier = ReliabilityComplianceVerifier()
        report = verifier.verify_reliability_compliance()

        assert report.total_pillars >= 6
        assert report.compliant_pillars_count == report.total_pillars
        assert report.overall_compliance_pct == 100.0
        assert report.enterprise_standards_satisfied is True

    def test_08_deployment_gate_verifier(self):
        runtime = ServiceReliabilityRuntime()
        results = runtime.run_full_reliability_verification()
        gate = results["gate_report"]

        assert gate.decision == DeploymentGateDecision.APPROVED
        assert gate.deployment_allowed is True
        assert len(gate.criteria) >= 5
        assert all(c.passed for c in gate.criteria)

    def test_09_executive_dashboard_verifier(self):
        verifier = ExecutiveDashboardVerifier()
        report = verifier.generate_executive_dashboards()

        assert len(report.personas) == 5
        assert report.dashboard_telemetry_active is True

        persona_names = [p.persona for p in report.personas]
        assert "Operations" in persona_names
        assert "Engineering" in persona_names
        assert "Management" in persona_names
        assert "SRE" in persona_names
        assert "AI_Operations" in persona_names

    def test_10_historical_trend_verifier(self):
        verifier = HistoricalTrendVerifier()
        report = verifier.analyze_historical_trends()

        assert len(report.periods) == 4
        assert report.regression_detected is False
        assert report.stability_trend == "STABLE_AND_IMPROVING"

    def test_11_ai_workload_reliability_verifier(self):
        verifier = AIWorkloadReliabilityVerifier()
        report = verifier.verify_ai_workload_reliability()

        assert report.total_workloads_verified >= 5
        assert report.all_ai_workloads_reliable is True

        for workload in report.workload_metrics:
            assert workload.accuracy_or_success_rate_pct >= 98.0
            assert workload.reliable is True

    def test_12_service_reliability_scorer(self):
        runtime = ServiceReliabilityRuntime()
        results = runtime.run_full_reliability_verification()
        scorecard = results["scorecard"]

        assert scorecard.overall_reliability_score >= 98.0
        assert scorecard.certification_tier == ReliabilityTier.ENTERPRISE_SRE_CERTIFIED
        assert scorecard.passed is True
        assert scorecard.overall_availability_pct >= 99.90
        assert len(scorecard.pillar_scores) == 7

    def test_13_service_reliability_exporter(self, test_output_dir):
        runtime = ServiceReliabilityRuntime(output_dir=test_output_dir)
        results = runtime.run_full_reliability_verification()

        assert os.path.exists(test_output_dir)
        assert len(results["exported_files"]) == 13

        metadata_path = os.path.join(test_output_dir, "metadata.json")
        assert os.path.exists(metadata_path)

        with open(metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        assert meta["overall_score"] >= 98.0
        assert meta["certification_tier"] == "Enterprise SRE Certified"
        assert meta["passed"] is True
        assert "file_manifest" in meta
        assert "slo_architecture_report.json" in meta["file_manifest"]
        assert "ai_reliability_report.json" in meta["file_manifest"]

    def test_14_service_reliability_api(self):
        status = get_reliability_status()
        assert status["status"] == "ACTIVE"
        assert status["phase"] == "3H.6"

        verify = run_reliability_verification()
        assert verify["overall_reliability_score"] >= 98.0
        assert verify["certification_tier"] == "Enterprise SRE Certified"
        assert verify["passed"] is True
        assert verify["deployment_decision"] == "APPROVED"

        slo_data = get_slo_architecture()
        assert slo_data["total_slos_defined"] >= 8

        gate_data = get_deployment_gate_status()
        assert gate_data["decision"] == "APPROVED"
        assert gate_data["deployment_allowed"] is True
