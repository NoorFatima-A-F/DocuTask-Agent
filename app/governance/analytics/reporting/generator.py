"""Report Generator compiling governance metrics, risk posture, and compliance findings."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid

from .templates import ReportType, GovernanceReport, GovernanceReportSection
from ..core.engine import GovernanceMetricsEngine
from ..risk.analyzer import RiskAnalyzer
from ..compliance.reports import ComplianceReportingEngine
from ..policies.effectiveness import PolicyEffectivenessEngine


class ReportGenerator:
    """Generates structured governance intelligence reports."""

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

    def generate_report(self, report_type: ReportType, tenant_id: str = "*", title: Optional[str] = None) -> GovernanceReport:
        gov_score = self.metrics.calculate_governance_score(tenant_id=tenant_id)
        dec_metrics = self.metrics.get_decision_metrics(tenant_id=tenant_id)
        risk_summary = self.risk.analyze_risk_posture(tenant_id=tenant_id)
        comp_summary = self.compliance.generate_audit_readiness_report(tenant_id=tenant_id)
        pol_summary = self.policy.evaluate_effectiveness(tenant_id=tenant_id)

        sections: List[GovernanceReportSection] = []

        if report_type == ReportType.DAILY_OPERATIONAL:
            rep_title = title or f"Daily Governance Operations Report ({datetime.now(timezone.utc).strftime('%Y-%m-%d')})"
            exec_summary = f"Total Decisions: {dec_metrics.total_decisions}, Allow Rate: {dec_metrics.allow_rate*100:.1f}%, Active Policies: {self.metrics.get_policy_metrics(tenant_id).active_policies_count}."
            sections.append(
                GovernanceReportSection(
                    title="Operational Decisions & Controls",
                    summary_text="Overview of runtime controls, authorizations, and manual review volume.",
                    metrics=dec_metrics.model_dump(),
                    key_findings=[
                        f"Autonomous execution rate maintained at {dec_metrics.allow_rate*100:.1f}%.",
                        f"{dec_metrics.approval_required_count} reviews submitted for human oversight.",
                    ],
                )
            )

        elif report_type == ReportType.RISK_ASSESSMENT:
            rep_title = title or "Enterprise AI Risk Assessment & Threat Analysis Report"
            exec_summary = f"Overall Risk Score: {risk_summary.overall_risk_score:.2f} ({risk_summary.enterprise_risk_level}). Critical Events: {risk_summary.critical_risk_events_count}."
            sections.append(
                GovernanceReportSection(
                    title="Risk Category Breakdown",
                    summary_text="Multi-factor evaluation across security, privacy, model, and compliance vectors.",
                    metrics=risk_summary.category_scores,
                    key_findings=risk_summary.risk_anomalies_detected or ["No critical risk anomalies detected."],
                    recommendations=["Ensure regular red-teaming reviews for high-exposure entities."],
                )
            )

        elif report_type == ReportType.COMPLIANCE_AUDIT:
            rep_title = title or "Regulatory AI Compliance & Audit Readiness Report"
            exec_summary = f"Audit Readiness Score: {comp_summary.overall_readiness_score:.1f}% ({comp_summary.audit_readiness_status}). Frameworks evaluated: SOC 2, ISO 27001, GDPR, HIPAA, EU AI Act."
            sections.append(
                GovernanceReportSection(
                    title="Framework Adherence & Controls",
                    summary_text="Control coverage and evidence preservation metrics.",
                    metrics={fw: fs.score for fw, fs in comp_summary.framework_scores.items()},
                    key_findings=[f"{len(comp_summary.identified_gaps)} compliance control gaps identified."] if comp_summary.identified_gaps else ["All evaluated regulatory controls are in compliance."],
                    recommendations=[g.remediation_step for g in comp_summary.identified_gaps] if comp_summary.identified_gaps else ["Maintain continuous evidence preservation."],
                )
            )

        else:  # MONTHLY_EXECUTIVE or WEEKLY_SUMMARY
            rep_title = title or "Executive AI Governance Intelligence & Health Report"
            exec_summary = f"Composite AI Governance Score: {gov_score}/100. Overall Enterprise Risk: {risk_summary.enterprise_risk_level}. Compliance Posture: {comp_summary.audit_readiness_status}."
            sections.append(
                GovernanceReportSection(
                    title="Governance Health & Risk Overview",
                    summary_text="High-level governance score and risk category summary.",
                    metrics={"governance_score": gov_score, "overall_risk": risk_summary.overall_risk_score},
                    key_findings=[f"Enterprise governance index stands at {gov_score}/100."],
                )
            )
            sections.append(
                GovernanceReportSection(
                    title="Policy Effectiveness & Friction",
                    summary_text="Evaluation of policy trigger frequency and human intervention rates.",
                    metrics={"effectiveness_score": pol_summary.overall_effectiveness_score, "false_positive_rate": pol_summary.false_positive_estimate_rate},
                    recommendations=[r.suggested_action for r in pol_summary.recommendations],
                )
            )

        return GovernanceReport(
            tenant_id=tenant_id,
            report_type=report_type,
            title=rep_title,
            executive_summary=exec_summary,
            governance_score=gov_score,
            sections=sections,
        )
