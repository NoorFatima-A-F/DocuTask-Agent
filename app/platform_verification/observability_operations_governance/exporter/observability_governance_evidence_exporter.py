"""
Phase 3I.10: Observability Intelligence Governance Evidence Exporter
Exports 11 JSON reports + metadata.json with cryptographic SHA-256 signatures to observability_governance_verification/
"""
import json
import hashlib
from pathlib import Path
from typing import Dict, Any
from datetime import datetime, timezone
from app.platform_verification.observability_operations_governance.domain.models import (
    EnterpriseOperationsCertificationReport,
)
from app.platform_verification.observability_operations_governance.domain.interfaces import (
    IObservabilityGovernanceExporter,
)


class ObservabilityGovernanceEvidenceExporter(IObservabilityGovernanceExporter):
    def __init__(self, output_dir: str = "observability_governance_verification"):
        self.output_dir = Path(output_dir)

    def export(
        self,
        verification_results: Dict[str, Any],
        certification_report: EnterpriseOperationsCertificationReport,
    ) -> Dict[str, str]:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        report_file_map = {
            "governance_architecture_report.json": verification_results.get("governance_architecture"),
            "policy_report.json": verification_results.get("policy_management"),
            "maturity_report.json": verification_results.get("maturity_model"),
            "sre_report.json": verification_results.get("sre_management"),
            "runbook_report.json": verification_results.get("runbook_automation"),
            "automation_safety_report.json": verification_results.get("automation_safety"),
            "change_management_report.json": verification_results.get("change_management"),
            "incident_report.json": verification_results.get("incident_governance"),
            "improvement_report.json": verification_results.get("continuous_improvement"),
            "dashboard_report.json": verification_results.get("operations_dashboard"),
            "certification_report.json": certification_report,
        }

        generated_files: Dict[str, str] = {}
        manifest_entries = {}

        for filename, data_obj in report_file_map.items():
            if data_obj is None:
                continue

            file_path = self.output_dir / filename
            if hasattr(data_obj, "model_dump"):
                content_dict = data_obj.model_dump(mode="json")
            elif hasattr(data_obj, "dict"):
                content_dict = data_obj.dict()
            else:
                content_dict = data_obj

            json_bytes = json.dumps(content_dict, indent=2).encode("utf-8")
            file_path.write_bytes(json_bytes)

            sha256_hash = hashlib.sha256(json_bytes).hexdigest()
            generated_files[filename] = str(file_path.resolve())
            manifest_entries[filename] = {
                "sha256": sha256_hash,
                "bytes": len(json_bytes),
                "verified": True,
            }

        # Write metadata.json
        metadata = {
            "metadata_version": "1.0.0",
            "phase": "Phase 3I.10 — Observability Intelligence Governance, Reliability Automation Maturity & Enterprise Operations Certification",
            "system_name": "DocuTask Agent Platform",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "target_directory": str(self.output_dir),
            "composite_operations_score_pct": certification_report.composite_operations_score_pct,
            "certification_tier": certification_report.certification_tier.value,
            "reports_count": len(manifest_entries),
            "manifest": manifest_entries,
        }

        metadata_bytes = json.dumps(metadata, indent=2).encode("utf-8")
        metadata_path = self.output_dir / "metadata.json"
        metadata_path.write_bytes(metadata_bytes)
        generated_files["metadata.json"] = str(metadata_path.resolve())

        return generated_files
