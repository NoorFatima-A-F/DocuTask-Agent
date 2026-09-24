"""Phase 3J.9: AI Workload Performance Evidence Exporter with SHA-256 Integrity Manifest."""

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, List

from ..domain.interfaces import IAIPerformanceExporter
from ..domain.models import (
    AIPerformanceVerificationManifest,
    EnterpriseAIPerformanceCertificationReport,
)


class AIPerformanceExporter(IAIPerformanceExporter):

    PHASE_TO_FILENAME_MAP: Dict[str, str] = {
        "3j.9.1": "architecture_report.json",
        "3j.9.2": "latency_report.json",
        "3j.9.3": "throughput_report.json",
        "3j.9.4": "bottleneck_report.json",
        "3j.9.5": "database_report.json",
        "3j.9.6": "queue_report.json",
        "3j.9.7": "worker_report.json",
        "3j.9.8": "ai_report.json",
        "3j.9.9": "regression_report.json",
        "3j.9.10": "capacity_report.json",
        "3j.9.11": "failure_report.json",
        "3j.9.12": "observability_report.json",
    }

    ALIASES_MAP: Dict[str, str] = {
        "architecture_report.json": "performance_architecture_report.json",
        "latency_report.json": "latency_breakdown_report.json",
        "throughput_report.json": "throughput_capacity_report.json",
        "bottleneck_report.json": "resource_bottleneck_report.json",
        "database_report.json": "database_performance_report.json",
        "queue_report.json": "queue_capacity_report.json",
        "worker_report.json": "worker_scaling_report.json",
        "ai_report.json": "ai_performance_report.json",
        "regression_report.json": "performance_regression_report.json",
        "capacity_report.json": "capacity_plan_report.json",
        "failure_report.json": "performance_failure_report.json",
        "observability_report.json": "performance_observability_report.json",
    }

    def _resolve_filename(self, key: str, report: Any) -> str:
        candidates = [key]
        if hasattr(report, "verifier_id") and report.verifier_id:
            candidates.append(report.verifier_id)
        if hasattr(report, "phase_id") and report.phase_id:
            candidates.append(report.phase_id)

        for cand in candidates:
            match = re.search(r"3j\.9\.\d+", str(cand), re.IGNORECASE)
            if match:
                phase_key = match.group(0).lower()
                if phase_key in self.PHASE_TO_FILENAME_MAP:
                    return self.PHASE_TO_FILENAME_MAP[phase_key]

        return f"report_{key.replace('.', '_').replace('-', '_')}.json"

    def export(
        self,
        reports: Dict[str, Any],
        certification: EnterpriseAIPerformanceCertificationReport,
        output_dir: str = "performance_ai_verification",
    ) -> List[str]:
        manifest = self.export_all(reports, certification, output_dir=output_dir)
        return manifest.reports_generated

    def export_all(
        self,
        reports: Dict[str, Any],
        certification: EnterpriseAIPerformanceCertificationReport,
        output_dir: str = "performance_ai_verification",
    ) -> AIPerformanceVerificationManifest:
        safe_out = resolve_safe_path(Path.cwd(), output_dir)
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

        manifest = AIPerformanceVerificationManifest(
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
