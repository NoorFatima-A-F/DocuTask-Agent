"""
Health Intelligence Scorer (Part 3H.3.3.15).
Computes weighted composite quality scorecards across the 6 core health intelligence categories:
1. State Accuracy: 25%
2. Transition Logic: 20%
3. Failure Detection: 20%
4. Recovery Validation: 15%
5. Alerting: 10%
6. Evidence Quality: 10%
"""
from app.platform_verification.health_transition_intelligence.domain.models import (
    StateMachineReport,
    DegradationReport,
    RecoveryValidationReport,
    SimulationReport,
    AlertingReport,
    IncidentTimeline,
    FlappingReport,
    HealthIntelligenceScorecard,
    HealthTier,
)


class HealthIntelligenceScorer:
    """
    Computes quality scorecards for enterprise health intelligence verification.
    """

    def compute_scorecard(
        self,
        sm_report: StateMachineReport,
        deg_report: DegradationReport,
        rec_report: RecoveryValidationReport,
        sim_report: SimulationReport,
        alert_report: AlertingReport,
        timeline: IncidentTimeline,
        flapping_report: FlappingReport,
        evidence_valid: bool = True,
    ) -> HealthIntelligenceScorecard:
        # 1. State Accuracy (25%)
        # State machine correctly maintains 5 states and deterministic behavior
        state_acc_points = 0.0
        if sm_report.total_states == 5 and sm_report.transition_matrix_valid:
            state_acc_points += 50.0
        if sm_report.all_deterministic and sm_report.passed:
            state_acc_points += 50.0
        state_acc_score = min(100.0, state_acc_points)

        # 2. Transition Logic (20%)
        # Flapping detection active + rule engine + all simulation transitions verified
        trans_points = 0.0
        if flapping_report.passed and flapping_report.window_seconds == 600:
            trans_points += 50.0
        if sim_report.all_scenarios_passed and sim_report.total_scenarios >= 4:
            trans_points += 50.0
        trans_score = min(100.0, trans_points)

        # 3. Failure Detection (20%)
        # Degradation trend analysis + early warning confidence + failure injection
        fail_points = 0.0
        if deg_report.passed and deg_report.confidence >= 0.80:
            fail_points += 50.0
        if sim_report.passed_scenarios >= 4:
            fail_points += 50.0
        fail_score = min(100.0, fail_points)

        # 4. Recovery Validation (15%)
        # Prerequisite verification + automated action + promotion to READY
        rec_points = 0.0
        if rec_report.all_prerequisites_met and rec_report.recovery_state_reached:
            rec_points += 50.0
        if rec_report.passed and rec_report.final_state.value == "READY":
            rec_points += 50.0
        rec_score = min(100.0, rec_points)

        # 5. Alerting (10%)
        alert_score = 100.0 if alert_report.passed and alert_report.prometheus_alertmanager_compatible else 0.0

        # 6. Evidence Quality (10%)
        evidence_score = 100.0 if evidence_valid and timeline.passed else 0.0

        # Weighted composite calculation
        overall = (
            (state_acc_score * 0.25)
            + (trans_score * 0.20)
            + (fail_score * 0.20)
            + (rec_score * 0.15)
            + (alert_score * 0.10)
            + (evidence_score * 0.10)
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = HealthTier.ENTERPRISE_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = HealthTier.PRODUCTION_READY
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 80.0:
            tier = HealthTier.NEEDS_IMPROVEMENT
            verdict = "REJECTED"
            passed = False
        else:
            tier = HealthTier.FAILED
            verdict = "REJECTED"
            passed = False

        return HealthIntelligenceScorecard(
            state_accuracy_score=round(state_acc_score, 2),
            transition_logic_score=round(trans_score, 2),
            failure_detection_score=round(fail_score, 2),
            recovery_validation_score=round(rec_score, 2),
            alerting_score=round(alert_score, 2),
            evidence_quality_score=round(evidence_score, 2),
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            details={
                "weights": {
                    "state_accuracy": 0.25,
                    "transition_logic": 0.20,
                    "failure_detection": 0.20,
                    "recovery_validation": 0.15,
                    "alerting": 0.10,
                    "evidence_quality": 0.10,
                },
                "minimum_required_for_enterprise": 95.0,
            },
        )
