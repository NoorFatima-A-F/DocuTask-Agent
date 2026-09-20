"""Incident Quality Scorer (Part 3H.3.6M).

Computes composite quality scorecards across the 6 core incident response automation dimensions:
1. Detection Accuracy: 20%
2. Recovery Automation: 20%
3. Safety Controls: 20%
4. Incident Diagnosis: 15%
5. Operational Learning: 15%
6. Security: 10%
"""

from __future__ import annotations

from typing import Any, Dict

from app.platform_verification.incident_response_automation.domain.interfaces import (
    IIncidentQualityScorer,
)
from app.platform_verification.incident_response_automation.domain.models import (
    IncidentArchitectureReport,
    IncidentAutomationTier,
    IncidentClassificationReport,
    IncidentCorrelationReport,
    IncidentDetectionReport,
    IncidentKnowledgeReport,
    IncidentQualityScorecard,
    IncidentSecurityReport,
    PostmortemReport,
    RecoveryPolicyReport,
    RunbookExecutionReport,
    SelfHealingReport,
)


class IncidentQualityScorer(IIncidentQualityScorer):
    """Calculates composite quality scorecards for automated incident response and self-healing."""

    def compute_scorecard(
        self,
        arch_report: IncidentArchitectureReport,
        detect_report: IncidentDetectionReport,
        class_report: IncidentClassificationReport,
        runbook_report: RunbookExecutionReport,
        healing_report: SelfHealingReport,
        policy_report: RecoveryPolicyReport,
        correlation_report: IncidentCorrelationReport,
        knowledge_report: IncidentKnowledgeReport,
        postmortem_report: PostmortemReport,
        security_report: IncidentSecurityReport,
    ) -> IncidentQualityScorecard:
        # 1. Detection Accuracy (20%)
        # Multi-signal detection, precision >= 95%, latency <= 10s
        det_pts = 0.0
        if detect_report.passed and detect_report.precision_pct >= 95.0 and detect_report.recall_pct >= 95.0:
            det_pts += 50.0
        if detect_report.avg_detection_latency_seconds <= 10.0 and detect_report.false_positive_rate_pct <= 5.0:
            det_pts += 50.0
        det_score = min(100.0, det_pts)

        # 2. Recovery Automation (20%)
        # Runbook execution success, zero task loss, MTTR <= 15s
        rec_pts = 0.0
        if runbook_report.passed and runbook_report.successful_steps == runbook_report.total_steps:
            rec_pts += 50.0
        if healing_report.passed and healing_report.zero_task_loss_verified and healing_report.avg_mttr_seconds <= 15.0:
            rec_pts += 50.0
        rec_score = min(100.0, rec_pts)

        # 3. Safety Controls (20%)
        # Policy rules active, dangerous actions blocked, rollback supported
        safe_pts = 0.0
        if policy_report.passed and policy_report.blocked_dangerous_actions >= 2 and policy_report.approval_gated_actions >= 2:
            safe_pts += 50.0
        if arch_report.rollback_supported and arch_report.detection_layer_isolated:
            safe_pts += 50.0
        safe_score = min(100.0, safe_pts)

        # 4. Incident Diagnosis (15%)
        # Classification accuracy >= 95%, causal chain complete, root cause identified
        diag_pts = 0.0
        if class_report.passed and class_report.classification_accuracy_pct >= 95.0:
            diag_pts += 50.0
        if correlation_report.passed and bool(correlation_report.root_cause_identified):
            diag_pts += 50.0
        diag_score = min(100.0, diag_pts)

        # 5. Operational Learning (15%)
        # Knowledge base entries active, postmortem generated with timeline & metrics
        learn_pts = 0.0
        if knowledge_report.passed and knowledge_report.total_knowledge_entries >= 4:
            learn_pts += 50.0
        if postmortem_report.passed and len(postmortem_report.timeline) >= 6 and postmortem_report.mttr_seconds > 0:
            learn_pts += 50.0
        learn_score = min(100.0, learn_pts)

        # 6. Security (10%)
        # Unauthorized execution blocked, RBAC enforced, immutable audit trails
        sec_pts = 0.0
        if security_report.passed and security_report.unauthorized_execution_blocked:
            sec_pts += 50.0
        if security_report.rbac_enforced and security_report.audit_trails_immutable:
            sec_pts += 50.0
        sec_score = min(100.0, sec_pts)

        # Weighted composite calculation
        overall = (
            (det_score * 0.20)
            + (rec_score * 0.20)
            + (safe_score * 0.20)
            + (diag_score * 0.15)
            + (learn_score * 0.15)
            + (sec_score * 0.10)
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = IncidentAutomationTier.AUTONOMOUS_INCIDENT_RESPONSE_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = IncidentAutomationTier.PRODUCTION_AUTOMATION_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 80.0:
            tier = IncidentAutomationTier.NEEDS_IMPROVEMENT
            verdict = "REJECTED"
            passed = False
        else:
            tier = IncidentAutomationTier.FAILED
            verdict = "REJECTED"
            passed = False

        return IncidentQualityScorecard(
            detection_accuracy_score=round(det_score, 2),
            recovery_automation_score=round(rec_score, 2),
            safety_controls_score=round(safe_score, 2),
            incident_diagnosis_score=round(diag_score, 2),
            operational_learning_score=round(learn_score, 2),
            security_score=round(sec_score, 2),
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            details={
                "weights": {
                    "detection_accuracy": 0.20,
                    "recovery_automation": 0.20,
                    "safety_controls": 0.20,
                    "incident_diagnosis": 0.15,
                    "operational_learning": 0.15,
                    "security": 0.10,
                },
                "minimum_required_for_enterprise": 95.0,
            },
        )
