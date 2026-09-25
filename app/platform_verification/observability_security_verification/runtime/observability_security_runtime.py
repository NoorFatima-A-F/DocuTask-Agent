"""
Phase 3H.4.10: Observability Security Verification Runtime
"""
from typing import Dict, Any
from ..verifiers import (
    DataClassificationVerifier,
    LogSecurityVerifier,
    LogSanitizationVerifier,
    MetricSecurityVerifier,
    TraceSecurityVerifier,
    DashboardAccessVerifier,
    AlertSecurityVerifier,
    PipelineSecurityVerifier,
    AISecurityVerifier,
    SecurityFailureSimulator,
)
from ..scoring.observability_security_scorer import ObservabilitySecurityScorer
from ..exporter.observability_security_exporter import ObservabilitySecurityExporter


class ObservabilitySecurityRuntime:
    def __init__(self):
        self.classification_verifier = DataClassificationVerifier()
        self.log_sec_verifier = LogSecurityVerifier()
        self.sanitization_verifier = LogSanitizationVerifier()
        self.metric_verifier = MetricSecurityVerifier()
        self.trace_verifier = TraceSecurityVerifier()
        self.dashboard_verifier = DashboardAccessVerifier()
        self.alert_verifier = AlertSecurityVerifier()
        self.pipeline_verifier = PipelineSecurityVerifier()
        self.ai_verifier = AISecurityVerifier()
        self.failure_simulator = SecurityFailureSimulator()
        self.scorer = ObservabilitySecurityScorer()
        self.exporter = ObservabilitySecurityExporter()

    def run_all_verifications(self, output_dir: str = "observability_security_verification") -> Dict[str, Any]:
        classification_report = self.classification_verifier.verify_data_classification()
        log_report = self.log_sec_verifier.scan_logs_for_sensitive_data()
        sanitization_report = self.sanitization_verifier.verify_sanitization_middleware()
        metric_report = self.metric_verifier.audit_metrics_privacy()
        trace_report = self.trace_verifier.audit_trace_security()
        access_report = self.dashboard_verifier.verify_dashboard_rbac()
        alert_report = self.alert_verifier.audit_alert_payloads()
        pipeline_report = self.pipeline_verifier.verify_pipeline_and_storage_security()
        ai_report = self.ai_verifier.audit_ai_telemetry_security()
        simulations = self.failure_simulator.simulate_security_failure_injections()

        scorecard = self.scorer.calculate_scorecard(
            classification_report=classification_report,
            log_report=log_report,
            metric_report=metric_report,
            trace_report=trace_report,
            access_report=access_report,
            pipeline_report=pipeline_report,
            ai_report=ai_report,
        )

        exported_files = self.exporter.export_evidence_manifests(
            output_dir=output_dir,
            classification_report=classification_report,
            log_report=log_report,
            sanitization_report=sanitization_report,
            metric_report=metric_report,
            trace_report=trace_report,
            access_report=access_report,
            alert_report=alert_report,
            pipeline_report=pipeline_report,
            ai_report=ai_report,
            simulations=simulations,
            scorecard=scorecard,
        )

        return {
            "scorecard": scorecard,
            "exported_files": exported_files,
            "classification": classification_report,
            "log_security": log_report,
            "sanitization": sanitization_report,
            "metric_security": metric_report,
            "trace_security": trace_report,
            "dashboard_access": access_report,
            "alert_security": alert_report,
            "pipeline_security": pipeline_report,
            "ai_security": ai_report,
            "simulations": simulations,
        }
