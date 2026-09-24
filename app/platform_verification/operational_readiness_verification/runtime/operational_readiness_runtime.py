"""
Phase 3H.4.11: Operational Readiness Verification Runtime
"""
from typing import Dict, Any
from ..evaluators import (
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
from ..exporter.readiness_evidence_exporter import ReadinessEvidenceExporter
from ..domain.models import OperationalReadinessScorecard


class OperationalReadinessRuntime:
    def __init__(self):
        self.metrics_evaluator = MetricsCompletenessEvaluator()
        self.monitoring_evaluator = MonitoringAccuracyEvaluator()
        self.alert_evaluator = AlertReliabilityEvaluator()
        self.incident_evaluator = IncidentQualityEvaluator()
        self.dashboard_evaluator = DashboardUsabilityEvaluator()
        self.security_evaluator = SecurityReadinessEvaluator()
        self.risk_analyzer = OperationalRiskAnalyzer()
        self.maturity_classifier = MaturityClassifier()
        self.certification_engine = CertificationDecisionEngine()
        self.remediation_generator = RemediationRecommendationGenerator()
        self.exporter = ReadinessEvidenceExporter()

    def evaluate_operational_readiness(self, output_dir: str = "operational_readiness_verification") -> Dict[str, Any]:
        metrics_score = self.metrics_evaluator.evaluate_metrics_completeness()
        monitoring_score = self.monitoring_evaluator.evaluate_monitoring_accuracy()
        alert_score = self.alert_evaluator.evaluate_alert_reliability()
        incident_score = self.incident_evaluator.evaluate_incident_quality()
        dashboard_score = self.dashboard_evaluator.evaluate_dashboard_usability()
        security_score = self.security_evaluator.evaluate_security_readiness()

        composite_score = round(
            (metrics_score.score * 0.20)
            + (monitoring_score.score * 0.20)
            + (alert_score.score * 0.20)
            + (incident_score.score * 0.15)
            + (dashboard_score.score * 0.15)
            + (security_score.score * 0.10),
            2,
        )

        risk_report = self.risk_analyzer.analyze_operational_risks(
            metrics_score=metrics_score,
            monitoring_score=monitoring_score,
            alert_score=alert_score,
            incident_score=incident_score,
            dashboard_score=dashboard_score,
            security_score=security_score,
        )

        maturity_report = self.maturity_classifier.classify_maturity(
            composite_score=composite_score,
            risk_report=risk_report,
        )

        certification_result = self.certification_engine.evaluate_certification(
            composite_score=composite_score,
            maturity_report=maturity_report,
            risk_report=risk_report,
        )

        remediation_report = self.remediation_generator.generate_recommendations(
            metrics_score=metrics_score,
            monitoring_score=monitoring_score,
            alert_score=alert_score,
            incident_score=incident_score,
            dashboard_score=dashboard_score,
            security_score=security_score,
            risk_report=risk_report,
        )

        scorecard = OperationalReadinessScorecard(
            metrics_completeness=metrics_score,
            monitoring_accuracy=monitoring_score,
            alert_reliability=alert_score,
            incident_quality=incident_score,
            dashboard_usability=dashboard_score,
            security_readiness=security_score,
            composite_score=composite_score,
            maturity_report=maturity_report,
            risk_report=risk_report,
            certification_result=certification_result,
            remediation_report=remediation_report,
        )

        exported_files = self.exporter.export_evidence_manifests(
            output_dir=output_dir,
            scorecard=scorecard,
        )

        return {
            "scorecard": scorecard,
            "exported_files": exported_files,
            "composite_score": composite_score,
            "certification": certification_result.certification.value,
            "maturity_level": maturity_report.level.value,
            "release_approved": certification_result.release_approved,
        }
