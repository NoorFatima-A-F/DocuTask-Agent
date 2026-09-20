"""
Phase 3J.10: Enterprise SLA/SLO Evidence & Artifact Exporter.
"""

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..domain.models import (
    BaseVerificationReport,
    ManifestEntry,
    SLASLOScorecard,
    VerificationManifest,
)


class SLASLOExporter:
    """Exports signed, traceable JSON artifacts for SLA/SLO verification with SHA-256 validation."""

    PHASE_FILENAME_MAP = {
        r"3j\.10\.1(?!\d)": ["sla_definition.json", "sla_definition_report.json"],
        r"3j\.10\.2(?!\d)": ["slo_report.json", "slo_configuration_report.json"],
        r"3j\.10\.3(?!\d)": ["error_budget.json", "error_budget_report.json"],
        r"3j\.10\.4(?!\d)": ["monitoring_report.json", "continuous_monitoring_report.json"],
        r"3j\.10\.5(?!\d)": ["regression_report.json", "regression_detection_report.json"],
        r"3j\.10\.6(?!\d)": ["endurance_report.json", "endurance_performance_report.json"],
        r"3j\.10\.7(?!\d)": ["alert_report.json", "performance_alert_report.json"],
        r"3j\.10\.8(?!\d)": ["incident_report.json", "performance_incident_report.json"],
        r"3j\.10\.9(?!\d)": ["recovery_report.json", "performance_recovery_report.json"],
        r"3j\.10\.10(?!\d)": ["dashboard_report.json", "dashboard_validation_report.json"],
        r"3j\.10\.11(?!\d)": ["performance_governance_report.json"],
        r"3j\.10\.12(?!\d)": ["performance_pipeline_report.json"],
    }

    def __init__(self, export_dir: Optional[str] = None):
        if export_dir:
            self.export_dir = Path(export_dir)
        else:
            self.export_dir = Path("sla_slo_verification")
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

    def export_scorecard(self, scorecard: SLASLOScorecard) -> List[Path]:
        scorecard_data = scorecard.model_dump()
        filenames = ["scorecard.json", "performance_reliability_scorecard.json"]
        paths: List[Path] = []
        for filename in filenames:
            file_path = self.export_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(scorecard_data, f, indent=2, default=str)
            paths.append(file_path)
        return paths

    def generate_manifest(
        self,
        scorecard: SLASLOScorecard,
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
            version="3.10.0",
            commit="HEAD",
            environment="Enterprise Production SRE",
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
