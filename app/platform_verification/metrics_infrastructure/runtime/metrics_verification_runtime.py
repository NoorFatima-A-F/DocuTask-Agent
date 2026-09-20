"""
Phase 3I.3: Runtime Orchestrator for Enterprise Metrics Infrastructure Verification
"""
from typing import Dict, Any
from ..domain.models import (
    MetricsArchitectureReport,
    MetricsStandardReport,
    ApplicationMetricsReport,
    AIMetricsReport,
    InfrastructureMetricsReport,
    BusinessSLAMetricsReport,
    DashboardReport,
    AlertValidationReport,
    MetricsAccuracyReport,
    MetricsSecurityReport,
    MetricsPerformanceReport,
    ChaosMetricReport,
    MetricsCertificationReport,
)
from ..verifiers.metrics_architecture_verifier import MetricsArchitectureVerifier
from ..verifiers.metrics_standard_verifier import MetricsStandardVerifier
from ..verifiers.application_metrics_verifier import ApplicationMetricsVerifier
from ..verifiers.ai_metrics_verifier import AIMetricsVerifier
from ..verifiers.infrastructure_metrics_verifier import InfrastructureMetricsVerifier
from ..verifiers.business_sla_metrics_verifier import BusinessSLAMetricsVerifier
from ..verifiers.metrics_dashboard_verifier import MetricsDashboardVerifier
from ..verifiers.alert_metric_verifier import AlertMetricVerifier
from ..verifiers.metrics_accuracy_verifier import MetricsAccuracyVerifier
from ..verifiers.metrics_security_verifier import MetricsSecurityVerifier
from ..verifiers.metrics_performance_verifier import MetricsPerformanceVerifier
from ..verifiers.failure_simulation_metrics_verifier import FailureSimulationMetricsVerifier
from ..scoring.metrics_quality_scorer import MetricsQualityScorer
from ..exporter.metrics_evidence_exporter import MetricsEvidenceExporter


class MetricsVerificationRuntime:
    """
    Orchestrates all Phase 3I.3 metrics verification engines, executes 6-pillar quality scoring, and exports signed evidence manifests.
    """

    def __init__(self):
        self.arch_verifier = MetricsArchitectureVerifier()
        self.std_verifier = MetricsStandardVerifier()
        self.app_verifier = ApplicationMetricsVerifier()
        self.ai_verifier = AIMetricsVerifier()
        self.infra_verifier = InfrastructureMetricsVerifier()
        self.biz_verifier = BusinessSLAMetricsVerifier()
        self.dash_verifier = MetricsDashboardVerifier()
        self.alert_verifier = AlertMetricVerifier()
        self.acc_verifier = MetricsAccuracyVerifier()
        self.sec_verifier = MetricsSecurityVerifier()
        self.perf_verifier = MetricsPerformanceVerifier()
        self.chaos_verifier = FailureSimulationMetricsVerifier()
        self.scorer = MetricsQualityScorer()
        self.exporter = MetricsEvidenceExporter()

    def run_full_verification(self, export_dir: str = "observability_verification/metrics") -> Dict[str, Any]:
        arch_report: MetricsArchitectureReport = self.arch_verifier.verify_metrics_architecture()
        std_report: MetricsStandardReport = self.std_verifier.verify_metrics_standard()
        app_report: ApplicationMetricsReport = self.app_verifier.verify_application_metrics()
        ai_report: AIMetricsReport = self.ai_verifier.verify_ai_metrics()
        infra_report: InfrastructureMetricsReport = self.infra_verifier.verify_infrastructure_metrics()
        biz_report: BusinessSLAMetricsReport = self.biz_verifier.verify_business_sla_metrics()
        dash_report: DashboardReport = self.dash_verifier.verify_dashboards()
        alert_report: AlertValidationReport = self.alert_verifier.verify_alert_metrics()
        acc_report: MetricsAccuracyReport = self.acc_verifier.verify_metrics_accuracy()
        sec_report: MetricsSecurityReport = self.sec_verifier.verify_metrics_security()
        perf_report: MetricsPerformanceReport = self.perf_verifier.verify_metrics_performance()
        chaos_report: ChaosMetricReport = self.chaos_verifier.verify_failure_simulation_metrics()

        certification_report: MetricsCertificationReport = self.scorer.calculate_certification_score(
            arch_report=arch_report,
            std_report=std_report,
            app_report=app_report,
            ai_report=ai_report,
            infra_report=infra_report,
            biz_report=biz_report,
            dash_report=dash_report,
            alert_report=alert_report,
            acc_report=acc_report,
            sec_report=sec_report,
            perf_report=perf_report,
            chaos_report=chaos_report,
        )

        metadata = self.exporter.export_all_reports(
            output_dir=export_dir,
            arch_report=arch_report,
            std_report=std_report,
            app_report=app_report,
            ai_report=ai_report,
            infra_report=infra_report,
            biz_report=biz_report,
            dash_report=dash_report,
            alert_report=alert_report,
            acc_report=acc_report,
            sec_report=sec_report,
            perf_report=perf_report,
            chaos_report=chaos_report,
            certification_report=certification_report,
        )

        return {
            "arch_report": arch_report,
            "std_report": std_report,
            "app_report": app_report,
            "ai_report": ai_report,
            "infra_report": infra_report,
            "biz_report": biz_report,
            "dash_report": dash_report,
            "alert_report": alert_report,
            "acc_report": acc_report,
            "sec_report": sec_report,
            "perf_report": perf_report,
            "chaos_report": chaos_report,
            "certification_report": certification_report,
            "metadata": metadata,
        }
