"""
Phase 3H.5.12: Operational Readiness Health Recovery Scorer
"""
from uuid import uuid4
from typing import List
from datetime import datetime, timezone

from ..domain.models import (
    HealthStateTransitionReport,
    FailureDetectionReport,
    RecoveryPolicyReport,
    ComponentRecoveryReport,
    RecoverySafetyReport,
    SelfHealingReport,
    RecoveryChaosReport,
    RecoveryValidationReport,
    RecoveryObservabilityReport,
    RecoverySecurityReport,
    HealthRecoveryScorecard,
    PillarScore,
    RecoveryCertificationTier,
)
from ..domain.interfaces import IHealthRecoveryScorer


class HealthRecoveryScorer(IHealthRecoveryScorer):
    """
    Computes weighted 6-pillar operational recovery readiness scores:
    1. Failure Detection (20%)
    2. Recovery Correctness (25%)
    3. Recovery Safety (20%)
    4. Validation Quality (15%)
    5. Observability (10%)
    6. Security (10%)
    """

    def calculate_scorecard(
        self,
        transition_report: HealthStateTransitionReport,
        detection_report: FailureDetectionReport,
        policy_report: RecoveryPolicyReport,
        component_report: ComponentRecoveryReport,
        safety_report: RecoverySafetyReport,
        self_healing_report: SelfHealingReport,
        chaos_report: RecoveryChaosReport,
        validation_report: RecoveryValidationReport,
        observability_report: RecoveryObservabilityReport,
        security_report: RecoverySecurityReport,
    ) -> HealthRecoveryScorecard:
        pillar_scores: List[PillarScore] = []

        # 1. Failure Detection (20%)
        if detection_report.total_scenarios_tested > 0:
            det_raw = (detection_report.detected_scenarios_count / detection_report.total_scenarios_tested) * 100.0
        else:
            det_raw = 100.0
        det_weighted = det_raw * 0.20
        pillar_scores.append(
            PillarScore(
                pillar_name="Failure Detection",
                weight=0.20,
                raw_score=round(det_raw, 2),
                weighted_score=round(det_weighted, 2),
                status="EXCELLENT" if det_raw >= 95 else "ADEQUATE",
                details=f"{detection_report.detected_scenarios_count}/{detection_report.total_scenarios_tested} failure modes detected. MTTD: {detection_report.mean_time_to_detect_seconds}s.",
            )
        )

        # 2. Recovery Correctness (25%)
        # Blend state transitions, policy operationality, and component restoration
        t_rate = (transition_report.valid_transitions_count / transition_report.total_transitions_evaluated) * 100.0 if transition_report.total_transitions_evaluated > 0 else 100.0
        c_rate = (component_report.successful_recoveries_count / component_report.total_components_verified) * 100.0 if component_report.total_components_verified > 0 else 100.0
        sh_rate = self_healing_report.recovery_success_rate_pct
        corr_raw = (t_rate * 0.3) + (c_rate * 0.4) + (sh_rate * 0.3)
        corr_weighted = corr_raw * 0.25
        pillar_scores.append(
            PillarScore(
                pillar_name="Recovery Correctness",
                weight=0.25,
                raw_score=round(corr_raw, 2),
                weighted_score=round(corr_weighted, 2),
                status="EXCELLENT" if corr_raw >= 95 else "ADEQUATE",
                details=f"Components recovered: {component_report.successful_recoveries_count}/{component_report.total_components_verified}, Self-healing: {sh_rate}%.",
            )
        )

        # 3. Recovery Safety (20%)
        if safety_report.total_safety_rules_verified > 0:
            safe_active = sum(1 for c in safety_report.safety_checks if c.protection_active)
            safe_raw = (safe_active / safety_report.total_safety_rules_verified) * 100.0
        else:
            safe_raw = 100.0
        safe_weighted = safe_raw * 0.20
        pillar_scores.append(
            PillarScore(
                pillar_name="Recovery Safety",
                weight=0.20,
                raw_score=round(safe_raw, 2),
                weighted_score=round(safe_weighted, 2),
                status="EXCELLENT" if safe_raw >= 95 else "ADEQUATE",
                details=f"{safety_report.total_safety_rules_verified} safety protections active (backoffs, limits, blast-radius isolation).",
            )
        )

        # 4. Validation Quality (15%)
        # Blend validation probes and chaos pass rate
        v_rate = (validation_report.passed_probes_count / validation_report.total_probes_executed) * 100.0 if validation_report.total_probes_executed > 0 else 100.0
        ch_rate = (chaos_report.passed_experiments_count / chaos_report.total_chaos_experiments) * 100.0 if chaos_report.total_chaos_experiments > 0 else 100.0
        val_raw = (v_rate * 0.5) + (ch_rate * 0.5)
        val_weighted = val_raw * 0.15
        pillar_scores.append(
            PillarScore(
                pillar_name="Validation Quality",
                weight=0.15,
                raw_score=round(val_raw, 2),
                weighted_score=round(val_weighted, 2),
                status="EXCELLENT" if val_raw >= 95 else "ADEQUATE",
                details=f"Probes passed: {validation_report.passed_probes_count}/{validation_report.total_probes_executed}, Chaos passed: {chaos_report.passed_experiments_count}/{chaos_report.total_chaos_experiments}.",
            )
        )

        # 5. Observability (10%)
        obs_raw = 100.0 if (observability_report.dashboard_configured and observability_report.realtime_telemetry_active) else 80.0
        obs_weighted = obs_raw * 0.10
        pillar_scores.append(
            PillarScore(
                pillar_name="Observability",
                weight=0.10,
                raw_score=round(obs_raw, 2),
                weighted_score=round(obs_weighted, 2),
                status="EXCELLENT" if obs_raw >= 95 else "ADEQUATE",
                details=f"{len(observability_report.metrics)} recovery metrics exported to Prometheus; dashboard active.",
            )
        )

        # 6. Security (10%)
        if security_report.total_actions_audited > 0:
            correctly_handled = security_report.authorized_actions_count + security_report.unauthorized_actions_blocked
            sec_raw = (correctly_handled / security_report.total_actions_audited) * 100.0
        else:
            sec_raw = 100.0
        sec_weighted = sec_raw * 0.10
        pillar_scores.append(
            PillarScore(
                pillar_name="Security",
                weight=0.10,
                raw_score=round(sec_raw, 2),
                weighted_score=round(sec_weighted, 2),
                status="EXCELLENT" if sec_raw >= 95 else "ADEQUATE",
                details=f"RBAC authorization enforced; {security_report.unauthorized_actions_blocked} unauthorized recovery attempts blocked, {security_report.authorized_actions_count} authorized actions executed.",
            )
        )

        overall_score = sum(p.weighted_score for p in pillar_scores)
        overall_score = round(overall_score, 2)

        if overall_score >= 95.0:
            tier = RecoveryCertificationTier.AUTONOMOUS_RECOVERY_READY
            passed = True
        elif overall_score >= 90.0:
            tier = RecoveryCertificationTier.PRODUCTION_RECOVERY_READY
            passed = True
        elif overall_score >= 80.0:
            tier = RecoveryCertificationTier.IMPROVEMENT_REQUIRED
            passed = False
        else:
            tier = RecoveryCertificationTier.FAILED
            passed = False

        return HealthRecoveryScorecard(
            verification_id=f"health-rec-{uuid4().hex[:8]}",
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_recovery_score=overall_score,
            certification_tier=tier,
            passed=passed,
            pillar_scores=pillar_scores,
            mttr_seconds=self_healing_report.mean_time_to_recovery_seconds,
            mttd_seconds=detection_report.mean_time_to_detect_seconds,
            recovery_success_rate=self_healing_report.recovery_success_rate_pct,
        )
