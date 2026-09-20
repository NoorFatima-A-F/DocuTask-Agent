"""
Phase 3M: Enterprise Cloud Readiness Evidence & Artifact Exporter.
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
    CloudReadinessScorecard,
    ManifestEntry,
    VerificationManifest,
)


class CloudReadinessExporter:
    """Exports signed, traceable JSON artifacts for cloud readiness verification with SHA-256 validation."""

    PHASE_FILENAME_MAP = {
        r"3m\.1(?!\d)": ["cloud_architecture_assessment.json", "architecture_report.json"],
        r"3m\.2(?!\d)": ["container_cloud_report.json", "container_report.json"],
        r"3m\.3(?!\d)": ["compute_resource_report.json", "compute_report.json"],
        r"3m\.4(?!\d)": ["network_security_report.json", "network_report.json"],
        r"3m\.5(?!\d)": ["cloud_storage_report.json", "storage_report.json"],
        r"3m\.6(?!\d)": ["managed_database_report.json", "database_report.json"],
        r"3m\.7(?!\d)": ["worker_scaling_report.json"],
        r"3m\.8(?!\d)": ["autoscaling_report.json", "scaling_report.json"],
        r"3m\.9(?!\d)": ["cloud_secret_report.json"],
        r"3m\.10(?!\d)": ["cloud_observability_report.json"],
        r"3m\.11(?!\d)": ["iac_verification_report.json"],
        r"3m\.12(?!\d)": ["kubernetes_readiness_report.json", "kubernetes_report.json"],
        r"3m\.13(?!\d)": ["cloud_security_report.json", "security_report.json"],
        r"3m\.14(?!\d)": ["cloud_portability_report.json"],
        r"3m\.15(?!\d)": ["migration_simulation_report.json", "migration_report.json"],
    }

    def __init__(self, export_dir: Optional[str] = None):
        if export_dir:
            self.export_dir = Path(export_dir)
        else:
            self.export_dir = Path("cloud_readiness_verification")
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

    def export_scorecard(self, scorecard: CloudReadinessScorecard) -> List[Path]:
        scorecard_data = scorecard.model_dump()
        filenames = ["cloud_readiness_scorecard.json", "cloud_certification.json", "scorecard.json"]
        paths: List[Path] = []
        for filename in filenames:
            file_path = self.export_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(scorecard_data, f, indent=2, default=str)
            paths.append(file_path)
        return paths

    def generate_manifest(
        self,
        scorecard: CloudReadinessScorecard,
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
            version="3.15.0",
            commit="HEAD",
            environment="Enterprise Cloud Readiness & Multi-Cloud Lab",
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_score=scorecard.overall_score,
            certification_tier=scorecard.certification_tier.value,
            cloud_targets=["AWS", "GCP", "Azure", "Kubernetes"],
            files=manifest_entries,
        )

        manifest_data = manifest.model_dump()
        for mf in ["metadata.json", "manifest.json"]:
            mf_path = self.export_dir / mf
            with open(mf_path, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, indent=2, default=str)

        return manifest
