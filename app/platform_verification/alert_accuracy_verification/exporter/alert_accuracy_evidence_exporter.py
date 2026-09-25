"""Alert Accuracy Evidence Exporter (3H.4.6.15).

Exports 14 deterministic JSON evidence manifests to alert_accuracy_verification/ directory.
"""

from dataclasses import asdict
from datetime import datetime, timezone
import json
import os
from typing import Dict, Any

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
from ..domain.interfaces import IAlertAccuracyEvidenceExporter


class AlertAccuracyEvidenceExporter(IAlertAccuracyEvidenceExporter):
    """Exports structured SRE compliance evidence for Alert Accuracy & Intelligence Verification."""

    def __init__(self, output_dir: str = "alert_accuracy_verification"):
        self.output_dir = output_dir

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
        os.makedirs(self.output_dir, exist_ok=True)
        exported_files: Dict[str, str] = {}

        # 1. ground_truth_report.json
        exported_files["ground_truth_report.json"] = self._write_json(
            "ground_truth_report.json", asdict(gt_rep)
        )

        # 2. true_positive_report.json
        exported_files["true_positive_report.json"] = self._write_json(
            "true_positive_report.json", asdict(tp_rep)
        )

        # 3. false_positive_report.json
        exported_files["false_positive_report.json"] = self._write_json(
            "false_positive_report.json", asdict(fp_rep)
        )

        # 4. false_negative_report.json
        exported_files["false_negative_report.json"] = self._write_json(
            "false_negative_report.json", asdict(fn_rep)
        )

        # 5. precision_report.json
        exported_files["precision_report.json"] = self._write_json(
            "precision_report.json", asdict(prec_rep)
        )

        # 6. recall_report.json
        exported_files["recall_report.json"] = self._write_json(
            "recall_report.json", asdict(rec_rep)
        )

        # 7. severity_report.json
        exported_files["severity_report.json"] = self._write_json(
            "severity_report.json", asdict(sev_rep)
        )

        # 8. timing_report.json
        exported_files["timing_report.json"] = self._write_json(
            "timing_report.json", asdict(time_rep)
        )

        # 9. correlation_report.json
        exported_files["correlation_report.json"] = self._write_json(
            "correlation_report.json", asdict(corr_rep)
        )

        # 10. noise_report.json
        exported_files["noise_report.json"] = self._write_json(
            "noise_report.json", asdict(noise_rep)
        )

        # 11. anomaly_report.json
        exported_files["anomaly_report.json"] = self._write_json(
            "anomaly_report.json", asdict(anom_rep)
        )

        # 12. recovery_report.json
        exported_files["recovery_report.json"] = self._write_json(
            "recovery_report.json", asdict(recov_rep)
        )

        # 13. certification_report.json
        exported_files["certification_report.json"] = self._write_json(
            "certification_report.json", asdict(scorecard)
        )

        # 14. metadata.json
        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3H.4.6",
            "overall_score": scorecard.overall_score,
            "certification_tier": scorecard.certification_tier.value,
            "passed": scorecard.passed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "manifest_count": 14,
            "files": list(exported_files.keys()),
        }
        exported_files["metadata.json"] = self._write_json("metadata.json", metadata)

        return exported_files

    def _write_json(self, filename: str, data: Any) -> str:
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        return filepath
