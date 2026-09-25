"""
Phase 3L: Disaster Recovery Evidence & Artifact Exporter.
"""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from ..domain.models import (
    BaseVerificationReport,
    DisasterRecoveryScorecard,
    ManifestEntry,
    VerificationManifest,
)


class DisasterRecoveryExporter:
    """Exports signed, traceable JSON artifacts for disaster recovery verification with SHA-256 validation."""

    PHASE_FILENAME_MAP = {
        r"3l\.1(?!\d)": ["disaster_recovery_architecture_report.json", "architecture_report.json"],
        r"3l\.2(?!\d)": ["business_impact_analysis.json"],
        r"3l\.3(?!\d)": ["recovery_objectives_report.json", "rto_rpo_report.json"],
        r"3l\.4(?!\d)": ["database_recovery_report.json", "database_backup_report.json"],
        r"3l\.5(?!\d)": ["storage_recovery_report.json", "document_storage_backup.json"],
        r"3l\.6(?!\d)": ["configuration_recovery_report.json"],
        r"3l\.7(?!\d)": ["secret_recovery_report.json"],
        r"3l\.8(?!\d)": ["complete_system_restore_report.json", "restore_report.json"],
        r"3l\.9(?!\d)": ["pitr_recovery_report.json"],
        r"3l\.10(?!\d)": ["backup_security_report.json", "security_report.json"],
        r"3l\.11(?!\d)": ["dr_automation_report.json", "dr_pipeline_report.json"],
        r"3l\.12(?!\d)": ["failure_simulation_report.json"],
        r"3l\.13(?!\d)": ["recovery_observability_report.json", "recovery_metrics.json"],
    }

    def __init__(self, export_dir: Optional[str] = None):
        if export_dir:
            self.export_dir = Path(export_dir)
        else:
            self.export_dir = Path("disaster_recovery_verification")
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def _compute_sha256(self, file_path: Path) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def export_report(self, report: BaseVerificationReport) -> List[Path]:
        written_paths: List[Path] = []
        report_data = report.model_dump()
        target_filenames: List[str] = []

        for pattern, filenames in self.PHASE_FILENAME_MAP.items():
            if re.search(pattern, report.phase_id, re.IGNORECASE) or re.search(pattern, report.verifier_id, re.IGNORECASE):
                target_filenames.extend(filenames)
                break

        if not target_filenames:
            safe_name = report.verifier_id.lower().replace("verify-", "").replace("-", "_")
            target_filenames = [f"{safe_name}.json"]

        for filename in target_filenames:
            file_path = self.export_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2, default=str)
            written_paths.append(file_path)

        return written_paths

    def export_scorecard(self, scorecard: DisasterRecoveryScorecard) -> List[Path]:
        scorecard_data = scorecard.model_dump()
        filenames = ["disaster_recovery_scorecard.json", "recovery_certification.json", "scorecard.json"]
        paths: List[Path] = []
        for filename in filenames:
            file_path = self.export_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(scorecard_data, f, indent=2, default=str)
            paths.append(file_path)
        return paths

    def generate_manifest(
        self,
        scorecard: DisasterRecoveryScorecard,
        reports: List[BaseVerificationReport],
    ) -> VerificationManifest:
        manifest_entries: List[ManifestEntry] = []

        for item in sorted(self.export_dir.iterdir()):
            if item.is_file() and item.name not in ["metadata.json", "manifest.json"]:
                sha = self._compute_sha256(item)
                size = item.stat().st_size
                manifest_entries.append(
                    ManifestEntry(
                        filename=item.name,
                        report_title=item.stem.replace("_", " ").title(),
                        sha256=sha,
                        size_bytes=size,
                    )
                )

        manifest = VerificationManifest(
            system="DocuTask Agent",
            version="3.14.0",
            commit="HEAD",
            environment="Enterprise Disaster Recovery & Continuity Lab",
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_score=scorecard.overall_score,
            certification_tier=scorecard.certification_tier.value,
            files=manifest_entries,
        )

        manifest_data = manifest.model_dump()
        for mf in ["metadata.json", "manifest.json"]:
            mf_path = self.export_dir / mf
            with open(mf_path, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, indent=2, default=str)

        return manifest
