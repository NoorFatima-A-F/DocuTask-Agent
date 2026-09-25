"""
Enterprise Reporting Platform Runtime facade.
"""
from __future__ import annotations
from datetime import datetime, timezone
from app.platform_verification.reporting_audit.core.audit_export_manager import EnterpriseAuditExportManager
from app.platform_verification.reporting_audit.core.compliance_engine import EnterpriseComplianceMappingEngine
from app.platform_verification.reporting_audit.core.dashboard_engine import EnterpriseDashboardAggregationEngine
from app.platform_verification.reporting_audit.core.data_pipeline import EnterpriseReportingDataPipeline
from app.platform_verification.reporting_audit.core.notification_service import EnterpriseNotificationService
from app.platform_verification.reporting_audit.core.report_generator import EnterpriseAuditReportGenerator
from app.platform_verification.reporting_audit.domain.models import VerificationSummary


class EnterpriseReportingPlatformRuntime:
    """Unified runtime connecting data pipelines, report generators, compliance mappings, and dashboards."""

    def __init__(self):
        self.data_pipeline = EnterpriseReportingDataPipeline()
        self.report_generator = EnterpriseAuditReportGenerator()
        self.compliance_engine = EnterpriseComplianceMappingEngine()
        self.notification_service = EnterpriseNotificationService()
        self.export_manager = EnterpriseAuditExportManager(report_generator=self.report_generator)
        self.dashboard_engine = EnterpriseDashboardAggregationEngine(
            pipeline=self.data_pipeline,
            compliance_engine=self.compliance_engine,
        )
        self._seed_sample_summary()

    def _seed_sample_summary(self) -> None:
        self.data_pipeline.ingest_verification_run(
            VerificationSummary(
                execution_id="EXEC-SAMPLE-001",
                system_version="v2.4.0",
                model_version="gemini-1.5-pro",
                environment="STAGING",
                timestamp=datetime.now(timezone.utc).isoformat(),
                overall_score=96.2,
                certification_status="CERTIFIED",
                risk_level="LOW",
                total_tests=450,
                failed_tests_count=0,
                hallucination_rate=0.012,
                p95_latency_ms=380.0,
                critical_vulnerabilities=0,
            )
        )
