"""Predictive Evidence Exporter (Part 3H.3.4.14).

Exports the 8 required health verification JSON manifests to health_verification/ directory.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from app.platform_verification.predictive_health_intelligence.domain.models import (
    AccuracyReport,
    AnomalyReport,
    BaselineReport,
    EarlyWarningReport,
    PredictiveHealthScorecard,
    PredictiveHealthTier,
    RecommendationReport,
    RiskPredictionReport,
    TelemetryReport,
)


class PredictiveEvidenceExporter:
    """Exports structured predictive health intelligence evidence manifests."""

    def __init__(self, output_dir: Optional[Path | str] = None) -> None:
        self.output_dir = Path(output_dir or "health_verification")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export_all(
        self,
        telemetry_report: TelemetryReport,
        baseline_report: BaselineReport,
        anomaly_report: AnomalyReport,
        risk_report: RiskPredictionReport,
        early_warning_report: EarlyWarningReport,
        recommendation_report: RecommendationReport,
        accuracy_report: AccuracyReport,
        scorecard: PredictiveHealthScorecard,
        additional_metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Path]:
        """Exports all 8 manifests to disk."""
        exported_files: Dict[str, Path] = {}

        # 1. telemetry_report.json
        telemetry_path = self.output_dir / "telemetry_report.json"
        with open(telemetry_path, "w", encoding="utf-8") as f:
            json.dump(asdict(telemetry_report), f, indent=2, default=str)
        exported_files["telemetry_report"] = telemetry_path

        # 2. baseline_report.json
        baseline_path = self.output_dir / "baseline_report.json"
        with open(baseline_path, "w", encoding="utf-8") as f:
            json.dump(asdict(baseline_report), f, indent=2, default=str)
        exported_files["baseline_report"] = baseline_path

        # 3. anomaly_report.json
        anomaly_path = self.output_dir / "anomaly_report.json"
        with open(anomaly_path, "w", encoding="utf-8") as f:
            json.dump(asdict(anomaly_report), f, indent=2, default=str)
        exported_files["anomaly_report"] = anomaly_path

        # 4. risk_prediction_report.json
        risk_path = self.output_dir / "risk_prediction_report.json"
        with open(risk_path, "w", encoding="utf-8") as f:
            json.dump(asdict(risk_report), f, indent=2, default=str)
        exported_files["risk_prediction_report"] = risk_path

        # 5. early_warning_report.json
        ew_path = self.output_dir / "early_warning_report.json"
        with open(ew_path, "w", encoding="utf-8") as f:
            json.dump(asdict(early_warning_report), f, indent=2, default=str)
        exported_files["early_warning_report"] = ew_path

        # 6. recommendation_report.json
        rec_path = self.output_dir / "recommendation_report.json"
        with open(rec_path, "w", encoding="utf-8") as f:
            json.dump(asdict(recommendation_report), f, indent=2, default=str)
        exported_files["recommendation_report"] = rec_path

        # 7. accuracy_report.json
        acc_path = self.output_dir / "accuracy_report.json"
        with open(acc_path, "w", encoding="utf-8") as f:
            json.dump(asdict(accuracy_report), f, indent=2, default=str)
        exported_files["accuracy_report"] = acc_path

        # 8. metadata.json
        metadata_path = self.output_dir / "metadata.json"
        metadata_payload = {
            "phase": "3H.3.4",
            "framework": "Enterprise Predictive Health Intelligence & Early Failure Detection Verification Framework",
            "platform": "DocuTask Agent",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "overall_score": scorecard.overall_score,
            "certification_tier": scorecard.certification_tier.value if isinstance(scorecard.certification_tier, PredictiveHealthTier) else str(scorecard.certification_tier),
            "certification_verdict": scorecard.certification_verdict,
            "passed": scorecard.passed,
            "dimension_scores": {
                "telemetry_quality": scorecard.telemetry_quality_score,
                "anomaly_detection": scorecard.anomaly_detection_score,
                "prediction_accuracy": scorecard.prediction_accuracy_score,
                "early_warning": scorecard.early_warning_score,
                "preventive_actions": scorecard.preventive_actions_score,
                "observability": scorecard.observability_score,
            },
            "manifest_files": [
                "telemetry_report.json",
                "baseline_report.json",
                "anomaly_report.json",
                "risk_prediction_report.json",
                "early_warning_report.json",
                "recommendation_report.json",
                "accuracy_report.json",
                "metadata.json",
            ],
            "custom_metadata": additional_metadata or {},
        }
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata_payload, f, indent=2, default=str)
        exported_files["metadata"] = metadata_path

        return exported_files
