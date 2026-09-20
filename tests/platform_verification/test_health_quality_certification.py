"""
Unit and Integration Tests for Phase 3H.5.11: Health Quality Scoring & Operational Certification Framework
"""
import os
import json
import pytest

from app.platform_verification.health_quality_certification.domain.models import (
    HealthMaturityLevel,
    CertificationStatus,
    DeploymentDecision,
)
from app.platform_verification.health_quality_certification.evaluators import (
    HealthQualityEvaluator,
    SREReliabilityEngine,
    RegressionDetector,
    DeploymentReadinessGate,
)
from app.platform_verification.health_quality_certification.scoring import HealthQualityScorer
from app.platform_verification.health_quality_certification.exporter import HealthQualityExporter
from app.platform_verification.health_quality_certification.runtime import HealthQualityRuntime
from app.platform_verification.health_quality_certification.api.health_quality_api import (
    get_health_certification_status,
    run_health_quality_certification,
    check_production_deployment_gate,
)


class TestHealthQualityCertification:
    @pytest.fixture
    def test_output_dir(self, tmp_path):
        return str(tmp_path / "health_quality_certification_evidence")

    def test_01_health_quality_evaluator_all_dimensions(self):
        evaluator = HealthQualityEvaluator()

        liveness = evaluator.evaluate_liveness()
        assert liveness.liveness_accuracy >= 99.0
        assert liveness.false_alive_rate == 0.0
        assert liveness.score >= 95.0

        readiness = evaluator.evaluate_readiness()
        assert readiness.readiness_accuracy >= 99.0
        assert readiness.false_ready_rate == 0.0
        assert readiness.score >= 95.0

        deps = evaluator.evaluate_dependencies()
        assert len(deps.dependencies_monitored) == 6
        assert deps.dependency_visibility == 100.0
        assert deps.critical_dependency_invisible is False

        failure = evaluator.evaluate_failure_detection()
        assert failure.mttd_seconds <= 2.5
        assert failure.scenarios_detected_count == 5

        recovery = evaluator.evaluate_recovery()
        assert recovery.mttr_seconds <= 15.0
        assert recovery.recovery_verified is True

        monitoring = evaluator.evaluate_monitoring()
        assert monitoring.metric_coverage_pct >= 95.0
        assert len(monitoring.integrations) == 4

        security = evaluator.evaluate_security()
        assert security.secret_exposure_count == 0
        assert security.security_score == 100.0

        evidence = evaluator.evaluate_evidence()
        assert evidence.evidence_missing is False
        assert evidence.reports_present is True

    def test_02_sre_reliability_engine(self):
        engine = SREReliabilityEngine()
        metrics = engine.calculate_reliability_metrics()

        assert metrics.availability_pct >= 99.90
        assert metrics.slo_compliant is True
        assert metrics.mttd_seconds > 0.0
        assert metrics.mttr_seconds > 0.0
        assert metrics.mtbf_hours > 0.0

    def test_03_regression_detector(self):
        detector = RegressionDetector()

        # Normal/improved build
        current_scores = {
            "liveness": 99.0,
            "readiness": 98.5,
            "dependencies": 99.5,
            "failure_detection": 97.5,
            "recovery": 96.0,
            "monitoring": 98.5,
            "security": 100.0,
            "evidence": 100.0,
            "overall": 98.4,
        }
        report = detector.detect_regression(current_scores=current_scores)
        assert report.regression_detected is False
        assert report.regression_policy_passed is True

        # Severe regression build
        regressed_scores = {
            "liveness": 70.0,
            "readiness": 65.0,
            "dependencies": 75.0,
            "failure_detection": 60.0,
            "recovery": 55.0,
            "monitoring": 70.0,
            "security": 90.0,
            "evidence": 80.0,
            "overall": 69.5,
        }
        regressed_report = detector.detect_regression(current_scores=regressed_scores)
        assert regressed_report.regression_detected is True
        assert regressed_report.regression_policy_passed is False

    def test_04_deployment_readiness_gate(self):
        gatekeeper = DeploymentReadinessGate(minimum_score=90.0)
        sre_engine = SREReliabilityEngine()
        sre_metrics = sre_engine.calculate_reliability_metrics()

        detector = RegressionDetector()
        clean_reg_report = detector.detect_regression(
            current_scores={
                "liveness": 99.0, "readiness": 98.5, "dependencies": 99.5,
                "failure_detection": 97.5, "recovery": 96.0, "monitoring": 98.5,
                "security": 100.0, "evidence": 100.0, "overall": 98.4,
            }
        )

        # Approved case
        gate_report = gatekeeper.evaluate_deployment_gate(
            overall_score=98.4,
            liveness_score=99.0,
            readiness_score=98.5,
            security_score=100.0,
            failure_detection_score=97.5,
            sre_metrics=sre_metrics,
            regression_report=clean_reg_report,
        )
        assert gate_report.decision == DeploymentDecision.APPROVED
        assert gate_report.critical_requirements_met is True

        # Blocked case: low security
        blocked_report = gatekeeper.evaluate_deployment_gate(
            overall_score=85.0,
            liveness_score=99.0,
            readiness_score=98.5,
            security_score=80.0,  # Below 95 critical requirement
            failure_detection_score=97.5,
            sre_metrics=sre_metrics,
            regression_report=clean_reg_report,
        )
        assert blocked_report.decision == DeploymentDecision.BLOCKED
        assert blocked_report.critical_requirements_met is False

    def test_05_health_quality_scorer_and_certification(self):
        evaluator = HealthQualityEvaluator()
        sre_engine = SREReliabilityEngine()
        reg_detector = RegressionDetector()
        gatekeeper = DeploymentReadinessGate()
        scorer = HealthQualityScorer()

        l = evaluator.evaluate_liveness()
        r = evaluator.evaluate_readiness()
        d = evaluator.evaluate_dependencies()
        fd = evaluator.evaluate_failure_detection()
        rec = evaluator.evaluate_recovery()
        m = evaluator.evaluate_monitoring()
        sec = evaluator.evaluate_security()
        ev = evaluator.evaluate_evidence()
        sre = sre_engine.calculate_reliability_metrics()
        reg = reg_detector.detect_regression(
            current_scores={
                "liveness": l.score, "readiness": r.score, "dependencies": d.score,
                "failure_detection": fd.score, "recovery": rec.score, "monitoring": m.score,
                "security": sec.score, "evidence": ev.score, "overall": 98.4,
            }
        )
        gate = gatekeeper.evaluate_deployment_gate(
            overall_score=98.4,
            liveness_score=l.score,
            readiness_score=r.score,
            security_score=sec.score,
            failure_detection_score=fd.score,
            sre_metrics=sre,
            regression_report=reg,
        )

        scorecard = scorer.calculate_certification_scorecard(
            liveness=l,
            readiness=r,
            dependencies=d,
            failure_detection=fd,
            recovery=rec,
            monitoring=m,
            security=sec,
            evidence=ev,
            sre_metrics=sre,
            regression_report=reg,
            gate_report=gate,
        )

        assert scorecard.overall_score >= 95.0
        assert scorecard.maturity_level == HealthMaturityLevel.LEVEL_4_ENTERPRISE_HEALTH
        assert scorecard.certification_status == CertificationStatus.CERTIFIED
        assert scorecard.passed is True
        assert len(scorecard.category_scores) == 8

    def test_06_veto_conditions(self):
        evaluator = HealthQualityEvaluator()
        sre_engine = SREReliabilityEngine()
        reg_detector = RegressionDetector()
        gatekeeper = DeploymentReadinessGate()
        scorer = HealthQualityScorer()

        l = evaluator.evaluate_liveness()
        r = evaluator.evaluate_readiness()
        d = evaluator.evaluate_dependencies()
        # Inject veto condition: Critical dependency invisible
        d.critical_dependency_invisible = True
        fd = evaluator.evaluate_failure_detection()
        rec = evaluator.evaluate_recovery()
        m = evaluator.evaluate_monitoring()
        sec = evaluator.evaluate_security()
        ev = evaluator.evaluate_evidence()
        sre = sre_engine.calculate_reliability_metrics()
        reg = reg_detector.detect_regression(current_scores={"overall": 95.0})
        gate = gatekeeper.evaluate_deployment_gate(
            overall_score=95.0, liveness_score=l.score, readiness_score=r.score,
            security_score=sec.score, failure_detection_score=fd.score,
            sre_metrics=sre, regression_report=reg,
        )

        scorecard = scorer.calculate_certification_scorecard(
            liveness=l, readiness=r, dependencies=d, failure_detection=fd,
            recovery=rec, monitoring=m, security=sec, evidence=ev,
            sre_metrics=sre, regression_report=reg, gate_report=gate,
        )

        assert scorecard.certification_report.veto_triggered is True
        assert scorecard.certification_status == CertificationStatus.FAILED
        assert scorecard.passed is False

    def test_07_health_quality_exporter(self, test_output_dir):
        runtime = HealthQualityRuntime(output_dir=test_output_dir)
        results = runtime.run_full_certification()

        assert os.path.exists(test_output_dir)
        assert len(results["exported_files"]) == 7

        metadata_path = os.path.join(test_output_dir, "metadata.json")
        assert os.path.exists(metadata_path)

        with open(metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        assert meta["overall_score"] >= 95.0
        assert meta["certification_status"] == "CERTIFIED"
        assert meta["passed"] is True
        assert "file_manifest" in meta
        assert "scoring_model.json" in meta["file_manifest"]
        assert "certification_report.json" in meta["file_manifest"]

    def test_08_health_quality_api(self):
        status = get_health_certification_status()
        assert status["status"] == "ACTIVE"
        assert status["phase"] == "3H.5.11"

        verify = run_health_quality_certification()
        assert verify["overall_score"] >= 95.0
        assert verify["certification_status"] == "CERTIFIED"
        assert verify["passed"] is True
        assert verify["deployment_decision"] == "APPROVED"

        gate = check_production_deployment_gate()
        assert gate["decision"] == "APPROVED"
        assert gate["critical_requirements_met"] is True
