"""
Phase 3H.4.11: Enterprise Operational Readiness Scoring Test Suite
"""
import os
import json
from app.platform_verification.operational_readiness_verification.evaluators import (
    MetricsCompletenessEvaluator,
    MonitoringAccuracyEvaluator,
    AlertReliabilityEvaluator,
    IncidentQualityEvaluator,
    DashboardUsabilityEvaluator,
    SecurityReadinessEvaluator,
    MaturityClassifier,
    OperationalRiskAnalyzer,
    CertificationDecisionEngine,
    RemediationRecommendationGenerator,
)
from app.platform_verification.operational_readiness_verification.runtime.operational_readiness_runtime import (
    OperationalReadinessRuntime,
)
from app.platform_verification.operational_readiness_verification.domain.models import (
    MaturityLevel,
    CertificationStatus,
)


class TestOperationalReadinessVerification:
    def test_readiness_scoring_architecture(self):
        """3H.4.11.1: Verify readiness scoring runtime architecture and evaluation loop."""
        runtime = OperationalReadinessRuntime()
        results = runtime.evaluate_operational_readiness()

        assert results["composite_score"] >= 95.0
        assert results["certification"] == CertificationStatus.ENTERPRISE_OBSERVABILITY_READY.value
        assert results["maturity_level"] == MaturityLevel.LEVEL_5_ENTERPRISE.value
        assert results["release_approved"] is True

    def test_scoring_model_and_weights(self):
        """3H.4.11.2: Verify weighted formula: 20% Met, 20% Mon, 20% Alt, 15% Inc, 15% Dsh, 10% Sec."""
        runtime = OperationalReadinessRuntime()
        results = runtime.evaluate_operational_readiness()
        scorecard = results["scorecard"]

        expected_calc = round(
            (scorecard.metrics_completeness.score * 0.20)
            + (scorecard.monitoring_accuracy.score * 0.20)
            + (scorecard.alert_reliability.score * 0.20)
            + (scorecard.incident_quality.score * 0.15)
            + (scorecard.dashboard_usability.score * 0.15)
            + (scorecard.security_readiness.score * 0.10),
            2,
        )
        assert scorecard.composite_score == expected_calc

    def test_metrics_completeness_scoring(self):
        """3H.4.11.3: Verify metrics coverage score across App, Agent, Queue, and Infra."""
        evaluator = MetricsCompletenessEvaluator()
        res = evaluator.evaluate_metrics_completeness()

        assert res.passed is True
        assert res.score >= 90.0
        assert res.application_metrics_coverage == 100.0
        assert res.agent_metrics_coverage == 100.0
        assert res.queue_metrics_coverage == 100.0
        assert res.infrastructure_metrics_coverage == 100.0

    def test_monitoring_accuracy_and_mttd_scoring(self):
        """3H.4.11.4: Verify detection success rate and MTTD latency SLA."""
        evaluator = MonitoringAccuracyEvaluator()
        res = evaluator.evaluate_monitoring_accuracy()

        assert res.passed is True
        assert res.detection_success_rate == 100.0
        assert res.mean_time_to_detect_seconds < 30.0
        assert res.mttd_benchmark_met is True
        assert res.score >= 95.0

    def test_alert_reliability_and_precision_recall(self):
        """3H.4.11.5: Verify precision, recall, auto-resolution, and false positive rates."""
        evaluator = AlertReliabilityEvaluator()
        res = evaluator.evaluate_alert_reliability()

        assert res.passed is True
        assert res.precision_rate >= 95.0
        assert res.recall_rate == 100.0
        assert res.auto_resolution_rate == 100.0
        assert res.false_positive_rate <= 5.0
        assert res.score >= 95.0

    def test_incident_quality_scoring(self):
        """3H.4.11.6: Verify incident diagnostic payload completeness and runbook attachment."""
        evaluator = IncidentQualityEvaluator()
        res = evaluator.evaluate_incident_quality()

        assert res.passed is True
        assert res.payload_completeness_rate == 100.0
        assert res.diagnostic_value_rate == 100.0
        assert res.runbook_attachment_rate == 100.0
        assert res.score == 100.0

    def test_dashboard_usability_scoring(self):
        """3H.4.11.7: Verify usability across System, AI Workflow, Infra, and Agent dashboards."""
        evaluator = DashboardUsabilityEvaluator()
        res = evaluator.evaluate_dashboard_usability()

        assert res.passed is True
        assert res.system_dashboard_completeness == 100.0
        assert res.ai_workflow_dashboard_completeness == 100.0
        assert res.infrastructure_dashboard_completeness == 100.0
        assert res.agent_dashboard_completeness == 100.0
        assert res.score == 100.0

    def test_security_readiness_scoring(self):
        """3H.4.11.8: Verify security score across logs, metrics, traces, RBAC, and transport encryption."""
        evaluator = SecurityReadinessEvaluator()
        res = evaluator.evaluate_security_readiness()

        assert res.passed is True
        assert res.log_sanitization_rate == 100.0
        assert res.metric_privacy_rate == 100.0
        assert res.trace_scrubbing_rate == 100.0
        assert res.rbac_enforcement_rate == 100.0
        assert res.transport_encryption_rate == 100.0
        assert res.score == 100.0

    def test_maturity_level_classification(self):
        """3H.4.11.9: Verify Level 0 to Level 5 operational maturity classification."""
        classifier = MaturityClassifier()
        analyzer = OperationalRiskAnalyzer()

        metrics_eval = MetricsCompletenessEvaluator().evaluate_metrics_completeness()
        mon_eval = MonitoringAccuracyEvaluator().evaluate_monitoring_accuracy()
        alt_eval = AlertReliabilityEvaluator().evaluate_alert_reliability()
        inc_eval = IncidentQualityEvaluator().evaluate_incident_quality()
        dsh_eval = DashboardUsabilityEvaluator().evaluate_dashboard_usability()
        sec_eval = SecurityReadinessEvaluator().evaluate_security_readiness()

        risk_rep = analyzer.analyze_operational_risks(metrics_eval, mon_eval, alt_eval, inc_eval, dsh_eval, sec_eval)
        mat_rep = classifier.classify_maturity(98.5, risk_rep)

        assert mat_rep.level == MaturityLevel.LEVEL_5_ENTERPRISE
        assert mat_rep.level_numeric == 5
        assert len(mat_rep.criteria_met) >= 4

    def test_operational_risk_analyzer_hard_gates(self):
        """3H.4.11.10: Test hard-gate override rule: Security < 70 blocks release."""
        analyzer = OperationalRiskAnalyzer()
        metrics_eval = MetricsCompletenessEvaluator().evaluate_metrics_completeness()
        mon_eval = MonitoringAccuracyEvaluator().evaluate_monitoring_accuracy()
        alt_eval = AlertReliabilityEvaluator().evaluate_alert_reliability()
        inc_eval = IncidentQualityEvaluator().evaluate_incident_quality()
        dsh_eval = DashboardUsabilityEvaluator().evaluate_dashboard_usability()
        
        # Injected low security score
        sec_eval = SecurityReadinessEvaluator().evaluate_security_readiness()
        sec_eval.score = 65.0  # Under 70 threshold

        risk_rep = analyzer.analyze_operational_risks(metrics_eval, mon_eval, alt_eval, inc_eval, dsh_eval, sec_eval)
        assert risk_rep.hard_gate_passed is False
        assert risk_rep.blocking_risks_count >= 1
        assert any(r.risk_id == "RISK-CRIT-SEC" for r in risk_rep.evaluated_risks)

    def test_certification_decision_engine(self):
        """3H.4.11.11: Verify certification logic for Enterprise Observability Ready status."""
        engine = CertificationDecisionEngine()
        classifier = MaturityClassifier()
        analyzer = OperationalRiskAnalyzer()

        metrics_eval = MetricsCompletenessEvaluator().evaluate_metrics_completeness()
        mon_eval = MonitoringAccuracyEvaluator().evaluate_monitoring_accuracy()
        alt_eval = AlertReliabilityEvaluator().evaluate_alert_reliability()
        inc_eval = IncidentQualityEvaluator().evaluate_incident_quality()
        dsh_eval = DashboardUsabilityEvaluator().evaluate_dashboard_usability()
        sec_eval = SecurityReadinessEvaluator().evaluate_security_readiness()

        risk_rep = analyzer.analyze_operational_risks(metrics_eval, mon_eval, alt_eval, inc_eval, dsh_eval, sec_eval)
        mat_rep = classifier.classify_maturity(99.0, risk_rep)

        cert = engine.evaluate_certification(99.0, mat_rep, risk_rep)
        assert cert.certification == CertificationStatus.ENTERPRISE_OBSERVABILITY_READY
        assert cert.release_approved is True
        assert len(cert.blocking_issues) == 0

    def test_remediation_recommendation_generator(self):
        """3H.4.11.12: Verify auto-generation of prioritized engineering action items."""
        generator = RemediationRecommendationGenerator()
        analyzer = OperationalRiskAnalyzer()

        metrics_eval = MetricsCompletenessEvaluator().evaluate_metrics_completeness()
        mon_eval = MonitoringAccuracyEvaluator().evaluate_monitoring_accuracy()
        alt_eval = AlertReliabilityEvaluator().evaluate_alert_reliability()
        inc_eval = IncidentQualityEvaluator().evaluate_incident_quality()
        dsh_eval = DashboardUsabilityEvaluator().evaluate_dashboard_usability()
        sec_eval = SecurityReadinessEvaluator().evaluate_security_readiness()

        risk_rep = analyzer.analyze_operational_risks(metrics_eval, mon_eval, alt_eval, inc_eval, dsh_eval, sec_eval)
        remediation = generator.generate_recommendations(metrics_eval, mon_eval, alt_eval, inc_eval, dsh_eval, sec_eval, risk_rep)

        assert remediation.total_recommendations >= 2
        for rec in remediation.recommendations:
            assert rec.action_id.startswith("REC-")
            assert len(rec.recommended_action) > 10

    def test_readiness_evidence_generation_and_manifests(self, tmp_path):
        """3H.4.11.13: Verify generation and schema correctness of all 12 evidence manifests."""
        runtime = OperationalReadinessRuntime()
        out_dir = str(tmp_path / "operational_readiness_verification")
        results = runtime.evaluate_operational_readiness(output_dir=out_dir)

        expected_files = [
            "scoring_model.json",
            "metrics_score.json",
            "monitoring_score.json",
            "alert_score.json",
            "incident_score.json",
            "dashboard_score.json",
            "security_score.json",
            "maturity_report.json",
            "risk_report.json",
            "certification_result.json",
            "remediation_report.json",
            "metadata.json",
        ]

        assert len(results["exported_files"]) == 12
        for ef in expected_files:
            file_path = os.path.join(out_dir, ef)
            assert os.path.exists(file_path), f"Missing manifest: {ef}"
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert data is not None
