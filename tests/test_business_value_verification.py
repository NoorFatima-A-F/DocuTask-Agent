"""
Comprehensive Unit and Integration Test Suite for Phase V11 — Enterprise Business Value, ROI Intelligence & Operational Impact Verification Program (EBV-OIVP).
"""

import os
import pytest
from app.business_value_verification.domain.models import (
    IndustryVertical,
)
from app.business_value_verification.metrics.automation_metrics import AutomationMetricsCalculator
from app.business_value_verification.metrics.productivity_analyzer import ProductivityAnalyzer
from app.business_value_verification.metrics.accuracy_comparator import AccuracyComparator
from app.business_value_verification.roi.roi_engine import ROIAnalyzer
from app.business_value_verification.roi.tco_analyzer import TCOAnalyzer
from app.business_value_verification.workflows.baseline_workflows import WorkflowModelFactory
from app.business_value_verification.workflows.process_optimizer import ProcessOptimizer
from app.business_value_verification.simulation.enterprise_simulator import EnterpriseSimulator
from app.business_value_verification.simulation.adoption_simulator import AdoptionSimulator
from app.business_value_verification.case_studies.case_study_generator import CaseStudyGenerator
from app.business_value_verification.reporting.business_value_scorer import BusinessValueScorer
from app.business_value_verification.reporting.evidence_generator import BusinessValueEvidenceGenerator


class TestBusinessMetricsAndProductivity:
    """Test suite for automation rates, productivity gains, and accuracy improvements."""

    def test_automation_metrics_calculator(self):
        metrics = AutomationMetricsCalculator.calculate_metrics(100, 88, 12, 91.5, 8.5)
        assert metrics.automation_rate_pct == 88.0
        assert metrics.straight_through_processing_pct == 91.5
        assert metrics.exception_routing_pct == 8.5
        assert metrics.fully_automated_tasks == 88

    def test_automation_metrics_zero_tasks(self):
        metrics = AutomationMetricsCalculator.calculate_metrics(0, 0, 0, 0.0, 0.0)
        assert metrics.automation_rate_pct == 0.0

    def test_productivity_analyzer(self):
        prod = ProductivityAnalyzer.calculate_productivity(
            annual_doc_volume=125000,
            baseline_mins_per_doc=18.0,
            ai_mins_per_doc=0.5,
        )
        assert prod.baseline_human_hours_annual == 37500.0
        assert prod.ai_human_hours_annual == pytest.approx(1041.67, abs=1.0)
        assert prod.hours_liberated_annual > 36000.0
        assert prod.fte_capacity_liberated > 18.0
        assert prod.throughput_expansion_multiplier == 36.0

    def test_accuracy_comparator(self):
        acc = AccuracyComparator.compare_accuracy(8.0, 0.5, 12.0, 99.0)
        assert acc.human_field_error_rate_pct == 8.0
        assert acc.ai_field_error_rate_pct == 0.5
        assert acc.overall_quality_improvement_pct == pytest.approx(93.75, abs=0.1)


class TestFinancialROIAndTCO:
    """Test suite for financial models, ROI calculations, and 3-Year TCO curves."""

    def test_roi_analyzer(self):
        roi = ROIAnalyzer.calculate_roi(
            monthly_docs=10000,
            employee_hourly_rate=28.0,
            baseline_mins_per_doc=16.0,
            ai_cost_per_doc=0.0080,
            annual_platform_investment=24000.0,
        )
        assert roi.baseline_monthly_cost == pytest.approx(74666.67, abs=1.0)
        assert roi.monthly_net_savings > 70000.0
        assert roi.annual_net_savings > 800000.0
        assert roi.net_annual_roi_pct > 3000.0
        assert roi.payback_period_months < 1.0
        assert roi.roi_multiple > 30.0

    def test_tco_analyzer(self):
        tco = TCOAnalyzer.calculate_3yr_tco(
            annual_docs=100000,
            labor_cost_per_doc=7.00,
            labor_inflation_rate=0.05,
            ai_fixed_annual_platform_fee=20000.0,
            ai_token_infra_cost_per_doc=0.0080,
        )
        assert tco.cumulative_3yr_human_tco > 2200000.0
        assert tco.cumulative_3yr_ai_tco < 70000.0
        assert tco.cumulative_3yr_net_savings > 2100000.0
        assert "O(1)" in tco.scaling_elasticity


