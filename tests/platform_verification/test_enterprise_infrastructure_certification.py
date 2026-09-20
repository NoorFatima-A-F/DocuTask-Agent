"""
Phase 3O: Comprehensive Test Suite for Enterprise Infrastructure Quality Scoring & Certification Framework.
"""

import json
import os
from pathlib import Path
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.enterprise_infrastructure_certification.domain.models import (
    CategoryQualityScore,
    CertificationDecision,
    CertificationLevel,
    MaturityAssessment,
    MaturityLevel,
    NormalizedEvidenceItem,
    QualityRegressionReport,
    QualityScorecard,
    RawEvidenceBundle,
    RiskAssessmentReport,
    RiskFinding,
    RiskLevel,
    VerificationManifest,
    VerificationStatus,
)
from app.platform_verification.enterprise_infrastructure_certification.core.evidence_collector import (
    EvidenceCollector,
)
from app.platform_verification.enterprise_infrastructure_certification.core.evidence_normalizer import (
    EvidenceNormalizer,
)
from app.platform_verification.enterprise_infrastructure_certification.scoring.infrastructure_quality_scorer import (
    InfrastructureQualityScorer,
)
from app.platform_verification.enterprise_infrastructure_certification.risk.infrastructure_risk_analyzer import (
    InfrastructureRiskAnalyzer,
)
from app.platform_verification.enterprise_infrastructure_certification.certification.infrastructure_certifier import (
    InfrastructureCertifier,
)
from app.platform_verification.enterprise_infrastructure_certification.certification.maturity_evaluator import (
    MaturityEvaluator,
)
from app.platform_verification.enterprise_infrastructure_certification.regression.quality_regression_detector import (
    QualityRegressionDetector,
)
from app.platform_verification.enterprise_infrastructure_certification.reports.readiness_markdown_generator import (
    ReadinessMarkdownGenerator,
)
from app.platform_verification.enterprise_infrastructure_certification.exporter.infrastructure_certification_exporter import (
    InfrastructureCertificationExporter,
)
from app.platform_verification.enterprise_infrastructure_certification.runtime.infrastructure_certification_runtime import (
    InfrastructureCertificationRuntime,
)
from app.platform_verification.enterprise_infrastructure_certification.api.infrastructure_certification_api import (
    router,
)


