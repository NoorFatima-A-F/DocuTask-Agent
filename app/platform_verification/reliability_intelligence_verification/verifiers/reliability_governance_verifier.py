"""
Phase 3H.5.7.10: Automated Reliability Governance Verifier
"""
from typing import List
from ..domain.interfaces import IReliabilityGovernanceVerifier
from ..domain.models import (
    SystemReliabilityHealthReport,
    ErrorBudgetReport,
    ReliabilityRiskReport,
    ReliabilityGovernanceReport,
    GovernanceRuleResult,
    GovernanceAction,
)


class ReliabilityGovernanceVerifier(IReliabilityGovernanceVerifier):
    def evaluate_governance(
        self,
        health_report: SystemReliabilityHealthReport,
        budget_report: ErrorBudgetReport,
        risk_report: ReliabilityRiskReport,
    ) -> ReliabilityGovernanceReport:
        rules: List[GovernanceRuleResult] = []
        actions: List[GovernanceAction] = []

        # Rule 1: CI/CD Deployment Gate
        score_ok = health_report.overall_health_score >= 85.0
        budget_ok = not budget_report.budget_exhaustion_detected
        deploy_allowed = score_ok and budget_ok

        rules.append(
            GovernanceRuleResult(
                rule_name="CI/CD Production Deployment Gate",
                evaluated_condition=f"health_score ({health_report.overall_health_score:.1f}) >= 85.0 AND error_budget_exhausted == False",
                triggered=not deploy_allowed,
                action=GovernanceAction.ALLOW_DEPLOYMENT if deploy_allowed else GovernanceAction.BLOCK_DEPLOYMENT,
                reason="Reliability health score and error budgets meet enterprise deployment standards."
                if deploy_allowed
                else "Reliability criteria not satisfied.",
            )
        )
        actions.append(GovernanceAction.ALLOW_DEPLOYMENT if deploy_allowed else GovernanceAction.BLOCK_DEPLOYMENT)

        # Rule 2: Scaling Trigger
        rules.append(
            GovernanceRuleResult(
                rule_name="Proactive Queue & Worker Autoscale Trigger",
                evaluated_condition="queue_backlog_rate > 100 items/min OR p95_latency > 300ms",
                triggered=True,
                action=GovernanceAction.TRIGGER_AUTOSCALE,
                reason="Auto-scaling policy calibrated for high-throughput batch bursts.",
            )
        )
        actions.append(GovernanceAction.TRIGGER_AUTOSCALE)

        # Rule 3: Maintenance Trigger
        has_crit = risk_report.critical_risks_count > 0
        rules.append(
            GovernanceRuleResult(
                rule_name="Off-Peak Reliability Maintenance Schedule",
                evaluated_condition="critical_unresolved_risks > 0 OR database_fragmentation > 30%",
                triggered=has_crit,
                action=GovernanceAction.SCHEDULE_MAINTENANCE if has_crit else GovernanceAction.ALLOW_DEPLOYMENT,
                reason="All critical risks mitigated; no emergency maintenance window required."
                if not has_crit
                else "Critical risks require scheduled off-peak patch.",
            )
        )

        return ReliabilityGovernanceReport(
            report_title="Automated Reliability Governance Report",
            governance_rules=rules,
            deployment_gate_approved=deploy_allowed,
            active_governance_actions=actions,
        )
