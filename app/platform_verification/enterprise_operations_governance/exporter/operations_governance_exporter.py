"""
Phase 3R.14: Operations Evidence Package & Governance Artifact Exporter.
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Union

from app.core.security import resolve_safe_path, validate_safe_filename_segment
from ..domain.models import (
    AIOpsReport,
    AlertReport,
    AuditTrailReport,
    ChangeManagementReport,
    ErrorBudgetReport,
    FinOpsReport,
    IncidentReport,
    ManifestEntry,
    OperationalMaturityScore,
    OperationsManifest,
    ProductionHealthReport,
    RootCauseAnalysisReport,
    RunbookReport,
    SelfHealingReport,
    SLODefinitionReport,
)


class OperationsGovernanceExporter:
    """
    Exports structured operational governance reports, metrics, runbooks,
    and cryptographic SHA-256 manifests to the operations_verification directory.
    """

    def __init__(self, base_dir: Optional[Union[str, Path]] = None):
        self.set_base_dir(base_dir or "operations_verification")

    def set_base_dir(self, base_dir: Union[str, Path]) -> None:
        self.base_dir = Path(base_dir) if base_dir else Path.cwd() / "operations_verification"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.runbooks_dir = self.base_dir / "runbooks"
        self.runbooks_dir.mkdir(parents=True, exist_ok=True)

    def _compute_sha256(self, file_path: Union[str, Path]) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def export_all(
        self,
        slo: SLODefinitionReport,
        error_budget: ErrorBudgetReport,
        health: ProductionHealthReport,
        incidents: IncidentReport,
        alerts: AlertReport,
        runbooks: RunbookReport,
        self_healing: SelfHealingReport,
        rca: RootCauseAnalysisReport,
        changes: ChangeManagementReport,
        audit: AuditTrailReport,
        ai_ops: AIOpsReport,
        finops: FinOpsReport,
        maturity: OperationalMaturityScore,
        export_dir: Optional[Union[str, Path]] = None,
    ) -> OperationsManifest:
        if export_dir is not None:
            self.set_base_dir(export_dir)

        # 1. Export JSON Governance Reports
        reports_map = {
            "slo_report.json": slo.model_dump(),
            "error_budget_report.json": error_budget.model_dump(),
            "health_report.json": health.model_dump(),
            "incident_report.json": incidents.model_dump(),
            "alert_report.json": alerts.model_dump(),
            "runbook_report.json": runbooks.model_dump(),
            "self_healing_report.json": self_healing.model_dump(),
            "root_cause_analysis.json": rca.model_dump(),
            "change_history.json": changes.model_dump(),
            "audit_report.json": audit.model_dump(),
            "ai_ops_report.json": ai_ops.model_dump(),
            "finops_report.json": finops.model_dump(),
            "maturity_score.json": maturity.model_dump(),
        }

        for filename, data in reports_map.items():
            with open(self.base_dir / filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)

        # 2. Copy/Export Runbook Markdown Files into operations_verification/runbooks/
        runbook_src_dir = Path("runbooks")
        if runbook_src_dir.exists():
            for rb_file in runbook_src_dir.glob("*.md"):
                dest_file = self.runbooks_dir / rb_file.name
                dest_file.write_text(rb_file.read_text(encoding="utf-8"), encoding="utf-8")

        # 3. Build Cryptographic Manifest
        entries: List[ManifestEntry] = []
        for root, _, files in os.walk(self.base_dir):
            for file_name in sorted(files):
                if file_name in ["metadata.json", "manifest.json"]:
                    continue
                full_p = Path(root) / file_name
                rel_p = str(full_p.relative_to(self.base_dir)).replace("\\", "/")
                sha = self._compute_sha256(full_p)
                entries.append(
                    ManifestEntry(
                        filename=rel_p,
                        report_title=full_p.stem.replace("_", " ").title(),
                        sha256=sha,
                        size_bytes=full_p.stat().st_size,
                    )
                )

        manifest = OperationsManifest(
            project="DocuTask-Agent",
            framework="Enterprise Production Operations Governance Framework",
            version="3.20.0",
            environment="Production Managed Environment",
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_score=maturity.overall_maturity_score,
            certification=maturity.certification.value,
            governance_approved=maturity.governance_passed,
            files=entries,
        )

        manifest_data = manifest.model_dump()
        for mf_name in ["metadata.json", "manifest.json"]:
            with open(self.base_dir / mf_name, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, indent=2, default=str)

        return manifest
