"""Abstract interfaces for Enterprise Alert Accuracy & Intelligence Verification sub-engines."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .models import (
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


class IGroundTruthEvaluator(ABC):
    """Interface for evaluating confusion matrix against ground truth (3H.4.6.1)."""

    @abstractmethod
    def evaluate_ground_truth(self) -> GroundTruthReport:
        pass


class ITruePositiveVerifier(ABC):
    """Interface for verifying real failure alert generation (3H.4.6.2)."""

    @abstractmethod
    def verify_true_positives(self) -> TruePositiveReport:
        pass


class IFalsePositiveVerifier(ABC):
    """Interface for verifying transient event suppression & false alarm control (3H.4.6.3)."""

    @abstractmethod
    def verify_false_positives(self) -> FalsePositiveReport:
        pass


class IFalseNegativeVerifier(ABC):
    """Interface for verifying silent failure detection (3H.4.6.4)."""

    @abstractmethod
    def verify_false_negatives(self) -> FalseNegativeReport:
        pass


class IPrecisionRecallCalculator(ABC):
    """Interface for calculating precision and recall scores (3H.4.6.5 & 3H.4.6.6)."""

    @abstractmethod
    def calculate_precision(self) -> PrecisionReport:
        pass

    @abstractmethod
    def calculate_recall(self) -> RecallReport:
        pass


class ISeverityAccuracyVerifier(ABC):
    """Interface for verifying severity-to-impact classification (3H.4.6.7)."""

    @abstractmethod
    def verify_severity_accuracy(self) -> SeverityAccuracyReport:
        pass


class IAlertTimingVerifier(ABC):
    """Interface for measuring detection latencies and MTTD (3H.4.6.8)."""

    @abstractmethod
    def verify_timing(self) -> TimingReport:
        pass


class IAlertCorrelationVerifier(ABC):
    """Interface for verifying cascade symptom grouping & root cause deduction (3H.4.6.9)."""

    @abstractmethod
    def verify_correlation(self) -> CorrelationReport:
        pass


class IAlertNoiseEvaluator(ABC):
    """Interface for measuring alert fatigue and noise ratios (3H.4.6.10)."""

    @abstractmethod
    def evaluate_noise(self) -> NoiseReport:
        pass


class IAnomalyDetectionVerifier(ABC):
    """Interface for verifying ML dynamic baseline anomaly alerts (3H.4.6.11)."""

    @abstractmethod
    def verify_anomaly_detection(self) -> AnomalyReport:
        pass


class IAlertRecoveryVerifier(ABC):
    """Interface for validating auto-resolution and incident closure (3H.4.6.12)."""

    @abstractmethod
    def verify_recovery(self) -> RecoveryReport:
        pass


class IAlertAccuracyScorer(ABC):
    """Interface for calculating 6-category weighted accuracy scorecard (3H.4.6.14)."""

    @abstractmethod
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
        pass


class IAlertAccuracyEvidenceExporter(ABC):
    """Interface for exporting structured 14-manifest compliance evidence (3H.4.6.15)."""

    @abstractmethod
    def export_all(
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
        scorecard: AlertAccuracyScorecard,
    ) -> Dict[str, str]:
        pass
