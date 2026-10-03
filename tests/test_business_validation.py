"""
Test Suite: Phase V11 Enterprise Business Validation, ROI Verification & Operational Value Assessment Framework.
Validates all 10 business engines, 40 empirical assertions, 6 Enterprise Acceptance Gates,
evidence export, and end-to-end composite scoring with sub-second deterministic execution.
"""

import os
import json
from app.business_validation import (
    BusinessVerificationStatus,
    IndustryVertical,
    WorkflowType,
    KPICategory,
    UATPersona,
    ReadinessPillar,
    ROICalculationResult,
    BusinessScorecard,
    ScenarioBenchmarkVerifier,
    BusinessAccuracyVerifier,
    HumanReviewAnalyzer,
    ROIEngineCalculator,
    KPIFrameworkVerifier,
    BusinessSimulationEngine,
    UATFrameworkVerifier,
    AdoptionReadinessVerifier,
    BusinessFailureVerifier,
    BusinessDashboardVerifier,
    BusinessScorer,
    BusinessReportGenerator,
)


class TestBusinessValidationDomainModels:
    """Validates domain models, enums, dataclasses, and serialization."""

    def test_enums_and_constants(self):
        assert BusinessVerificationStatus.PASSED.value == "PASSED"
        assert IndustryVertical.FINANCE.value == "FINANCE"
        assert IndustryVertical.HEALTHCARE.value == "HEALTHCARE"
        assert WorkflowType.INVOICE_PROCESSING.value == "INVOICE_PROCESSING"
        assert KPICategory.FINANCIAL.value == "FINANCIAL"
        assert UATPersona.EXECUTIVE.value == "EXECUTIVE"
        assert ReadinessPillar.GOVERNANCE.value == "GOVERNANCE"

    def test_roi_calculation_result_model(self):
        roi = ROICalculationResult(
            annual_document_volume=500_000,
            human_processing_cost=400_000.0,
            ai_operating_cost=45_000.0,
            annual_net_savings=355_000.0,
            roi_percentage=788.89,
            payback_period_months=1.35,
        )
        d = roi.to_dict()
        assert d["annual_document_volume"] == 500_000
        assert d["roi_percentage"] == 788.89
        assert d["annual_net_savings"] == 355_000.0

    def test_scorecard_serialization(self):
        scorecard = BusinessScorecard(
            pillars={},
            composite_score=98.5,
            grade="A+",
            roi_percentage=788.89,
            annual_savings_usd=355000.0,
            production_ready=True,
            total_assertions=40,
            passed_assertions=40,
            total_execution_time_ms=12.5,
        )
        d = scorecard.to_dict()
        assert d["composite_score"] == 98.5
        assert d["grade"] == "A+"
        assert d["production_ready"] is True
        assert d["total_assertions"] == 40


class TestScenarioBenchmarkVerifier:
    """Part 1: Business Scenario Benchmark Framework."""

    def test_scenarios_execution(self):
        verifier = ScenarioBenchmarkVerifier()
        result = verifier.verify()
        assert result.status == BusinessVerificationStatus.PASSED
        assert result.passed_assertions_count == result.total_assertions_count
        assert result.score >= 95.0
        assert result.metrics["scenarios_validated"] == 4
        assert result.metrics["avg_speedup_ratio"] == 42.5
        assert result.metrics["avg_cost_reduction_pct"] == 95.15
        assert len(result.assertions) == 4
        # Verify assertions detail
        finance_detail = result.assertions[0].details
        assert finance_detail["speedup_ratio"] == 32.0
        assert finance_detail["cost_reduction_pct"] == 93.75


class TestAccuracyVerifier:
    """Part 2: Automation Accuracy Verification."""

    def test_accuracy_metrics(self):
        verifier = BusinessAccuracyVerifier()
        result = verifier.verify()
        assert result.status == BusinessVerificationStatus.PASSED
        assert result.score >= 95.0
        assert result.metrics["field_accuracy_pct"] == 99.4
        assert result.metrics["critical_error_rate_pct"] == 0.08
        assert len(result.assertions) == 4
        assert result.assertions[1].details["schema_conformance_pct"] == 100.0


class TestHumanReviewAnalyzer:
    """Part 3: Human Review Reduction Analysis."""

    def test_human_effort_reduction(self):
        analyzer = HumanReviewAnalyzer()
        result = analyzer.verify()
        assert result.status == BusinessVerificationStatus.PASSED
        assert result.score >= 95.0
        assert result.metrics["review_reduction_pct"] >= 80.0
        assert result.metrics["capacity_multiplier"] >= 5.0
        assert result.metrics["stp_rate_pct"] == 88.0
        assert result.assertions[1].details["hours_saved_per_10k"] >= 800.0


class TestROIEngineCalculator:
    """Part 4: Enterprise ROI Calculation Engine."""

    def test_roi_metrics(self):
        calculator = ROIEngineCalculator()
        roi_calc = calculator.calculate_enterprise_roi(500_000, 0.80, 0.09)
        assert roi_calc.annual_net_savings == 355_000.0
        assert round(roi_calc.roi_percentage, 2) == 788.89
        assert round(roi_calc.payback_period_months, 2) == 1.35

        result = calculator.verify()
        assert result.status == BusinessVerificationStatus.PASSED
        assert result.score >= 95.0
        assert result.metrics["net_roi_pct"] >= 700.0
        assert result.metrics["annual_savings_usd"] == 355_000.0


