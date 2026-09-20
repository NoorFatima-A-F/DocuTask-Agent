"""
Comprehensive Unit and Integration Test Suite for Phase V12 — Enterprise AI Platform Verification Certification & Readiness Assessment Program (EAP-VCRAP).
"""

import os
import pytest
from app.certification.domain.models import (
    MaturityTier,
    RiskCategory,
    RiskSeverity,
)
from app.certification.aggregation.result_aggregator import ResultAggregator
from app.certification.aggregation.maturity_engine import MaturityEngine
from app.certification.aggregation.readiness_calculator import ReadinessCalculator
from app.certification.governance.evidence_graph_builder import EvidenceGraphBuilder
from app.certification.governance.risk_register_engine import RiskRegisterEngine
from app.certification.governance.ai_governance_evaluator import AIGovernanceEvaluator
from app.certification.portfolio.system_card_generator import SystemCardGenerator
from app.certification.portfolio.portfolio_package_builder import PortfolioPackageBuilder
from app.certification.reporting.final_report_generator import FinalReportGenerator
from app.certification.reporting.evidence_exporter import EvidenceExporter


class TestResultAggregationAndMaturity:
    """Test suite for multi-phase aggregation, maturity tiers, and readiness scoring."""

    def test_result_aggregator_all_phases(self):
        phases = ResultAggregator.aggregate_all_phases()
        assert len(phases) == 11
        for p in phases:
            assert p.score == 100.0
            assert p.status == "PASSED"
            assert p.tests_passed == p.total_tests
            assert len(p.key_evidence_files) >= 2

    def test_maturity_engine_levels(self):
        maturity = MaturityEngine.evaluate_maturity()
        assert maturity.current_maturity_level >= 4.5
        assert maturity.tier == MaturityTier.LEVEL_4_ENTERPRISE_READY
        assert len(maturity.evaluation_criteria) >= 5

        # Test lower tier
        lower = MaturityEngine.evaluate_maturity(2.0, 2.0, 2.0, 2.0, 2.0)
        assert lower.tier == MaturityTier.LEVEL_1_FUNCTIONAL

    def test_readiness_calculator_score(self):
        score = ReadinessCalculator.calculate_readiness_score(100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0)
        assert score.overall_readiness_score == 100.0
        assert score.grade == "A+"
        assert "DocuTask Agent" in score.readiness_statement


class TestGovernanceAndRiskRegister:
    """Test suite for evidence graph, risk register, and AI governance."""

    def test_evidence_graph_builder(self):
        graph = EvidenceGraphBuilder.build_evidence_graph()
        assert len(graph) == 6
        for node in graph:
            assert node.verified is True
            assert len(node.sha256_hash) == 64
            assert node.claim_id.startswith("CLAIM-")

    def test_risk_register_engine(self):
        risks = RiskRegisterEngine.get_full_risk_register()
        assert len(risks) == 5
        for r in risks:
            assert r.risk_id.startswith("RISK-")
            assert r.status in ["MITIGATED", "CONTROLLED", "MONITORED"]
            assert len(r.mitigation_control) > 10

    def test_ai_governance_evaluator(self):
        gov = AIGovernanceEvaluator.evaluate_governance()
        assert gov.overall_governance_score > 95.0
        assert gov.transparency_score > 95.0
        assert gov.human_oversight_score > 95.0
        assert "NIST AI" in gov.framework_alignment


class TestPortfolioAndReporting:
    """Test suite for System Card, Portfolio Deliverables, and Evidence Export."""

    def test_system_card_generator(self):
        card = SystemCardGenerator.generate_system_card_markdown()
        assert "# DocuTask Agent" in card
        assert "Intended Use" in card
        assert "Safety, Governance & Limitations" in card
        assert "Human-in-the-Loop" in card

    def test_portfolio_package_builder(self, tmp_path):
        base_dir = str(tmp_path)
        docs = PortfolioPackageBuilder.generate_portfolio_package(base_dir)
        assert len(docs) == 9
        for d in docs:
            assert d.size_bytes > 0
            assert len(d.sha256_hash) == 64
            assert os.path.exists(os.path.join(base_dir, "portfolio_package", d.filename))

    def test_final_report_generator(self):
        phases = ResultAggregator.aggregate_all_phases()
        maturity = MaturityEngine.evaluate_maturity()
        readiness = ReadinessCalculator.calculate_readiness_score()
        graph = EvidenceGraphBuilder.build_evidence_graph()
        risks = RiskRegisterEngine.get_full_risk_register()
        gov = AIGovernanceEvaluator.evaluate_governance()
        docs = []

        report = FinalReportGenerator.generate_report_markdown(
            phases, maturity, readiness, graph, risks, gov, docs
        )
        assert "# Master Enterprise AI Platform Verification" in report
        assert "Enterprise AI Maturity Model" in report
        assert "Enterprise AI Risk Register" in report

    def test_evidence_exporter(self, tmp_path):
        base_dir = str(tmp_path)
        phases = ResultAggregator.aggregate_all_phases()
        maturity = MaturityEngine.evaluate_maturity()
        readiness = ReadinessCalculator.calculate_readiness_score()
        graph = EvidenceGraphBuilder.build_evidence_graph()
        risks = RiskRegisterEngine.get_full_risk_register()
        gov = AIGovernanceEvaluator.evaluate_governance()
        docs = PortfolioPackageBuilder.generate_portfolio_package(base_dir)

        manifest = EvidenceExporter.export_all_certification_evidence(
            base_dir=base_dir,
            phases_summary=phases,
            maturity_assessment=maturity,
            readiness_score=readiness,
            evidence_graph=graph,
            risk_register=risks,
            governance_audit=gov,
            portfolio_docs=docs,
        )

        assert "artifacts" in manifest
        assert len(manifest["artifacts"]) == 8
        for name, meta in manifest["artifacts"].items():
            assert os.path.exists(meta["path"])
            assert len(meta["sha256"]) == 64
            assert meta["size_bytes"] > 0
