"""
Phase 3I.9.14: Observability Intelligence Evidence Exporter
Exports all 13 predictive reliability verification reports + certification report + metadata.json with SHA-256 signatures
to observability_intelligence_verification/.
"""
import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any

from ..domain.interfaces import IObservabilityIntelligenceEvidenceExporter
from ..domain.models import (
    AIOpsArchitectureReport,
    OperationalDataQualityReport,
    FailurePredictionReport,
    CapacityForecastingReport,
    BehaviorBaselineReport,
    PredictiveAnomalyReport,
    ReliabilityIntelligenceReport,
    IncidentPreventionReport,
    DeploymentIntelligenceReport,
    AIReliabilityMonitoringReport,
    ContinuousOptimizationReport,
    AIOpsExplainabilityReport,
    AIOpsValidationReport,
    PredictiveCertificationReport,
)


class ObservabilityIntelligenceEvidenceExporter(IObservabilityIntelligenceEvidenceExporter):
    def export_all_reports(
        self,
        output_dir: str,
        arch_report: AIOpsArchitectureReport,
        data_report: OperationalDataQualityReport,
        pred_report: FailurePredictionReport,
        capacity_report: CapacityForecastingReport,
        baseline_report: BehaviorBaselineReport,
        anomaly_report: PredictiveAnomalyReport,
        score_report: ReliabilityIntelligenceReport,
        prevention_report: IncidentPreventionReport,
        deploy_report: DeploymentIntelligenceReport,
        ai_report: AIReliabilityMonitoringReport,
        opt_report: ContinuousOptimizationReport,
        explain_report: AIOpsExplainabilityReport,
        val_report: AIOpsValidationReport,
        certification_report: PredictiveCertificationReport,
    ) -> Dict[str, Any]:
        os.makedirs(output_dir, exist_ok=True)

        report_map = {
            "aiops_architecture_report.json": arch_report.model_dump(mode="json"),
            "data_quality_report.json": data_report.model_dump(mode="json"),
            "prediction_report.json": pred_report.model_dump(mode="json"),
            "capacity_report.json": capacity_report.model_dump(mode="json"),
            "baseline_report.json": baseline_report.model_dump(mode="json"),
            "anomaly_prediction_report.json": anomaly_report.model_dump(mode="json"),
            "reliability_score_report.json": score_report.model_dump(mode="json"),
            "prevention_report.json": prevention_report.model_dump(mode="json"),
            "deployment_intelligence_report.json": deploy_report.model_dump(mode="json"),
            "ai_reliability_report.json": ai_report.model_dump(mode="json"),
            "optimization_report.json": opt_report.model_dump(mode="json"),
            "explainability_report.json": explain_report.model_dump(mode="json"),
            "validation_report.json": val_report.model_dump(mode="json"),
            "certification_report.json": certification_report.model_dump(mode="json"),
        }

        file_manifest = {}
        for filename, content in report_map.items():
            filepath = os.path.join(output_dir, filename)
            json_str = json.dumps(content, indent=2)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(json_str)

            sha256 = hashlib.sha256(json_str.encode("utf-8")).hexdigest()
            file_manifest[filename] = {
                "file_path": filepath,
                "file_size_bytes": len(json_str.encode("utf-8")),
                "sha256_hash": sha256,
            }

        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3I.9",
            "capability": "Predictive Reliability Intelligence",
            "framework_phase": "Phase 3I.9 — Observability Intelligence, Predictive Reliability & AIOps Maturity",
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "target_directory": output_dir,
            "overall_certification_tier": certification_report.certification_tier.value,
            "overall_score_pct": certification_report.overall_score_pct,
            "certification_granted": certification_report.certification_granted,
            "total_reports_exported": len(report_map),
            "manifest": file_manifest,
        }

        metadata_path = os.path.join(output_dir, "metadata.json")
        meta_json_str = json.dumps(metadata, indent=2)
        with open(metadata_path, "w", encoding="utf-8") as f:
            f.write(meta_json_str)

        metadata["manifest"]["metadata.json"] = {
            "file_path": metadata_path,
            "file_size_bytes": len(meta_json_str.encode("utf-8")),
            "sha256_hash": hashlib.sha256(meta_json_str.encode("utf-8")).hexdigest(),
        }

        return metadata
