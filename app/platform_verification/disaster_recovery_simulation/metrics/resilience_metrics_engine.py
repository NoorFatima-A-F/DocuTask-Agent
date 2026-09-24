"""
Resilience Metrics & Scoring Engine for Part 3G.3.
Calculates weighted resilience scores, evaluates RTO/RPO/MTTR/MTTD, and assigns certification tiers.
"""
from typing import List
from app.platform_verification.disaster_recovery_simulation.domain.models import (
    ResilienceCertificationLevel,
    ScenarioSimulationResult,
    ChaosExperimentResult,
    IncidentDetectionResult,
    PostRecoveryValidationReport,
    TabletopExerciseResult,
    ResilienceScorecard,
)
from app.platform_verification.disaster_recovery_simulation.domain.interfaces import (
    IResilienceMetricsEngine,
)


class ResilienceMetricsEngine(IResilienceMetricsEngine):
    """
    Computes weighted Resilience Score:
    Score = (Recovery Success * 0.30) + (RTO * 0.20) + (RPO * 0.20)
          + (Automation * 0.15) + (Detection * 0.10) + (Documentation * 0.05)
    """

    WEIGHTS = {
        "recovery_success": 0.30,
        "rto_performance": 0.20,
        "rpo_compliance": 0.20,
        "automation": 0.15,
        "detection": 0.10,
        "documentation": 0.05,
    }

    TARGET_RTO_MINUTES = 45.0
    TARGET_RPO_MINUTES = 5.0

    def compute_resilience_scorecard(
        self,
        scenario_results: List[ScenarioSimulationResult],
        chaos_results: List[ChaosExperimentResult],
        detection_result: IncidentDetectionResult,
        validation_report: PostRecoveryValidationReport,
        tabletop_result: TabletopExerciseResult,
    ) -> ResilienceScorecard:
        # 1. Recovery Success Score (30%)
        scenarios_passed = sum(1 for s in scenario_results if s.simulation_passed)
        chaos_passed = sum(1 for c in chaos_results if c.passed)
        total_tests = len(scenario_results) + len(chaos_results)
        total_passed = scenarios_passed + chaos_passed
        recovery_success_score = round((total_passed / total_tests) * 100.0, 2) if total_tests > 0 else 100.0

        # 2. RTO Performance Score (20%)
        # Calculate max and avg RTO across scenarios
        rto_seconds_list = [s.measured_rto_seconds for s in scenario_results]
        max_rto_sec = max(rto_seconds_list) if rto_seconds_list else 420.0
        avg_rto_sec = sum(rto_seconds_list) / len(rto_seconds_list) if rto_seconds_list else 420.0
        max_rto_min = max_rto_sec / 60.0
        avg_rto_min = avg_rto_sec / 60.0

        if max_rto_min <= self.TARGET_RTO_MINUTES:
            rto_score = 100.0
        elif max_rto_min <= 120.0:
            rto_score = 80.0
        else:
            rto_score = 40.0

        # 3. RPO Compliance Score (20%)
        rpo_seconds_list = [s.measured_rpo_seconds for s in scenario_results]
        max_rpo_sec = max(rpo_seconds_list) if rpo_seconds_list else 60.0
        max_rpo_min = max_rpo_sec / 60.0

        if max_rpo_min <= self.TARGET_RPO_MINUTES:
            rpo_score = 100.0
        elif max_rpo_min <= 15.0:
            rpo_score = 80.0
        else:
            rpo_score = 40.0

        # 4. Automation Score (15%)
        automation_score = 100.0 if validation_report.overall_validation_passed else 60.0

        # 5. Detection Score (10%)
        mttd_min = detection_result.measured_mttd_seconds / 60.0
        detection_score = 100.0 if detection_result.mttd_met else 50.0

        # 6. Documentation & Tabletop Score (5%)
        doc_score = 100.0 if tabletop_result.passed else 70.0

        # Composite Weighted Calculation
        composite = (
            (recovery_success_score * self.WEIGHTS["recovery_success"])
            + (rto_score * self.WEIGHTS["rto_performance"])
            + (rpo_score * self.WEIGHTS["rpo_compliance"])
            + (automation_score * self.WEIGHTS["automation"])
            + (detection_score * self.WEIGHTS["detection"])
            + (doc_score * self.WEIGHTS["documentation"])
        )
        composite = round(composite, 2)

        if composite >= 95.0:
            tier = ResilienceCertificationLevel.LEVEL_4_MISSION_CRITICAL
        elif composite >= 90.0:
            tier = ResilienceCertificationLevel.LEVEL_3_ENTERPRISE_READY
        elif composite >= 80.0:
            tier = ResilienceCertificationLevel.LEVEL_2_PRODUCTION_READY
        else:
            tier = ResilienceCertificationLevel.LEVEL_1_NEEDS_IMPROVEMENT

        passed = composite >= 80.0
        ci_cd_approved = composite >= 90.0

        mttr_min = avg_rto_min + mttd_min  # Mean Time to Recovery = MTTD + RTO restoration

        metadata = {
            "evaluation_standard": "DOCUTASK_DISASTER_RECOVERY_v3G.3",
            "weights": self.WEIGHTS,
            "passing_threshold": 80.0,
            "ci_cd_deployment_gate_threshold": 90.0,
            "mission_critical_threshold": 95.0,
            "status": "CERTIFIED" if passed else "FAILED",
        }

        return ResilienceScorecard(
            recovery_success_score=recovery_success_score,
            rto_performance_score=rto_score,
            rpo_compliance_score=rpo_score,
            automation_score=automation_score,
            detection_score=detection_score,
            documentation_score=doc_score,
            composite_score=composite,
            certification_level=tier,
            passed=passed,
            ci_cd_deployment_approved=ci_cd_approved,
            measured_rto_minutes=round(max_rto_min, 2),
            measured_rpo_minutes=round(max_rpo_min, 2),
            measured_mttr_minutes=round(mttr_min, 2),
            measured_mttd_minutes=round(mttd_min, 2),
            metadata=metadata,
        )
