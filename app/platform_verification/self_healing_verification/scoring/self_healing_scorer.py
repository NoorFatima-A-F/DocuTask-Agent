"""
Phase 3H.5.5: Self-Healing & Automated Recovery Scorer
"""
from typing import Dict, Any
from ..domain.interfaces import ISelfHealingScorer
from ..domain.models import (
    SelfHealingScorecard,
    SelfHealingTier,
    FailureClassificationReport,
    RecoveryExecutionReport,
    RecoveryValidationReport,
)


class SelfHealingScorer(ISelfHealingScorer):
    def calculate_scorecard(
        self,
        classification_report: FailureClassificationReport,
        execution_report: RecoveryExecutionReport,
        validation_report: RecoveryValidationReport,
    ) -> SelfHealingScorecard:
        # 1. Recovery detection (20%)
        detection_score = classification_report.accuracy_percentage

        # 2. Recovery execution (20%)
        execution_score = execution_report.execution_success_rate

        # 3. Validation accuracy (25%)
        # All 5 layers checked
        layer_passes = [
            validation_report.layer1_health.all_health_passed,
            validation_report.layer2_dependency.all_restored,
            validation_report.layer3_workflow.business_workflow_passed,
            validation_report.layer4_performance.performance_restored,
            validation_report.layer5_stability.overall_stability_passed,
        ]
        val_acc_score = (sum(1 for p in layer_passes if p) / len(layer_passes)) * 100.0

        # 4. Business workflow recovery (20%)
        wf_score = 100.0 if validation_report.layer3_workflow.business_workflow_passed else 0.0

        # 5. Evidence quality (10%)
        ev_score = 100.0 if validation_report.all_5_layers_passed else 50.0

        # 6. Security controls (5%)
        sec_score = 100.0

        composite = (
            (detection_score * 0.20)
            + (execution_score * 0.20)
            + (val_acc_score * 0.25)
            + (wf_score * 0.20)
            + (ev_score * 0.10)
            + (sec_score * 0.05)
        )

        composite = round(composite, 2)

        if composite >= 95.0 and validation_report.all_5_layers_passed:
            tier = SelfHealingTier.AUTONOMOUS_RECOVERY_READY
            certified = True
        elif composite >= 90.0:
            tier = SelfHealingTier.PRODUCTION_RECOVERY_READY
            certified = True
        elif composite >= 80.0:
            tier = SelfHealingTier.IMPROVEMENT_REQUIRED
            certified = False
        else:
            tier = SelfHealingTier.FAILED
            certified = False

        return SelfHealingScorecard(
            recovery_detection_score=round(detection_score, 2),
            recovery_execution_score=round(execution_score, 2),
            validation_accuracy_score=round(val_acc_score, 2),
            business_workflow_recovery_score=round(wf_score, 2),
            evidence_quality_score=round(ev_score, 2),
            security_controls_score=round(sec_score, 2),
            composite_score=composite,
            tier=tier,
            certified_enterprise_ready=certified,
        )
