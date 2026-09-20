"""Alert Accuracy Scorer (3H.4.6.14).

Computes 6-category weighted composite score for alert intelligence:
- True positive detection (25%)
- False positive control (20%)
- False negative prevention (20%)
- Severity accuracy (15%)
- Detection speed (10%)
- Correlation quality (10%)
"""

from datetime import datetime, timezone
from ..domain.models import (
    GroundTruthReport,
    TruePositiveReport,
    FalsePositiveReport,
    FalseNegativeReport,
    PrecisionReport,
    RecallReport,
    SeverityAccuracyReport,
    TimingReport,
    CorrelationReport,
    NoiseReport,
    AnomalyReport,
    RecoveryReport,
    AlertAccuracyScorecard,
    AlertAccuracyTier,
)
from ..domain.interfaces import IAlertAccuracyScorer


class AlertAccuracyScorer(IAlertAccuracyScorer):
    """Calculates weighted operational readiness score for alert accuracy and intelligence."""

    def score_accuracy(
        self,
        gt_rep: GroundTruthReport,
        tp_rep: TruePositiveReport,
        fp_rep: FalsePositiveReport,
        fn_rep: FalseNegativeReport,
        prec_rep: PrecisionReport,
        rec_rep: RecallReport,
        sev_rep: SeverityAccuracyReport,
        time_rep: TimingReport,
        corr_rep: CorrelationReport,
        noise_rep: NoiseReport,
        anom_rep: AnomalyReport,
        recov_rep: RecoveryReport,
    ) -> AlertAccuracyScorecard:
        # 1. True Positive Detection (25%)
        tp_score = 100.0 if (tp_rep.status == "PASS" and rec_rep.recall_target_met) else 50.0

        # 2. False Positive Control (20%)
        fp_score = 100.0 if (fp_rep.status == "PASS" and prec_rep.precision_target_met) else 50.0

        # 3. False Negative Prevention (20%)
        fn_score = 100.0 if (fn_rep.status == "PASS" and fn_rep.zero_undetected_silent_failures) else 50.0

        # 4. Severity Accuracy (15%)
        sev_score = 100.0 if (sev_rep.status == "PASS" and sev_rep.critical_misclassifications == 0) else 50.0

        # 5. Detection Speed (10%)
        speed_score = 100.0 if (time_rep.status == "PASS" and time_rep.detection_sla_met) else 50.0

        # 6. Correlation Quality (10%)
        corr_score = 100.0 if (corr_rep.status == "PASS" and corr_rep.correlation_efficiency_ratio >= 0.90) else 50.0

        # Weighted calculation
        overall = (
            tp_score * 0.25
            + fp_score * 0.20
            + fn_score * 0.20
            + sev_score * 0.15
            + speed_score * 0.10
            + corr_score * 0.10
        )
        overall = round(overall, 2)

        if overall >= 95.0:
            tier = AlertAccuracyTier.ENTERPRISE_ALERT_INTELLIGENCE_CERTIFIED
            verdict = "CERTIFIED"
            passed = True
        elif overall >= 90.0:
            tier = AlertAccuracyTier.PRODUCTION_RELIABLE_ALERTING
            verdict = "CONDITIONAL_PASS"
            passed = True
        elif overall >= 80.0:
            tier = AlertAccuracyTier.IMPROVEMENT_REQUIRED
            verdict = "REMEDIATION_REQUIRED"
            passed = False
        else:
            tier = AlertAccuracyTier.FAILED
            verdict = "FAILED"
            passed = False

        return AlertAccuracyScorecard(
            true_positive_score=tp_score,
            false_positive_score=fp_score,
            false_negative_score=fn_score,
            severity_accuracy_score=sev_score,
            detection_speed_score=speed_score,
            correlation_quality_score=corr_score,
            overall_score=overall,
            certification_tier=tier,
            certification_verdict=verdict,
            passed=passed,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
