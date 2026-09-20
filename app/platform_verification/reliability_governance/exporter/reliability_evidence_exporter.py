"""
Phase 3I.6.13: Reliability Evidence Exporter
Exports all 9 verification reports + certification report + automation report + metadata.json with SHA-256 signatures
to observability_verification/reliability/.
"""
import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any

from ..domain.interfaces import IReliabilityEvidenceExporter
from ..domain.models import (
    ReliabilityGovernanceReport,
    SLIReport,
    SLOReport,
    ErrorBudgetReport,
    ReliabilityDashboardReport,
    ReliabilityTrendReport,
    ProductionGateReport,
    ReliabilityRegressionReport,
    TelemetryQualityReport,
    ReliabilityAutomationReport,
    ReliabilityCertificationReport,
)


class ReliabilityEvidenceExporter(IReliabilityEvidenceExporter):
    def export_all_reports(
        self,
        output_dir: str,
        gov_report: ReliabilityGovernanceReport,
        sli_report: SLIReport,
        slo_report: SLOReport,
        budget_report: ErrorBudgetReport,
        dash_report: ReliabilityDashboardReport,
        trend_report: ReliabilityTrendReport,
        gate_report: ProductionGateReport,
        reg_report: ReliabilityRegressionReport,
        qual_report: TelemetryQualityReport,
        auto_report: ReliabilityAutomationReport,
        certification_report: ReliabilityCertificationReport,
    ) -> Dict[str, Any]:
        os.makedirs(output_dir, exist_ok=True)

        report_map = {
            "governance_report.json": gov_report.model_dump(mode="json"),
            "sli_report.json": sli_report.model_dump(mode="json"),
            "slo_report.json": slo_report.model_dump(mode="json"),
            "error_budget_report.json": budget_report.model_dump(mode="json"),
            "dashboard_report.json": dash_report.model_dump(mode="json"),
            "trend_analysis_report.json": trend_report.model_dump(mode="json"),
            "production_gate_report.json": gate_report.model_dump(mode="json"),
            "regression_report.json": reg_report.model_dump(mode="json"),
            "telemetry_quality_report.json": qual_report.model_dump(mode="json"),
            "automation_report.json": auto_report.model_dump(mode="json"),
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
            "framework_phase": "Phase 3I.6 — Observability Governance, SLO Engineering & Reliability Certification",
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
