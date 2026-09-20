"""
Phase 3H.5.9: Evidence Exporter for Predictive Health Intelligence & Proactive Failure Prevention
"""
import os
import json
import hashlib
from datetime import datetime, timezone
from typing import List, Dict, Any
from ..domain.models import (
    PredictiveArchitectureReport,
    FeatureEngineeringReport,
    AnomalyDetectionReport,
    FailurePredictionReport,
    CapacityPredictionReport,
    ProactiveRemediationReport,
    PredictionAccuracyReport,
    PredictiveIncidentReport,
    ReliabilityTwinReport,
    ChaosPredictionReport,
    PredictiveDashboardReport,
    PredictiveHealthScorecard,
)


class PredictiveHealthExporter:
    def export_evidence_manifests(
        self,
        output_dir: str,
        arch_report: PredictiveArchitectureReport,
        feature_report: FeatureEngineeringReport,
        anomaly_report: AnomalyDetectionReport,
        prediction_report: FailurePredictionReport,
        capacity_report: CapacityPredictionReport,
        remediation_report: ProactiveRemediationReport,
        accuracy_report: PredictionAccuracyReport,
        incident_report: PredictiveIncidentReport,
        twin_report: ReliabilityTwinReport,
        chaos_report: ChaosPredictionReport,
        dashboard_report: PredictiveDashboardReport,
        scorecard: PredictiveHealthScorecard,
    ) -> List[str]:
        os.makedirs(output_dir, exist_ok=True)
        exported_files: List[str] = []

        manifest_map: Dict[str, Any] = {
            "architecture_report.json": arch_report.model_dump(),
            "feature_report.json": feature_report.model_dump(),
            "anomaly_report.json": anomaly_report.model_dump(),
            "failure_prediction_report.json": prediction_report.model_dump(),
            "capacity_prediction_report.json": capacity_report.model_dump(),
            "remediation_report.json": remediation_report.model_dump(),
            "accuracy_report.json": accuracy_report.model_dump(),
            "predictive_incident_report.json": incident_report.model_dump(),
            "reliability_twin_report.json": twin_report.model_dump(),
            "chaos_prediction_report.json": chaos_report.model_dump(),
            "certification_report.json": scorecard.model_dump(),
        }

        file_hashes = {}
        for filename, data in manifest_map.items():
            filepath = os.path.join(output_dir, filename)
            content_str = json.dumps(data, indent=2, default=str)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content_str)
            exported_files.append(filepath)
            sha = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
            file_hashes[filename] = sha

        now_iso = datetime.now(timezone.utc).isoformat()
        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3H.5.9",
            "capability": "Predictive Health Intelligence & Proactive Failure Prevention",
            "environment": "production_verification",
            "timestamp": now_iso,
            "composite_score": scorecard.composite_score,
            "tier": scorecard.tier.value,
            "certified_predictive_ready": scorecard.certified_predictive_ready,
            "manifest_hashes": file_hashes,
        }

        meta_filepath = os.path.join(output_dir, "metadata.json")
        with open(meta_filepath, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        exported_files.append(meta_filepath)

        return exported_files
