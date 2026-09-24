"""Governance Analytics Developer SDK Client."""

from typing import Dict, Any, List, Optional

from ..events.normalizers import GovernanceAnalyticsEvent, AnalyticsEventType
from ..events.consumer import GovernanceEventConsumer
from ..warehouse.repositories import GovernanceDataWarehouseRepository
from ..core.engine import GovernanceMetricsEngine
from ..risk.analyzer import RiskAnalyzer, RiskAnalysisSummary
from ..risk.trends import RiskTrendAnalyzer, RiskTrendSignal
from ..compliance.evaluator import ComplianceEvaluator
from ..compliance.reports import ComplianceReportingEngine, AuditReadinessReport
from ..policies.analytics import PolicyAnalyticsEngine, PolicyIntelligenceReport
from ..policies.effectiveness import PolicyEffectivenessEngine
from ..ai_systems.agents import AgentAnalyticsEngine
from ..ai_systems.models import ModelAnalyticsEngine
from ..ai_systems.workflows import WorkflowAnalyticsEngine
from ..reporting.templates import ReportType, ReportFormat
from ..reporting.generator import ReportGenerator
from ..reporting.exporters import ReportExporter
from ..dashboards.schemas import ExecutiveDashboardDTO, AdministratorDashboardDTO, DeveloperDashboardDTO
from ..dashboards.services import DashboardService
from ..alerts.detector import AlertDetector, AlertEvent


class GovernanceAnalyticsSDK:
    """Unified Python SDK Client for enterprise AI governance intelligence and reporting."""

    def __init__(
        self,
        repository: Optional[GovernanceDataWarehouseRepository] = None,
    ):
        self.repo = repository or GovernanceDataWarehouseRepository()
        self.consumer = GovernanceEventConsumer()
        # Automatically pipe ingested events into the warehouse
        self.consumer.subscribe(self.repo.insert_event)

        self.metrics = GovernanceMetricsEngine(self.repo)
        self.risk = RiskAnalyzer(self.repo)
        self.risk_trends = RiskTrendAnalyzer(self.repo)
        self.compliance_eval = ComplianceEvaluator(self.repo)
        self.compliance_rep = ComplianceReportingEngine(self.compliance_eval)
        self.policy_analytics = PolicyAnalyticsEngine(self.repo)
        self.policy_effectiveness = PolicyEffectivenessEngine(self.repo)
        self.agent_analytics = AgentAnalyticsEngine(self.repo)
        self.model_analytics = ModelAnalyticsEngine(self.repo)
        self.workflow_analytics = WorkflowAnalyticsEngine(self.repo)
        self.reports = ReportGenerator(
            metrics_engine=self.metrics,
            risk_analyzer=self.risk,
            compliance_engine=self.compliance_rep,
            policy_engine=self.policy_effectiveness,
        )
        self.dashboards = DashboardService(
            metrics_engine=self.metrics,
            risk_analyzer=self.risk,
            compliance_engine=self.compliance_rep,
            policy_engine=self.policy_effectiveness,
        )
        self.alerts = AlertDetector(metrics_engine=self.metrics, risk_analyzer=self.risk)

    def ingest_event(self, event: Any, event_type: Optional[AnalyticsEventType] = None) -> GovernanceAnalyticsEvent:
        """Ingests a governance event into analytics pipelines."""
        return self.consumer.ingest(event, event_type=event_type)

    def get_governance_score(self, tenant_id: str = "*") -> float:
        return self.metrics.calculate_governance_score(tenant_id)

    def get_overview(self, tenant_id: str = "*") -> Dict[str, Any]:
        return {
            "tenant_id": tenant_id,
            "governance_score": self.get_governance_score(tenant_id),
            "decisions": self.metrics.get_decision_metrics(tenant_id).model_dump(),
            "risk_summary": self.risk.analyze_risk_posture(tenant_id).model_dump(),
            "compliance_status": self.compliance_rep.generate_audit_readiness_report(tenant_id).audit_readiness_status,
        }

    def get_risk_posture(self, tenant_id: str = "*") -> RiskAnalysisSummary:
        return self.risk.analyze_risk_posture(tenant_id)

    def get_risk_trends(self, tenant_id: str = "*") -> List[RiskTrendSignal]:
        return self.risk_trends.detect_trend_signals(tenant_id)

    def get_compliance_report(self, tenant_id: str = "*") -> AuditReadinessReport:
        return self.compliance_rep.generate_audit_readiness_report(tenant_id)

    def get_policy_intelligence(self, tenant_id: str = "*") -> PolicyIntelligenceReport:
        return self.policy_analytics.generate_policy_intelligence(tenant_id)

    def get_executive_dashboard(self, tenant_id: str = "*") -> ExecutiveDashboardDTO:
        return self.dashboards.get_executive_dashboard(tenant_id)

    def get_admin_dashboard(self, tenant_id: str = "*") -> AdministratorDashboardDTO:
        return self.dashboards.get_administrator_dashboard(tenant_id)

    def get_developer_dashboard(self, tenant_id: str = "*") -> DeveloperDashboardDTO:
        return self.dashboards.get_developer_dashboard(tenant_id)

    def generate_report(
        self,
        report_type: ReportType = ReportType.MONTHLY_EXECUTIVE,
        tenant_id: str = "*",
        title: Optional[str] = None,
        export_format: ReportFormat = ReportFormat.JSON,
    ) -> str:
        rep = self.reports.generate_report(report_type=report_type, tenant_id=tenant_id, title=title)
        return ReportExporter.export(rep, format=export_format)

    def evaluate_alerts(self, tenant_id: str = "*") -> List[AlertEvent]:
        return self.alerts.evaluate_alerts(tenant_id)
