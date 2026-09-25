"""
Phase 3I.8.14: Autonomous Reliability Quality Scorer
Calculates weighted scores across the 6 enterprise autonomous operations pillars:
1. Detection Accuracy (20%)
2. Root Cause Analysis (20%)
3. Safe Remediation (20%)
4. Recovery Automation (15%)
5. Human Control (10%)
6. Learning Capability (15%)
"""
from typing import List
from ..domain.interfaces import IAutonomousReliabilityScorer
from ..domain.models import (
    AutonomousArchitectureReport,
    AnomalyDetectionReport,
    EventCorrelationReport,
    RootCauseAnalysisReport,
    RemediationExecutionReport,
    AutomationSafetyReport,
    SelfHealingValidationReport,
    IncidentAutomationReport,
    ReliabilityLearningReport,
    AutonomousTestingReport,
    HumanControlPolicyReport,
    AutonomousDashboardReport,
    AutonomousPillarScore,
    AutonomousCertificationReport,
    AutonomousCertificationTier,
)


class AutonomousReliabilityScorer(IAutonomousReliabilityScorer):
    def calculate_certification_score(
        self,
        arch_report: AutonomousArchitectureReport,
        anomaly_report: AnomalyDetectionReport,
        corr_report: EventCorrelationReport,
        rca_report: RootCauseAnalysisReport,
        remediation_report: RemediationExecutionReport,
        safety_report: AutomationSafetyReport,
        healing_report: SelfHealingValidationReport,
        incident_report: IncidentAutomationReport,
        learning_report: ReliabilityLearningReport,
        testing_report: AutonomousTestingReport,
        human_report: HumanControlPolicyReport,
        dash_report: AutonomousDashboardReport,
    ) -> AutonomousCertificationReport:
        pillar_scores: List[AutonomousPillarScore] = []

        # Pillar 1: Detection Accuracy (20%)
        p1_achieved = 100.0 if (
            anomaly_report.detection_accuracy_pct >= 95.0
            and arch_report.status == "PASS"
            and len(arch_report.components) == 8
        ) else 85.0
        p1_weighted = round((p1_achieved * 20.0) / 100.0, 2)
        pillar_scores.append(
            AutonomousPillarScore(
                pillar_name="Intelligent Anomaly Detection & Telemetry Architecture",
                weight_pct=20.0,
                achieved_score_pct=p1_achieved,
                weighted_score_pct=p1_weighted,
                status="PASSED" if p1_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 2: Root Cause Analysis (20%)
        p2_achieved = 100.0 if (
            corr_report.correlation_verified
            and rca_report.status == "PASS"
            and any(h.confidence >= 0.90 for h in rca_report.hypotheses)
        ) else 85.0
        p2_weighted = round((p2_achieved * 20.0) / 100.0, 2)
        pillar_scores.append(
            AutonomousPillarScore(
                pillar_name="Multi-Signal Event Correlation & AI Root Cause Diagnosis",
                weight_pct=20.0,
                achieved_score_pct=p2_achieved,
                weighted_score_pct=p2_weighted,
                status="PASSED" if p2_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 3: Safe Remediation (20%)
        p3_achieved = 100.0 if (
            remediation_report.all_actions_verified
            and safety_report.guardrails_enforced
            and safety_report.zero_unauthorized_high_risk_actions
        ) else 88.0
        p3_weighted = round((p3_achieved * 20.0) / 100.0, 2)
        pillar_scores.append(
            AutonomousPillarScore(
                pillar_name="Automated Remediation Workflows & Safety Guardrails",
                weight_pct=20.0,
                achieved_score_pct=p3_achieved,
                weighted_score_pct=p3_weighted,
                status="PASSED" if p3_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 4: Recovery Automation (15%)
        p4_achieved = 100.0 if (
            healing_report.all_healing_loops_verified
            and incident_report.lifecycle_automated
            and incident_report.postmortem_automation_verified
        ) else 80.0
        p4_weighted = round((p4_achieved * 15.0) / 100.0, 2)
        pillar_scores.append(
            AutonomousPillarScore(
                pillar_name="Self-Healing Recovery Loops & Automated Postmortems",
                weight_pct=15.0,
                achieved_score_pct=p4_achieved,
                weighted_score_pct=p4_weighted,
                status="PASSED" if p4_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 5: Human Control (10%)
        p5_achieved = 100.0 if (
            human_report.human_oversight_enforced
            and dash_report.dashboards_active
        ) else 85.0
        p5_weighted = round((p5_achieved * 10.0) / 100.0, 2)
        pillar_scores.append(
            AutonomousPillarScore(
                pillar_name="Human-in-the-Loop Governance & AIOps Telemetry Dashboard",
                weight_pct=10.0,
                achieved_score_pct=p5_achieved,
                weighted_score_pct=p5_weighted,
                status="PASSED" if p5_achieved >= 95.0 else "WARNING",
            )
        )

        # Pillar 6: Learning Capability (15%)
        p6_achieved = 100.0 if (
            learning_report.knowledge_base_active
            and learning_report.recurrence_prevention_score_pct >= 95.0
            and testing_report.all_simulations_passed
        ) else 80.0
        p6_weighted = round((p6_achieved * 15.0) / 100.0, 2)
        pillar_scores.append(
            AutonomousPillarScore(
                pillar_name="Reliability Learning & Chaos Simulation Testing",
                weight_pct=15.0,
                achieved_score_pct=p6_achieved,
                weighted_score_pct=p6_weighted,
                status="PASSED" if p6_achieved >= 95.0 else "WARNING",
            )
        )

        overall_score = round(sum(p.weighted_score_pct for p in pillar_scores), 2)
        min_threshold = 95.0
        certification_granted = overall_score >= min_threshold

        if overall_score >= 95.0:
            tier = AutonomousCertificationTier.AUTONOMOUS_OPERATIONS_READY
        elif overall_score >= 90.0:
            tier = AutonomousCertificationTier.ADVANCED_PRODUCTION_OPERATIONS
        elif overall_score >= 80.0:
            tier = AutonomousCertificationTier.IMPROVEMENT_REQUIRED
        else:
            tier = AutonomousCertificationTier.FAILED

        return AutonomousCertificationReport(
            report_title="Phase 3I.8 Enterprise Autonomous Operations & Reliability Certification",
            certification_tier=tier,
            overall_score_pct=overall_score,
            minimum_passing_threshold_pct=min_threshold,
            pillar_scores=pillar_scores,
            certification_granted=certification_granted,
            auditor="DocuTask Enterprise Autonomous Reliability & Self-Healing Operations Certification Engine",
        )
