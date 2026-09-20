"""AI Health Monitoring Master Runtime.

Coordinates all 12 modules of Phase 3H.3.9 AI Health Monitoring Integration.
"""

from __future__ import annotations

from typing import Any, Dict, Optional
from datetime import datetime, timezone

from app.platform_verification.ai_health_monitoring.architecture.ai_observability_architecture_verifier import AIObservabilityArchitectureVerifier
from app.platform_verification.ai_health_monitoring.metrics.ai_metrics_collector_verifier import AIMetricsCollectorVerifier
from app.platform_verification.ai_health_monitoring.dashboards.ai_dashboard_verifier import AIDashboardVerifier
from app.platform_verification.ai_health_monitoring.logging.ai_logging_verifier import AILoggingVerifier
from app.platform_verification.ai_health_monitoring.tracing.ai_tracing_verifier import AITracingVerifier
from app.platform_verification.ai_health_monitoring.alerting.ai_alerting_verifier import AIAlertingVerifier
from app.platform_verification.ai_health_monitoring.slo.ai_slo_monitoring_verifier import AISLOMonitoringVerifier
from app.platform_verification.ai_health_monitoring.incidents.ai_incident_detector_verifier import AIIncidentDetectorVerifier
from app.platform_verification.ai_health_monitoring.automation.ai_automated_response_verifier import AIAutomatedResponseVerifier
from app.platform_verification.ai_health_monitoring.security.ai_monitoring_security_verifier import AIMonitoringSecurityVerifier
from app.platform_verification.ai_health_monitoring.scoring.ai_monitoring_quality_scorer import AIMonitoringQualityScorer
from app.platform_verification.ai_health_monitoring.exporter.ai_monitoring_evidence_exporter import AIMonitoringEvidenceExporter


class AIHealthMonitoringRuntime:
    """Master Orchestrator for Phase 3H.3.9 AI Health Monitoring Integration Verification."""

    def __init__(self, export_dir: Optional[str] = None):
        self.arch_verifier = AIObservabilityArchitectureVerifier()
        self.metrics_verifier = AIMetricsCollectorVerifier()
        self.dashboard_verifier = AIDashboardVerifier()
        self.logging_verifier = AILoggingVerifier()
        self.tracing_verifier = AITracingVerifier()
        self.alerting_verifier = AIAlertingVerifier()
        self.slo_verifier = AISLOMonitoringVerifier()
        self.incident_verifier = AIIncidentDetectorVerifier()
        self.automation_verifier = AIAutomatedResponseVerifier()
        self.security_verifier = AIMonitoringSecurityVerifier()
        self.scorer = AIMonitoringQualityScorer()
        self.exporter = AIMonitoringEvidenceExporter(output_dir=export_dir)

    def run_full_verification(self) -> Dict[str, Any]:
        """Executes full verification across all AI observability dimensions and exports manifests."""
        arch_rep = self.arch_verifier.verify_architecture()
        metrics_rep = self.metrics_verifier.verify_metrics_collection()
        dash_rep = self.dashboard_verifier.verify_dashboards()
        log_rep = self.logging_verifier.verify_logging()
        trace_rep = self.tracing_verifier.verify_tracing()
        alert_rep = self.alerting_verifier.verify_alerting()
        slo_rep = self.slo_verifier.verify_slos()
        inc_rep = self.incident_verifier.verify_incident_detection()
        auto_rep = self.automation_verifier.verify_automated_response()
        sec_rep = self.security_verifier.verify_security()

        scorecard = self.scorer.compute_scorecard(
            arch_report=arch_rep,
            metrics_report=metrics_rep,
            dashboard_report=dash_rep,
            logging_report=log_rep,
            tracing_report=trace_rep,
            alerting_report=alert_rep,
            slo_report=slo_rep,
            incident_report=inc_rep,
            automation_report=auto_rep,
            security_report=sec_rep,
        )

        manifests = self.exporter.export_all(
            arch_report=arch_rep,
            metrics_report=metrics_rep,
            dashboard_report=dash_rep,
            logging_report=log_rep,
            tracing_report=trace_rep,
            alerting_report=alert_rep,
            slo_report=slo_rep,
            incident_report=inc_rep,
            scorecard=scorecard,
        )

        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "architecture_report": arch_rep,
            "metrics_report": metrics_rep,
            "dashboard_report": dash_rep,
            "logging_report": log_rep,
            "tracing_report": trace_rep,
            "alerting_report": alert_rep,
            "slo_report": slo_rep,
            "incident_report": inc_rep,
            "automation_report": auto_rep,
            "security_report": sec_rep,
            "scorecard": scorecard,
            "exported_manifests": manifests,
            "passed": scorecard.passed,
        }
