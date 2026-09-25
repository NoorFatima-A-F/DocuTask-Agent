"""
Runtime Orchestrator for Part 3I: Enterprise Observability Infrastructure (Logging & Metrics)
"""
from typing import Dict, Any
from ..logging_verifiers.logging_architecture_verifier import LoggingArchitectureVerifier
from ..logging_verifiers.structured_logging_verifier import StructuredLoggingVerifier
from ..logging_verifiers.correlation_verifier import CorrelationVerifier
from ..logging_verifiers.ai_workflow_logging_verifier import AIWorkflowLoggingVerifier
from ..logging_verifiers.security_scan_verifier import SecurityScanVerifier
from ..logging_verifiers.log_retention_verifier import LogRetentionVerifier
from ..logging_verifiers.log_performance_verifier import LogPerformanceVerifier
from ..metrics_verifiers.metrics_architecture_verifier import MetricsArchitectureVerifier
from ..metrics_verifiers.golden_signals_verifier import GoldenSignalsVerifier
from ..metrics_verifiers.app_infra_metrics_verifier import AppInfraMetricsVerifier
from ..metrics_verifiers.sli_slo_verifier import SLISLOVerifier
from ..metrics_verifiers.alerting_verifier import AlertingVerifier
from ..metrics_verifiers.dashboard_verifier import DashboardVerifier
from ..metrics_verifiers.metrics_performance_verifier import MetricsPerformanceVerifier
from ..scoring.logging_quality_scorer import LoggingQualityScorer
from ..scoring.metrics_quality_scorer import MetricsQualityScorer
from ..scoring.observability_composite_scorer import ObservabilityCompositeScorer
from ..exporter.observability_exporter import ObservabilityExporter


class ObservabilityRuntime:
    """
    Executes both Part 3I.1 (Logging) and Part 3I.2 (Metrics) verification pipelines, computes dual scores, and exports signed manifests.
    """

    def __init__(self):
        # Logging Verifiers
        self.log_arch = LoggingArchitectureVerifier()
        self.log_struct = StructuredLoggingVerifier()
        self.log_corr = CorrelationVerifier()
        self.log_ai = AIWorkflowLoggingVerifier()
        self.log_sec = SecurityScanVerifier()
        self.log_ret = LogRetentionVerifier()
        self.log_perf = LogPerformanceVerifier()

        # Metrics Verifiers
        self.met_arch = MetricsArchitectureVerifier()
        self.met_golden = GoldenSignalsVerifier()
        self.met_app_infra = AppInfraMetricsVerifier()
        self.met_sli = SLISLOVerifier()
        self.met_alert = AlertingVerifier()
        self.met_dash = DashboardVerifier()
        self.met_perf = MetricsPerformanceVerifier()

        # Scorers & Exporter
        self.log_scorer = LoggingQualityScorer()
        self.met_scorer = MetricsQualityScorer()
        self.composite_scorer = ObservabilityCompositeScorer()
        self.exporter = ObservabilityExporter()

    def run_full_verification(self, export_base_dir: str = "observability_verification") -> Dict[str, Any]:
        # 1. Execute Logging Verifiers
        arch_report = self.log_arch.verify_logging_architecture()
        struct_report = self.log_struct.verify_structured_logging()
        corr_report = self.log_corr.verify_correlation()
        ai_log_report = self.log_ai.verify_ai_workflow_logging()
        sec_report = self.log_sec.verify_security_scanning()
        ret_report = self.log_ret.verify_retention()
        log_perf_report = self.log_perf.verify_log_performance()

        logging_cert = self.log_scorer.calculate_logging_score(
            arch_report=arch_report,
            struct_report=struct_report,
            corr_report=corr_report,
            ai_report=ai_log_report,
            sec_report=sec_report,
            ret_report=ret_report,
            perf_report=log_perf_report,
        )

        logging_payloads = {
            "logging_architecture_report.json": arch_report.model_dump(mode="json"),
            "structured_logging_report.json": struct_report.model_dump(mode="json"),
            "correlation_report.json": corr_report.model_dump(mode="json"),
            "ai_workflow_logging_report.json": ai_log_report.model_dump(mode="json"),
            "security_scan_report.json": sec_report.model_dump(mode="json"),
            "retention_report.json": ret_report.model_dump(mode="json"),
            "performance_report.json": log_perf_report.model_dump(mode="json"),
        }

        # 2. Execute Metrics Verifiers
        inv_report = self.met_arch.verify_metrics_architecture()
        golden_report = self.met_golden.verify_golden_signals()
        app_infra_report = self.met_app_infra.verify_app_infra_metrics()
        sli_report = self.met_sli.verify_sli_slo()
        alert_report = self.met_alert.verify_alerting()
        dash_report = self.met_dash.verify_dashboards()
        met_perf_report = self.met_perf.verify_metrics_performance()

        metrics_cert = self.met_scorer.calculate_metrics_score(
            inventory_report=inv_report,
            golden_report=golden_report,
            app_infra_report=app_infra_report,
            sli_report=sli_report,
            alert_report=alert_report,
            dash_report=dash_report,
            perf_report=met_perf_report,
        )

        metrics_payloads = {
            "metric_inventory.json": inv_report.model_dump(mode="json"),
            "golden_signals_report.json": golden_report.model_dump(mode="json"),
            "app_infra_metrics_report.json": app_infra_report.model_dump(mode="json"),
            "sli_slo_report.json": sli_report.model_dump(mode="json"),
            "alert_report.json": alert_report.model_dump(mode="json"),
            "dashboard_report.json": dash_report.model_dump(mode="json"),
            "performance_report.json": met_perf_report.model_dump(mode="json"),
        }

        # 3. Compute Composite Certification
        unified_cert = self.composite_scorer.calculate_unified_certification(
            logging_cert=logging_cert,
            metrics_cert=metrics_cert,
        )

        # 4. Export Artifacts
        manifest_meta = self.exporter.export_all_observability_reports(
            base_dir=export_base_dir,
            logging_reports=logging_payloads,
            logging_cert=logging_cert,
            metrics_reports=metrics_payloads,
            metrics_cert=metrics_cert,
            unified_cert=unified_cert,
        )

        return {
            "logging": {
                "reports": logging_payloads,
                "certification": logging_cert,
            },
            "metrics": {
                "reports": metrics_payloads,
                "certification": metrics_cert,
            },
            "unified_certification": unified_cert,
            "metadata": manifest_meta,
        }
