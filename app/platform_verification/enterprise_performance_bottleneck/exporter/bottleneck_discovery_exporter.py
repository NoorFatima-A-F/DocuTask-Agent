"""Phase 3J.7: Bottleneck Discovery Exporter with SHA-256 Integrity Manifest."""

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from app.core.security import resolve_safe_path, validate_safe_filename_segment
from ..domain.interfaces import IBottleneckDiscoveryExporter
from ..domain.models import (
    BottleneckVerificationManifest,
    EnterpriseBottleneckCertificationReport,
)


class BottleneckDiscoveryExporter(IBottleneckDiscoveryExporter):

    PHASE_TO_FILENAME_MAP: Dict[str, str] = {
        "3j.7.1": "architecture_profile.json",
        "3j.7.2": "resource_report.json",
        "3j.7.3": "bottleneck_report.json",
        "3j.7.4": "database_report.json",
        "3j.7.5": "queue_report.json",
        "3j.7.6": "worker_capacity_report.json",
        "3j.7.7": "ai_latency_report.json",
        "3j.7.8": "regression_report.json",
        "3j.7.9": "capacity_model.json",
        "3j.7.10": "optimization_report.json",
    }

    ALIASES_MAP: Dict[str, str] = {
        "architecture_profile.json": "performance_architecture_map.json",
        "resource_report.json": "resource_saturation_report.json",
        "ai_latency_report.json": "ai_performance_report.json",
        "capacity_model.json": "capacity_boundary_report.json",
    }

    def _resolve_filename(self, key: str, report: Any) -> str:
        candidates = [key]
        if hasattr(report, "verifier_id") and report.verifier_id:
            candidates.append(report.verifier_id)
        if hasattr(report, "phase_id") and report.phase_id:
            candidates.append(report.phase_id)

        for cand in candidates:
            match = re.search(r"3j\.7\.\d+", str(cand), re.IGNORECASE)
            if match:
                phase_key = match.group(0).lower()
                if phase_key in self.PHASE_TO_FILENAME_MAP:
                    return self.PHASE_TO_FILENAME_MAP[phase_key]

        return f"report_{key.replace('.', '_').replace('-', '_')}.json"

    def export(
        self,
        reports: Dict[str, Any],
        certification: EnterpriseBottleneckCertificationReport,
        output_dir: str = "performance_verification",
    ) -> List[str]:
        manifest = self.export_all(reports, certification, output_dir=output_dir)
        return manifest.reports_generated

    def export_all(
        self,
        reports: Dict[str, Any],
        certification: EnterpriseBottleneckCertificationReport,
        output_dir: str = "performance_verification",
    ) -> BottleneckVerificationManifest:
        safe_out = Path(output_dir) if output_dir else Path.cwd() / "performance_verification"
        safe_out.mkdir(parents=True, exist_ok=True)
        file_hashes: Dict[str, str] = {}
        written_files: List[str] = []

        for key, report in reports.items():
            raw_fname = self._resolve_filename(key, report)
            fname = validate_safe_filename_segment(raw_fname)
            fpath = resolve_safe_path(safe_out, fname)

            if hasattr(report, "model_dump_json"):
                content = report.model_dump_json(indent=2)
            else:
                content = json.dumps(report, indent=2, default=str)

            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)

            file_hashes[fname] = hashlib.sha256(content.encode("utf-8")).hexdigest()
            written_files.append(fname)

            if fname in self.ALIASES_MAP:
                raw_alias = self.ALIASES_MAP[fname]
                alias_name = validate_safe_filename_segment(raw_alias)
                alias_path = resolve_safe_path(safe_out, alias_name)
                with open(alias_path, "w", encoding="utf-8") as f:
                    f.write(content)
                file_hashes[alias_name] = hashlib.sha256(content.encode("utf-8")).hexdigest()
                written_files.append(alias_name)

        cert_name = "certification_report.json"
        cert_path = resolve_safe_path(safe_out, cert_name)
        cert_content = certification.model_dump_json(indent=2)
        with open(cert_path, "w", encoding="utf-8") as f:
            f.write(cert_content)
        file_hashes[cert_name] = hashlib.sha256(cert_content.encode("utf-8")).hexdigest()
        written_files.append(cert_name)

        manifest = BottleneckVerificationManifest(
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_score=certification.overall_score,
            certification_tier=certification.certification_tier.value,
            passed=certification.passed,
            reports_generated=written_files,
            file_hashes=file_hashes,
        )

        manifest_path = resolve_safe_path(safe_out, "metadata.json")
        manifest_content = manifest.model_dump_json(indent=2)
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

        return manifest
