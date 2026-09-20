"""
Phase 3I.5: 6-Pillar Enterprise Alerting & Incident Detection Quality Scorer
"""
from typing import List
from datetime import datetime, timezone
from ..domain.models import (
    AlertCertificationTier,
    AlertingArchitectureReport,
    AlertSignalCoverageReport,
    AlertRulesReport,
    AIAgentAlertReport,
    IncidentSeverityReport,
    RemediationReport,
    AlertSecurityReport,
    AlertTestingReport,
    AlertingPillarScore,
    AlertingCertificationReport,
)
from ..domain.interfaces import IAlertingQualityScorer


class AlertingQualityScorer(IAlertingQualityScorer):
    """
    Evaluates 6 core incident detection categories:
      - Detection coverage: 20%
      - Alert accuracy: 20%
      - AI-specific monitoring: 20%
      - Incident routing: 15%
      - Automation capability: 15%
      - Security: 10%
    """

    def calculate_certification_score(
        self,
        arch_report: AlertingArchitectureReport,
        signal_report: AlertSignalCoverageReport,
        rule_report: AlertRulesReport,
        ai_report: AIAgentAlertReport,
        routing_report: IncidentSeverityReport,
        remediation_report: RemediationReport,
        sec_report: AlertSecurityReport,
        testing_report: AlertTestingReport,
    ) -> AlertingCertificationReport:
        # 1. Detection Coverage (20%)
        cov_valid = (arch_report.monitored_services >= 8) and signal_report.multi_signal_correlation_active and (signal_report.overall_signal_coverage_pct >= 95.0)
        cov_score = signal_report.overall_signal_coverage_pct if cov_valid else 0.0
        cov_weight = 20.0
        cov_weighted = (cov_score * cov_weight) / 100.0

        # 2. Alert Accuracy & Golden Signals (20%)
        acc_valid = rule_report.alert_rules_compliant and rule_report.duration_window_enforced and testing_report.all_tests_passed
        acc_score = 100.0 if acc_valid else 0.0
        acc_weight = 20.0
        acc_weighted = (acc_score * acc_weight) / 100.0

        # 3. AI-Specific Monitoring (20%)
        ai_valid = (ai_report.ai_alerting_coverage_score >= 95.0) and ai_report.agent_retry_explosion_detection and ai_report.planning_failure_detection
        ai_score = ai_report.ai_alerting_coverage_score if ai_valid else 0.0
        ai_weight = 20.0
        ai_weighted = (ai_score * ai_weight) / 100.0

        # 4. Incident Routing & Severity (15%)
        rout_valid = (routing_report.routing_accuracy_pct >= 95.0) and len(routing_report.routing_table) >= 4
        rout_score = routing_report.routing_accuracy_pct if rout_valid else 0.0
        rout_weight = 15.0
        rout_weighted = (rout_score * rout_weight) / 100.0

        # 5. Automation & Self-Healing (15%)
        auto_valid = (remediation_report.self_healing_success_rate_pct >= 95.0) and len(remediation_report.remediation_actions) >= 3
        auto_score = remediation_report.self_healing_success_rate_pct if auto_valid else 0.0
        auto_weight = 15.0
        auto_weighted = (auto_score * auto_weight) / 100.0

        # 6. Security Protection (10%)
        sec_valid = sec_report.sanitization_verified and (sec_report.security_score_pct >= 95.0)
        sec_score = sec_report.security_score_pct if sec_valid else 0.0
        sec_weight = 10.0
        sec_weighted = (sec_score * sec_weight) / 100.0

        total_score = cov_weighted + acc_weighted + ai_weighted + rout_weighted + auto_weighted + sec_weighted
        total_score = round(total_score, 2)

        pillar_scores: List[AlertingPillarScore] = [
            LoggingPillar := AlertingPillarScore(
                pillar_name="Detection Coverage & Multi-Signal Telemetry",
                weight_pct=cov_weight,
                achieved_score_pct=round(cov_score, 2),
                weighted_score_pct=round(cov_weighted, 2),
                status="PASSED" if cov_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            AlertingPillarScore(
                pillar_name="Alert Accuracy & SRE Golden Signals",
                weight_pct=acc_weight,
                achieved_score_pct=round(acc_score, 2),
                weighted_score_pct=round(acc_weighted, 2),
                status="PASSED" if acc_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            AlertingPillarScore(
                pillar_name="AI Agent Telemetry & Autonomous Failure Detection",
                weight_pct=ai_weight,
                achieved_score_pct=round(ai_score, 2),
                weighted_score_pct=round(ai_weighted, 2),
                status="PASSED" if ai_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            AlertingPillarScore(
                pillar_name="Incident Severity Classification & Routing",
                weight_pct=rout_weight,
                achieved_score_pct=round(rout_score, 2),
                weighted_score_pct=round(rout_weighted, 2),
                status="PASSED" if rout_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            AlertingPillarScore(
                pillar_name="Automated Remediation & Self-Healing Workflows",
                weight_pct=auto_weight,
                achieved_score_pct=round(auto_score, 2),
                weighted_score_pct=round(auto_weighted, 2),
                status="PASSED" if auto_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            AlertingPillarScore(
                pillar_name="Alert Security & Notification Sanitization",
                weight_pct=sec_weight,
                achieved_score_pct=round(sec_score, 2),
                weighted_score_pct=round(sec_weighted, 2),
                status="PASSED" if sec_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
        ]

        if total_score >= 95.0:
            tier = AlertCertificationTier.ENTERPRISE_INCIDENT_READY
            granted = True
        elif total_score >= 90.0:
            tier = AlertCertificationTier.PRODUCTION_ALERTING_READY
            granted = True
        elif total_score >= 80.0:
            tier = AlertCertificationTier.IMPROVEMENT_REQUIRED
            granted = False
        else:
            tier = AlertCertificationTier.FAILED
            granted = False

        return AlertingCertificationReport(
            report_title="Phase 3I.5 Enterprise Alerting & Incident Detection Certification",
            evaluated_at=datetime.now(timezone.utc).isoformat(),
            certification_tier=tier,
            overall_score_pct=total_score,
            minimum_passing_threshold_pct=95.0,
            pillar_scores=pillar_scores,
            certification_granted=granted,
            auditor="DocuTask Enterprise Observability & SRE Incident Certification Engine"
        )
