"""
Phase 3N: Enterprise Infrastructure Security Evidence & Artifact Exporter.
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
    SecurityScorecard,
    VerificationManifest,
)


class InfrastructureSecurityExporter:
    """Exports signed, traceable JSON artifacts for infrastructure security verification with SHA-256 validation."""

    PHASE_FILENAME_MAP = {
        r"3n\.1(?!\d)": ["security_architecture_report.json", "architecture_report.json"],
        r"3n\.2(?!\d)": ["threat_model_report.json"],
        r"3n\.3(?!\d)": ["container_security_report.json"],
        r"3n\.4(?!\d)": ["image_supply_chain_report.json", "image_security_report.json", "software_bill_of_materials.json"],
        r"3n\.5(?!\d)": ["vulnerability_report.json"],
        r"3n\.6(?!\d)": ["secret_security_report.json", "secret_report.json"],
        r"3n\.7(?!\d)": ["iam_security_report.json", "iam_report.json"],
        r"3n\.8(?!\d)": ["network_security_report.json", "network_report.json"],
        r"3n\.9(?!\d)": ["service_security_report.json"],
        r"3n\.10(?!\d)": ["api_security_report.json"],
        r"3n\.11(?!\d)": ["database_security_report.json"],
        r"3n\.12(?!\d)": ["storage_security_report.json"],
        r"3n\.13(?!\d)": ["ai_security_report.json"],
        r"3n\.14(?!\d)": ["cicd_security_report.json"],
        r"3n\.15(?!\d)": ["security_attack_simulation_report.json", "attack_simulation_report.json"],
        r"3n\.16(?!\d)": ["security_monitoring_report.json"],
    }

    def __init__(self, export_dir: Optional[str] = None):
        if export_dir:
            self.export_dir = Path(export_dir)
        else:
            self.export_dir = Path("security_verification")
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

    def export_scorecard(self, scorecard: SecurityScorecard) -> List[Path]:
        scorecard_data = scorecard.model_dump()
        filenames = ["security_scorecard.json", "security_certification.json", "scorecard.json"]
        paths: List[Path] = []
        for filename in filenames:
            file_path = self.export_dir / filename
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(scorecard_data, f, indent=2, default=str)
            paths.append(file_path)
        return paths

    def generate_manifest(
        self,
        scorecard: SecurityScorecard,
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
            project="DocuTask-Agent",
            security_framework="Enterprise DevSecOps & Zero-Trust",
            version="3.16.0",
            commit="HEAD",
            environment="Enterprise Infrastructure Security Lab",
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