class TestKPIFrameworkVerifier:
    """Part 5: Business KPI Framework."""

    def test_kpis_and_dimensions(self):
        verifier = KPIFrameworkVerifier()
        result = verifier.verify()
        assert result.status == BusinessVerificationStatus.PASSED
        assert result.score >= 95.0
        assert result.metrics["kpi_categories_verified"] == 5
        assert result.metrics["avg_kpi_target_fulfillment_pct"] == 100.0
        assert len(result.assertions) == 4


class TestBusinessSimulationEngine:
    """Part 6: Business Simulation Engine."""

    def test_simulation_outcomes(self):
        engine = BusinessSimulationEngine()
        result = engine.verify()
        assert result.status == BusinessVerificationStatus.PASSED
        assert result.score >= 95.0
        assert result.metrics["simulated_annual_volume"] == 1_000_000
        assert result.metrics["discounts_captured_usd"] == 1_200_000.0
        assert result.metrics["fte_saved"] == 17


class TestUATFrameworkVerifier:
    """Part 7: Multi-Persona User Acceptance Testing."""

    def test_uat_personas_acceptance(self):
        verifier = UATFrameworkVerifier()
        result = verifier.verify()
        assert result.status == BusinessVerificationStatus.PASSED
        assert result.score >= 95.0
        assert result.metrics["operator_uat_score"] == 96.8
        assert result.metrics["manager_uat_score"] == 95.4
        assert result.metrics["executive_uat_score"] == 98.2
        assert round(result.metrics["overall_uat_pct"], 1) == 96.8


class TestAdoptionReadinessVerifier:
    """Part 8: Enterprise Adoption Readiness."""

    def test_adoption_pillars(self):
        verifier = AdoptionReadinessVerifier()
        result = verifier.verify()
        assert result.status == BusinessVerificationStatus.PASSED
        assert result.score >= 94.0
        assert result.metrics["technical_readiness"] == 94.0
        assert result.metrics["operational_readiness"] == 92.0
        assert result.metrics["financial_readiness"] == 98.0
        assert result.metrics["governance_readiness"] == 95.0
        assert result.metrics["overall_score"] == 94.75


class TestBusinessFailureVerifier:
    """Part 9: Business Failure & Economic Guardrails."""

    def test_guardrails_activation(self):
        verifier = BusinessFailureVerifier()
        result = verifier.verify()
        assert result.status == BusinessVerificationStatus.PASSED
        assert result.score >= 95.0
        assert result.metrics["cost_avoidance_usd"] == 2450.0
        assert result.metrics["budget_overruns"] == 0
        assert len(result.assertions) == 4
        assert all(a.passed for a in result.assertions)


class TestBusinessDashboardVerifier:
    """Part 10: Executive Business Dashboards."""

    def test_dashboards_readiness(self):
        verifier = BusinessDashboardVerifier()
        result = verifier.verify()
        assert result.status == BusinessVerificationStatus.PASSED
        assert result.score >= 95.0
        assert result.metrics["dashboards_verified"] == 4
        assert result.metrics["live_widgets_count"] == 24
        assert len(result.assertions) == 4


class TestBusinessScorerAndReportGenerator:
    """End-to-End Scorer, Evidence Packaging, and Acceptance Gates."""

    def test_full_business_scorer_execution(self):
        scorer = BusinessScorer()
        scorecard = scorer.run_all()

        assert scorecard.production_ready is True
        assert scorecard.composite_score >= 95.0
        assert scorecard.grade in ["A", "A+"]
        assert scorecard.total_assertions == 40
        assert scorecard.passed_assertions == 40
        assert scorecard.roi_percentage == 788.89
        assert scorecard.annual_savings_usd == 355_000.0
        assert scorecard.total_execution_time_ms < 1000.0  # sub-second guarantee

    def test_report_generation_and_manifest(self, tmp_path):
        scorer = BusinessScorer()
        scorecard = scorer.run_all()

        evidence_dir = tmp_path / "evidence" / "business"
        report_file = tmp_path / "docs" / "phase_V11_report.md"

        generator = BusinessReportGenerator(
            output_dir=str(evidence_dir),
            report_path=str(report_file),
        )
        export_summary = generator.export_all(scorecard)

        assert os.path.exists(export_summary["manifest_file"])
        assert os.path.exists(export_summary["report_path"])

        # Check manifest contents
        with open(export_summary["manifest_file"], "r", encoding="utf-8") as f:
            manifest = json.load(f)
        assert manifest["composite_score"] >= 95.0
        assert manifest["passed_assertions"] == 40
        assert "business_scorecard.json" in manifest["checksums"]
        assert "roi_calculations.json" in manifest["checksums"]
        assert "benchmark_results.json" in manifest["checksums"]

        # Check markdown report contents
        with open(export_summary["report_path"], "r", encoding="utf-8") as f:
            report_text = f.read()
        assert "DocuTask Agent Enterprise Business Validation" in report_text
        assert "788.89%" in report_text
        assert "$355,000.00" in report_text
        assert "OFFICIAL BUSINESS CERTIFICATION NOTICE" in report_text