class TestWorkflowModelsAndOptimization:
    """Test suite for industry workflow definitions and bottleneck analysis."""

    def test_workflow_comparisons_all_verticals(self):
        comparisons = WorkflowModelFactory.get_all_comparisons()
        assert len(comparisons) == 4

        verticals = [c.vertical for c in comparisons]
        assert IndustryVertical.FINANCE in verticals
        assert IndustryVertical.LEGAL in verticals
        assert IndustryVertical.HR in verticals
        assert IndustryVertical.HEALTHCARE in verticals

        for c in comparisons:
            assert c.speedup_multiplier > 200.0
            assert c.cost_reduction_pct > 99.0
            assert c.human_effort_reduction_pct > 95.0
            assert c.accuracy_improvement_pct > 5.0
            assert c.baseline.is_ai_system is False
            assert c.ai_system.is_ai_system is True

    def test_process_optimizer(self):
        optimizations = ProcessOptimizer.analyze_optimization_opportunities()
        assert len(optimizations) == 4
        for opt in optimizations:
            assert "workflow" in opt
            assert "bottleneck_identified" in opt
            assert "ai_optimization" in opt
            assert opt["eliminated_hand_offs"] >= 1


class TestEnterpriseAndAdoptionSimulation:
    """Test suite for multi-tier enterprise scaling and user adoption."""

    def test_enterprise_simulator(self):
        tiers = EnterpriseSimulator.simulate_all_tiers()
        assert len(tiers) == 3

        small = tiers[0]
        assert small.monthly_docs == 1000
        assert small.annual_net_savings > 75000.0

        mid = tiers[1]
        assert mid.monthly_docs == 50000
        assert mid.annual_net_savings > 4000000.0

        large = tiers[2]
        assert large.monthly_docs == 500000
        assert large.annual_net_savings > 40000000.0
        assert large.ftes_reallocated > 200.0

    def test_adoption_simulator(self):
        adoptions = AdoptionSimulator.simulate_role_adoption()
        assert len(adoptions) == 4
        for a in adoptions:
            assert a.satisfaction_score > 90.0
            assert a.adoption_velocity_days <= 7
            assert a.active_engagement_pct > 90.0


class TestCaseStudiesAndMasterScoring:
    """Test suite for case studies and master business value scoring."""

    def test_case_study_generator(self):
        studies = CaseStudyGenerator.generate_all_case_studies()
        assert len(studies) == 3
        for s in studies:
            assert len(s.title) > 5
            assert len(s.problem_statement) > 20
            assert len(s.solution_architecture) > 20
            assert len(s.quantified_results) >= 4
            assert len(s.executive_testimonial) > 10

    def test_business_value_scorer_perfect(self):
        score = BusinessValueScorer.calculate_score(100.0, 100.0, 100.0, 100.0)
        assert score.overall_business_score == 100.0
        assert score.grade == "A+"
        assert score.validation_status == "ENTERPRISE VALUE VALIDATED"

    def test_business_value_scorer_moderate(self):
        score = BusinessValueScorer.calculate_score(85.0, 80.0, 75.0, 70.0)
        assert score.overall_business_score < 90.0
        assert score.grade == "C"


class TestEvidenceExportAndManifest:
    """Test suite for artifact export and SHA-256 manifest generation."""

    def test_evidence_export(self, tmp_path):
        base_dir = str(tmp_path)
        auto_metrics = AutomationMetricsCalculator.calculate_metrics()
        productivity = ProductivityAnalyzer.calculate_productivity()
        accuracy = AccuracyComparator.compare_accuracy()
        roi = ROIAnalyzer.calculate_roi()
        tco = TCOAnalyzer.calculate_3yr_tco()
        workflows = WorkflowModelFactory.get_all_comparisons()
        sims = EnterpriseSimulator.simulate_all_tiers()
        adoptions = AdoptionSimulator.simulate_role_adoption()
        cases = CaseStudyGenerator.generate_all_case_studies()
        optimizations = ProcessOptimizer.analyze_optimization_opportunities()
        score = BusinessValueScorer.calculate_score()

        manifest = BusinessValueEvidenceGenerator.export_all_evidence(
            base_dir=base_dir,
            automation_metrics=auto_metrics,
            productivity_impact=productivity,
            accuracy_comp=accuracy,
            roi_result=roi,
            tco_result=tco,
            workflow_comparisons=workflows,
            simulations=sims,
            adoption_metrics=adoptions,
            case_studies=cases,
            optimizations=optimizations,
            master_score=score,
        )

        assert "artifacts" in manifest
        assert len(manifest["artifacts"]) == 8
        for name, meta in manifest["artifacts"].items():
            assert os.path.exists(meta["path"])
            assert len(meta["sha256"]) == 64
            assert meta["size_bytes"] > 0
