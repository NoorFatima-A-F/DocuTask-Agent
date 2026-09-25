"""
Phase 3I.8.13: Observability Automation Evidence Exporter
Exports all 12 autonomous reliability verification reports + certification report + metadata.json with SHA-256 signatures
to observability_automation_verification/.
"""
import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any

from ..domain.interfaces import IObservabilityAutomationEvidenceExporter
from ..domain.models import (
    AutonomousArchitectureReport,
    AnomalyDetectionReport,
    EventCorrelationReport,
    RootCauseAnalysisReport,
    RemediationExecutionReport,
    AutomationSafetyReport,
    SelfHealingValidationReport,
    IncidentAutomationReport,
    ReliabilityLearningReport,
    AutonomousTestingReport,
    HumanControlPolicyReport,
    AutonomousDashboardReport,
    AutonomousCertificationReport,
)


class ObservabilityAutomationEvidenceExporter(IObservabilityAutomationEvidenceExporter):
    def export_all_reports(
        self,
        output_dir: str,
        arch_report: AutonomousArchitectureReport,
        anomaly_report: AnomalyDetectionReport,
        corr_report: EventCorrelationReport,
        rca_report: RootCauseAnalysisReport,
        remediation_report: RemediationExecutionReport,
        safety_report: AutomationSafetyReport,
        healing_report: SelfHealingValidationReport,
        incident_report: IncidentAutomationReport,
        learning_report: ReliabilityLearningReport,
        testing_report: AutonomousTestingReport,
        human_report: HumanControlPolicyReport,
        dash_report: AutonomousDashboardReport,
        certification_report: AutonomousCertificationReport,
    ) -> Dict[str, Any]:
        os.makedirs(output_dir, exist_ok=True)

        report_map = {
            "architecture_report.json": arch_report.model_dump(mode="json"),
            "anomaly_report.json": anomaly_report.model_dump(mode="json"),
            "correlation_report.json": corr_report.model_dump(mode="json"),
            "root_cause_report.json": rca_report.model_dump(mode="json"),
            "remediation_report.json": remediation_report.model_dump(mode="json"),
            "safety_report.json": safety_report.model_dump(mode="json"),
            "self_healing_report.json": healing_report.model_dump(mode="json"),
            "incident_report.json": incident_report.model_dump(mode="json"),
            "learning_report.json": learning_report.model_dump(mode="json"),
            "testing_report.json": testing_report.model_dump(mode="json"),
            "human_control_policy_report.json": human_report.model_dump(mode="json"),
            "autonomous_dashboard_report.json": dash_report.model_dump(mode="json"),
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
            "phase": "3I.8",
            "framework_phase": "Phase 3I.8 — Observability Automation, Self-Healing Operations & Autonomous Reliability",
            "automation_level": "autonomous",
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
