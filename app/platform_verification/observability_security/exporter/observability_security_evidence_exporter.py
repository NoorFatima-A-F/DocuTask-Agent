"""
Phase 3I.7.13: Observability Security Evidence Exporter
Exports all 12 security verification reports + certification report + metadata.json with SHA-256 signatures
to observability_security_verification/.
"""
import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any

from ..domain.interfaces import IObservabilitySecurityEvidenceExporter
from ..domain.models import (
    ObservabilityThreatModelReport,
    SensitiveDataReport,
    LogRedactionReport,
    AITelemetryPrivacyReport,
    AccessControlReport,
    TelemetryEncryptionReport,
    TelemetryRetentionReport,
    ObservabilityAuditReport,
    ComplianceMappingReport,
    AttackSimulationReport,
    TelemetryIncidentResponseReport,
    ContinuousSecurityReport,
    ObservabilitySecurityCertificationReport,
)


class ObservabilitySecurityEvidenceExporter(IObservabilitySecurityEvidenceExporter):
    def export_all_reports(
        self,
        output_dir: str,
        threat_report: ObservabilityThreatModelReport,
        data_report: SensitiveDataReport,
        redact_report: LogRedactionReport,
        ai_report: AITelemetryPrivacyReport,
        access_report: AccessControlReport,
        encrypt_report: TelemetryEncryptionReport,
        retention_report: TelemetryRetentionReport,
        audit_report: ObservabilityAuditReport,
        compliance_report: ComplianceMappingReport,
        attack_report: AttackSimulationReport,
        incident_report: TelemetryIncidentResponseReport,
        continuous_report: ContinuousSecurityReport,
        certification_report: ObservabilitySecurityCertificationReport,
    ) -> Dict[str, Any]:
        os.makedirs(output_dir, exist_ok=True)

        report_map = {
            "threat_model_report.json": threat_report.model_dump(mode="json"),
            "sensitive_data_report.json": data_report.model_dump(mode="json"),
            "redaction_report.json": redact_report.model_dump(mode="json"),
            "ai_privacy_report.json": ai_report.model_dump(mode="json"),
            "access_control_report.json": access_report.model_dump(mode="json"),
            "encryption_report.json": encrypt_report.model_dump(mode="json"),
            "retention_report.json": retention_report.model_dump(mode="json"),
            "audit_report.json": audit_report.model_dump(mode="json"),
            "compliance_report.json": compliance_report.model_dump(mode="json"),
            "attack_simulation_report.json": attack_report.model_dump(mode="json"),
            "incident_response_report.json": incident_report.model_dump(mode="json"),
            "continuous_security_report.json": continuous_report.model_dump(mode="json"),
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
            "phase": "3I.7",
            "framework_phase": "Phase 3I.7 — Observability Security, Privacy & Compliance Verification",
            "security_level": "enterprise",
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