class TestEnterpriseInfrastructureCertification:
    """Complete test suite for Phase 3O."""

    @pytest.fixture
    def app_client(self):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    @pytest.fixture
    def temp_export_dir(self, tmp_path):
        export_path = tmp_path / "test_infrastructure_certification"
        export_path.mkdir(parents=True, exist_ok=True)
        return str(export_path)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. Evidence Collector & Normalizer Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_evidence_collector_default_bundles(self):
        collector = EvidenceCollector()
        bundles = collector.collect_all_evidence(search_paths=[])
        assert len(bundles) >= 5
        for bundle in bundles:
            assert bundle.evidence_count > 0
            assert len(bundle.raw_payloads) > 0

    def test_evidence_normalizer_categorization(self):
        collector = EvidenceCollector()
        bundles = collector.collect_all_evidence(search_paths=[])
        normalizer = EvidenceNormalizer()
        items = normalizer.normalize(bundles)

        assert len(items) > 10
        categories_present = {item.category for item in items}
        assert "Reliability" in categories_present
        assert "Security" in categories_present
        assert "Scalability" in categories_present
        assert "Observability" in categories_present
        assert "Deployment Quality" in categories_present
        assert "Recovery Capability" in categories_present

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Quality Scoring Engine Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_quality_scorer_all_passed(self):
        collector = EvidenceCollector()
        bundles = collector.collect_all_evidence(search_paths=[])
        normalizer = EvidenceNormalizer()
        items = normalizer.normalize(bundles)

        scorer = InfrastructureQualityScorer()
        scorecard = scorer.calculate_score(items, execution_time_seconds=0.5)

        assert scorecard.overall_score == 100.0
        assert scorecard.grade == "ENTERPRISE_READY"
        assert len(scorecard.categories) == 6
        assert scorecard.total_evidence_evaluated == len(items)
        assert scorecard.total_evidence_passed == len(items)

        # Verify exact category weights
        assert scorecard.categories["Reliability"].weight == 0.25
        assert scorecard.categories["Security"].weight == 0.20
        assert scorecard.categories["Scalability"].weight == 0.20
        assert scorecard.categories["Observability"].weight == 0.15
        assert scorecard.categories["Deployment Quality"].weight == 0.10
        assert scorecard.categories["Recovery Capability"].weight == 0.10

    def test_quality_scorer_weighted_calculation(self):
        scorer = InfrastructureQualityScorer()
        custom_items = [
            NormalizedEvidenceItem(category="Reliability", test_id="REL-1", name="Rel 1", score=100.0, status=VerificationStatus.PASSED),
            NormalizedEvidenceItem(category="Security", test_id="SEC-1", name="Sec 1", score=50.0, status=VerificationStatus.FAILED),
        ]
        scorecard = scorer.calculate_score(custom_items)
        # Reliability: 100 * 0.25 = 25.0
        # Security: 0 * 0.20 = 0.0
        # Scalability: 100 * 0.20 = 20.0
        # Observability: 100 * 0.15 = 15.0
        # Deployment: 100 * 0.10 = 10.0
        # Recovery: 100 * 0.10 = 10.0
        # Total = 25 + 0 + 20 + 15 + 10 + 10 = 80.0
        assert scorecard.overall_score == 80.0
        assert scorecard.grade == "TESTING_READY"

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Risk Assessment & Critical Override Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_risk_analyzer_clean_state(self):
        collector = EvidenceCollector()
        bundles = collector.collect_all_evidence(search_paths=[])
        normalizer = EvidenceNormalizer()
        items = normalizer.normalize(bundles)
        scorer = InfrastructureQualityScorer()
        scorecard = scorer.calculate_score(items)

        analyzer = InfrastructureRiskAnalyzer()
        risk_report = analyzer.assess_risks(scorecard, items)

        assert risk_report.highest_risk == RiskLevel.NONE
        assert risk_report.critical_risks_count == 0
        assert risk_report.high_risks_count == 0
        assert risk_report.production_blocker_present is False
        assert len(risk_report.risks) == 0

    def test_risk_analyzer_critical_failure_override(self):
        items = [
            NormalizedEvidenceItem(
                category="Security",
                test_id="SEC-CRIT",
                name="Critical CVE Vulnerability",
                score=0.0,
                status=VerificationStatus.FAILED,
                severity=RiskLevel.CRITICAL,
                details="Unpatched Remote Code Execution in Base Container Image",
            )
        ]
        scorer = InfrastructureQualityScorer()
        scorecard = scorer.calculate_score(items)
        analyzer = InfrastructureRiskAnalyzer()
        risk_report = analyzer.assess_risks(scorecard, items)

        assert risk_report.highest_risk == RiskLevel.CRITICAL
        assert risk_report.critical_risks_count == 1
        assert risk_report.production_blocker_present is True
        assert len(risk_report.risks) == 1

        # Certification engine must block deployment
        certifier = InfrastructureCertifier()
        decision = certifier.evaluate_certification(scorecard, risk_report)
        assert decision.deployment_approved is False
        assert decision.certification == CertificationLevel.BLOCKED
        assert len(decision.blocker_reasons) > 0

    # ──────────────────────────────────────────────────────────────────────────
    # 4. Production Certification & Maturity Model Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_certifier_enterprise_ready(self):
        collector = EvidenceCollector()
        bundles = collector.collect_all_evidence(search_paths=[])
        normalizer = EvidenceNormalizer()
        items = normalizer.normalize(bundles)
        scorer = InfrastructureQualityScorer()
        scorecard = scorer.calculate_score(items)
        analyzer = InfrastructureRiskAnalyzer()
        risk_report = analyzer.assess_risks(scorecard, items)

        certifier = InfrastructureCertifier()
        decision = certifier.evaluate_certification(scorecard, risk_report)

        assert decision.deployment_approved is True
        assert decision.certification == CertificationLevel.ENTERPRISE_READY
        assert decision.status == VerificationStatus.PASSED
        assert len(decision.recommendations) > 0

    def test_maturity_evaluator_level_5(self):
        collector = EvidenceCollector()
        bundles = collector.collect_all_evidence(search_paths=[])
        normalizer = EvidenceNormalizer()
        items = normalizer.normalize(bundles)
        scorer = InfrastructureQualityScorer()
        scorecard = scorer.calculate_score(items)
        analyzer = InfrastructureRiskAnalyzer()
        risk_report = analyzer.assess_risks(scorecard, items)

        evaluator = MaturityEvaluator()
        maturity = evaluator.assess_maturity(scorecard, risk_report)

        assert maturity.maturity_level == MaturityLevel.LEVEL_5
        assert maturity.maturity_score == 100.0
        assert len(maturity.capabilities_achieved) >= 5
        assert len(maturity.pillar_ratings) == 6

    # ──────────────────────────────────────────────────────────────────────────
    # 5. Quality Regression Detector Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_regression_detector_clean(self):
        scorer = InfrastructureQualityScorer()
        scorecard = QualityScorecard(
            overall_score=100.0,
            categories={
                "Reliability": CategoryQualityScore(category="Reliability", weight=0.25, score=100.0, contribution=25.0, passed_items=10, total_items=10),
            },
        )
        detector = QualityRegressionDetector()
        report = detector.detect_regressions(scorecard)

        assert report.regression_detected is False
        assert report.score_delta >= 0

    def test_regression_detector_detects_drop(self):
        scorecard = QualityScorecard(
            overall_score=85.0,
            categories={
                "Reliability": CategoryQualityScore(category="Reliability", weight=0.25, score=80.0, contribution=20.0, passed_items=8, total_items=10),
            },
        )
        detector = QualityRegressionDetector()
        report = detector.detect_regressions(
            scorecard,
            previous_data={"overall_score": 96.0, "categories": {"Reliability": 98.0}, "version": "3.16.0"},
        )

        assert report.regression_detected is True
        assert report.score_delta < -3.0
        assert any(f.is_regression for f in report.findings)

    # ──────────────────────────────────────────────────────────────────────────
    # 6. Exporter, Manifest & Markdown Report Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_exporter_and_markdown_generator(self, temp_export_dir):
        runtime = InfrastructureCertificationRuntime()
        result = runtime.run_full_certification(export_dir=temp_export_dir)

        assert result["passed"] is True
        assert result["overall_score"] == 100.0
        assert result["certification"] == "Enterprise Infrastructure Ready"

        base = Path(temp_export_dir)
        assert (base / "evidence" / "normalized_results" / "normalized_evidence.json").exists()
        assert (base / "scoring" / "quality_score.json").exists()
        assert (base / "scoring" / "maturity_assessment.json").exists()
        assert (base / "reports" / "certification_report.json").exists()
        assert (base / "reports" / "risk_assessment.json").exists()
        assert (base / "reports" / "regression_report.json").exists()
        assert (base / "reports" / "readiness_report.md").exists()
        assert (base / "Infrastructure_Readiness_Report.md").exists()
        assert (base / "history" / "previous_scores.json").exists()
        assert (base / "metadata.json").exists()
        assert (base / "manifest.json").exists()

        manifest = result["manifest"]
        assert len(manifest.files) >= 8
        for fentry in manifest.files:
            assert len(fentry.sha256) == 64
            assert fentry.size_bytes > 0

    # ──────────────────────────────────────────────────────────────────────────
    # 7. FastAPI REST API Endpoints Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_api_health(self, app_client):
        res = app_client.get("/api/v1/certification/health")
        assert res.status_code == 200
        assert res.json()["status"] == "healthy"

    def test_api_pillars(self, app_client):
        res = app_client.get("/api/v1/certification/pillars")
        assert res.status_code == 200
        pillars = res.json()
        assert len(pillars) == 6
        assert pillars[0]["name"] == "Reliability"
        assert pillars[0]["weight"] == 0.25

    def test_api_run_certification(self, app_client):
        res = app_client.post("/api/v1/certification/run")
        assert res.status_code == 200
        manifest = res.json()
        assert manifest["overall_score"] == 100.0
        assert manifest["certification"] == "Enterprise Infrastructure Ready"
        assert manifest["deployment_approved"] is True

    def test_api_scorecard(self, app_client):
        res = app_client.get("/api/v1/certification/scorecard")
        assert res.status_code == 200
        data = res.json()
        assert data["overall_score"] == 100.0
        assert "categories" in data

    def test_api_decision(self, app_client):
        res = app_client.get("/api/v1/certification/decision")
        assert res.status_code == 200
        data = res.json()
        assert data["deployment_approved"] is True
        assert data["certification"] == "Enterprise Infrastructure Ready"

    def test_api_risks(self, app_client):
        res = app_client.get("/api/v1/certification/risks")
        assert res.status_code == 200
        data = res.json()
        assert data["production_blocker_present"] is False
        assert data["critical_risks_count"] == 0

    def test_api_maturity(self, app_client):
        res = app_client.get("/api/v1/certification/maturity")
        assert res.status_code == 200
        data = res.json()
        assert "Level 5" in data["maturity_level"]

    def test_api_manifest(self, app_client):
        res = app_client.get("/api/v1/certification/manifest")
        assert res.status_code == 200
        data = res.json()
        assert len(data["files"]) > 0

    def test_api_markdown_report(self, app_client):
        res = app_client.get("/api/v1/certification/report/markdown")
        assert res.status_code == 200
        assert "DocuTask Agent — Enterprise Infrastructure Readiness & Certification Report" in res.text
