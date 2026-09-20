"""Alert Accuracy Verification Runtime.

Coordinates full end-to-end alert accuracy, intelligence, and reliability evaluation across all sub-phases.
"""

from typing import Dict, Any, Tuple
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
)
from ..evaluators.ground_truth_evaluator import GroundTruthEvaluator
from ..evaluators.true_positive_verifier import TruePositiveVerifier
from ..evaluators.false_positive_verifier import FalsePositiveVerifier
from ..evaluators.false_negative_verifier import FalseNegativeVerifier
from ..evaluators.precision_recall_calculator import PrecisionRecallCalculator
from ..evaluators.severity_accuracy_verifier import SeverityAccuracyVerifier
from ..evaluators.alert_timing_verifier import AlertTimingVerifier
from ..evaluators.alert_correlation_verifier import AlertCorrelationVerifier
from ..evaluators.alert_noise_evaluator import AlertNoiseEvaluator
from ..evaluators.anomaly_detection_verifier import AnomalyDetectionVerifier
from ..evaluators.alert_recovery_verifier import AlertRecoveryVerifier
from ..scoring.alert_accuracy_scorer import AlertAccuracyScorer
from ..exporter.alert_accuracy_evidence_exporter import AlertAccuracyEvidenceExporter


class AlertAccuracyVerificationRuntime:
    """Runtime coordinator executing all alert accuracy and intelligence evaluation engines."""

    def __init__(self, output_dir: str = "alert_accuracy_verification"):
        self.gt_evaluator = GroundTruthEvaluator()
        self.tp_verifier = TruePositiveVerifier()
        self.fp_verifier = FalsePositiveVerifier()
        self.fn_verifier = FalseNegativeVerifier()
        self.pr_calculator = PrecisionRecallCalculator()
        self.sev_verifier = SeverityAccuracyVerifier()
        self.timing_verifier = AlertTimingVerifier()
        self.corr_verifier = AlertCorrelationVerifier()
        self.noise_evaluator = AlertNoiseEvaluator()
        self.anom_verifier = AnomalyDetectionVerifier()
        self.recov_verifier = AlertRecoveryVerifier()
        self.scorer = AlertAccuracyScorer()
        self.exporter = AlertAccuracyEvidenceExporter(output_dir=output_dir)

    def execute_full_verification(self) -> Tuple[AlertAccuracyScorecard, Dict[str, str]]:
        # 1. Ground Truth Confusion Matrix
        gt_rep = self.gt_evaluator.evaluate_ground_truth()

        # 2. True Positives
        tp_rep = self.tp_verifier.verify_true_positives()

        # 3. False Positives
        fp_rep = self.fp_verifier.verify_false_positives()

        # 4. False Negatives
        fn_rep = self.fn_verifier.verify_false_negatives()

        # 5 & 6. Precision & Recall
        prec_rep = self.pr_calculator.calculate_precision()
        rec_rep = self.pr_calculator.calculate_recall()

        # 7. Severity Accuracy
        sev_rep = self.sev_verifier.verify_severity_accuracy()

        # 8. Detection Timing
        time_rep = self.timing_verifier.verify_timing()

        # 9. Correlation
        corr_rep = self.corr_verifier.verify_correlation()

        # 10. Noise & Fatigue
        noise_rep = self.noise_evaluator.evaluate_noise()

        # 11. Anomaly Detection
        anom_rep = self.anom_verifier.verify_anomaly_detection()

        # 12. Alert Recovery
        recov_rep = self.recov_verifier.verify_recovery()

        # 13. Quality Scorecard
        scorecard = self.scorer.score_accuracy(
            gt_rep=gt_rep,
            tp_rep=tp_rep,
            fp_rep=fp_rep,
            fn_rep=fn_rep,
            prec_rep=prec_rep,
            rec_rep=rec_rep,
            sev_rep=sev_rep,
            time_rep=time_rep,
            corr_rep=corr_rep,
            noise_rep=noise_rep,
            anom_rep=anom_rep,
            recov_rep=recov_rep,
        )

        # 14. Export Evidence Manifests
        exported_manifests = self.exporter.export_all(
            gt_rep=gt_rep,
            tp_rep=tp_rep,
            fp_rep=fp_rep,
            fn_rep=fn_rep,
            prec_rep=prec_rep,
            rec_rep=rec_rep,
            sev_rep=sev_rep,
            time_rep=time_rep,
            corr_rep=corr_rep,
            noise_rep=noise_rep,
            anom_rep=anom_rep,
            recov_rep=recov_rep,
            scorecard=scorecard,
        )

        return scorecard, exported_manifests
