"""
Phase 3H.5.10: Health Security Runtime Orchestrator
"""
from typing import Dict, Any, Optional

from ..verifiers import (
    EndpointSecurityVerifier,
    HealthAuthorizationVerifier,
    MetricsPrivacyVerifier,
    LogSecurityVerifier,
    AlertSecurityVerifier,
    TraceSecurityVerifier,
    SecretScanVerifier,
    DashboardSecurityVerifier,
    SecurityFailureInjectionVerifier,
    ComplianceSecurityVerifier,
)
from ..scoring import HealthSecurityScorer
from ..exporter import HealthSecurityExporter
from ..domain.models import HealthSecurityScorecard


class HealthSecurityRuntime:
    """
    Main orchestrator for executing full Phase 3H.5.10 Health Security & Information Exposure Verification.
    """

    def __init__(
        self,
        output_dir: str = "health_security_verification",
        endpoint_verifier: Optional[EndpointSecurityVerifier] = None,
        auth_verifier: Optional[HealthAuthorizationVerifier] = None,
        metrics_verifier: Optional[MetricsPrivacyVerifier] = None,
        log_verifier: Optional[LogSecurityVerifier] = None,
        alert_verifier: Optional[AlertSecurityVerifier] = None,
        trace_verifier: Optional[TraceSecurityVerifier] = None,
        secret_verifier: Optional[SecretScanVerifier] = None,
        dashboard_verifier: Optional[DashboardSecurityVerifier] = None,
        injection_verifier: Optional[SecurityFailureInjectionVerifier] = None,
        compliance_verifier: Optional[ComplianceSecurityVerifier] = None,
        scorer: Optional[HealthSecurityScorer] = None,
        exporter: Optional[HealthSecurityExporter] = None,
    ):
        self.output_dir = output_dir
        self.endpoint_verifier = endpoint_verifier or EndpointSecurityVerifier()
        self.auth_verifier = auth_verifier or HealthAuthorizationVerifier()
        self.metrics_verifier = metrics_verifier or MetricsPrivacyVerifier()
        self.log_verifier = log_verifier or LogSecurityVerifier()
        self.alert_verifier = alert_verifier or AlertSecurityVerifier()
        self.trace_verifier = trace_verifier or TraceSecurityVerifier()
        self.secret_verifier = secret_verifier or SecretScanVerifier()
        self.dashboard_verifier = dashboard_verifier or DashboardSecurityVerifier()
        self.injection_verifier = injection_verifier or SecurityFailureInjectionVerifier()
        self.compliance_verifier = compliance_verifier or ComplianceSecurityVerifier()
        self.scorer = scorer or HealthSecurityScorer()
        self.exporter = exporter or HealthSecurityExporter(output_dir=self.output_dir)

    def run_full_verification(self) -> Dict[str, Any]:
        """
        Executes all 10 verifications, computes the scorecard, and exports evidence.
        """
        # Step 1: Execute all verifications
        ep_report = self.endpoint_verifier.verify_endpoint_security()
        auth_report = self.auth_verifier.verify_health_authorization()
        metrics_report = self.metrics_verifier.verify_metrics_privacy()
        log_report = self.log_verifier.verify_log_security()
        alert_report = self.alert_verifier.verify_alert_security()
        trace_report = self.trace_verifier.verify_trace_security()
        secret_report = self.secret_verifier.scan_secrets_across_observability()
        dashboard_report = self.dashboard_verifier.verify_dashboard_security()
        injection_report = self.injection_verifier.execute_security_failure_injection()
        compliance_report = self.compliance_verifier.verify_compliance_and_standards()

        # Step 2: Calculate overall scorecard
        scorecard: HealthSecurityScorecard = self.scorer.calculate_scorecard(
            endpoint_report=ep_report,
            auth_report=auth_report,
            metrics_report=metrics_report,
            log_report=log_report,
            alert_report=alert_report,
            trace_report=trace_report,
            secret_report=secret_report,
            dashboard_report=dashboard_report,
            injection_report=injection_report,
            compliance_report=compliance_report,
        )

        # Step 3: Export evidence files & SHA-256 metadata manifest
        exported_files = self.exporter.export_all(
            endpoint_report=ep_report,
            auth_report=auth_report,
            metrics_report=metrics_report,
            log_report=log_report,
            alert_report=alert_report,
            trace_report=trace_report,
            secret_report=secret_report,
            dashboard_report=dashboard_report,
            injection_report=injection_report,
            compliance_report=compliance_report,
            scorecard=scorecard,
        )

        return {
            "scorecard": scorecard,
            "endpoint_report": ep_report,
            "auth_report": auth_report,
            "metrics_report": metrics_report,
            "log_report": log_report,
            "alert_report": alert_report,
            "trace_report": trace_report,
            "secret_report": secret_report,
            "dashboard_report": dashboard_report,
            "injection_report": injection_report,
            "compliance_report": compliance_report,
            "exported_files": exported_files,
        }
