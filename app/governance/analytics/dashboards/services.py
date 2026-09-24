"""Dashboard Service constructing role-specific aggregation views."""

from typing import Optional
from .schemas import ExecutiveDashboardDTO, AdministratorDashboardDTO, DeveloperDashboardDTO
from ..core.engine import GovernanceMetricsEngine
from ..risk.analyzer import RiskAnalyzer
from ..compliance.reports import ComplianceReportingEngine
from ..policies.effectiveness import PolicyEffectivenessEngine


class DashboardService:
    """Aggregates and formats dashboard payloads for Executive, Admin, and Developer views."""

    def __init__(
        self,
        metrics_engine: Optional[GovernanceMetricsEngine] = None,
        risk_analyzer: Optional[RiskAnalyzer] = None,
        compliance_engine: Optional[ComplianceReportingEngine] = None,
        policy_engine: Optional[PolicyEffectivenessEngine] = None,
    ):
        self.metrics = metrics_engine or GovernanceMetricsEngine()
        self.risk = risk_analyzer or RiskAnalyzer(self.metrics.repo)
        self.compliance = compliance_engine or ComplianceReportingEngine()
        self.policy = policy_engine or PolicyEffectivenessEngine(self.metrics.repo)

    def get_executive_dashboard(self, tenant_id: str = "*") -> ExecutiveDashboardDTO:
        gov_score = self.metrics.calculate_governance_score(tenant_id=tenant_id)
        risk_summary = self.risk.analyze_risk_posture(tenant_id=tenant_id)
        comp_summary = self.compliance.generate_audit_readiness_report(tenant_id=tenant_id)
        pol_metrics = self.metrics.get_policy_metrics(tenant_id=tenant_id)
        model_metrics = self.metrics.get_model_metrics(tenant_id=tenant_id)
        agent_metrics = self.metrics.get_agent_metrics(tenant_id=tenant_id)

        fw_scores = {k: v.score for k, v in comp_summary.framework_scores.items()}

        return ExecutiveDashboardDTO(
            tenant_id=tenant_id,
            overall_governance_score=gov_score,
            enterprise_risk_level=risk_summary.enterprise_risk_level,
            overall_risk_score=risk_summary.overall_risk_score,
            compliance_status=comp_summary.audit_readiness_status,
            ai_adoption_total_executions=agent_metrics.total_agent_executions + model_metrics.total_model_invocations,
            total_cost_usd=model_metrics.total_cost_usd,
            major_incidents_count=risk_summary.critical_risk_events_count,
            policy_health_score=pol_metrics.policy_effectiveness_score,
            approval_completion_rate=agent_metrics.agent_approval_rate,
            category_risk_scores=risk_summary.category_scores,
            framework_compliance_scores=fw_scores,
        )

    def get_administrator_dashboard(self, tenant_id: str = "*") -> AdministratorDashboardDTO:
        dec_metrics = self.metrics.get_decision_metrics(tenant_id=tenant_id)
        pol_metrics = self.metrics.get_policy_metrics(tenant_id=tenant_id)
        risk_summary = self.risk.analyze_risk_posture(tenant_id=tenant_id)
        comp_summary = self.compliance.generate_audit_readiness_report(tenant_id=tenant_id)
        model_metrics = self.metrics.get_model_metrics(tenant_id=tenant_id)

        return AdministratorDashboardDTO(
            tenant_id=tenant_id,
            total_policy_violations=pol_metrics.total_policy_violations,
            most_triggered_policies=pol_metrics.most_triggered_policies,
            critical_risk_events_count=risk_summary.critical_risk_events_count,
            blocked_actions_count=dec_metrics.blocked_actions,
            pending_approvals_count=dec_metrics.approval_required_count,
            failed_evaluations_count=model_metrics.model_failure_count,
            audit_findings_count=len(comp_summary.identified_gaps),
            decisions=dec_metrics,
            policies=pol_metrics,
        )

    def get_developer_dashboard(self, tenant_id: str = "*") -> DeveloperDashboardDTO:
        agent_metrics = self.metrics.get_agent_metrics(tenant_id=tenant_id)
        model_metrics = self.metrics.get_model_metrics(tenant_id=tenant_id)
        prompt_metrics = self.metrics.get_prompt_metrics(tenant_id=tenant_id)

        fail_rate = (agent_metrics.failed_agent_executions / agent_metrics.total_agent_executions) if agent_metrics.total_agent_executions > 0 else 0.0

        return DeveloperDashboardDTO(
            tenant_id=tenant_id,
            agent_executions_count=agent_metrics.total_agent_executions,
            agent_failure_rate=round(fail_rate, 4),
            avg_model_latency_ms=model_metrics.avg_latency_ms,
            avg_prompt_evaluation_score=prompt_metrics.avg_evaluation_score,
            model_drift_signals_count=model_metrics.model_drift_signals_count,
            workflow_failures_count=model_metrics.model_failure_count,
            agents=agent_metrics,
            models=model_metrics,
            prompts=prompt_metrics,
        )
