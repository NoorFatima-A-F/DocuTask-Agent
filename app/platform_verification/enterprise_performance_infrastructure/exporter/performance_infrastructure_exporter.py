"""Phase 3J.6: Performance Infrastructure Exporter.

Exports all structured performance reports, certification summary, and cryptographic SHA-256 metadata manifest.
"""

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..domain.interfaces import IPerformanceInfrastructureExporter
from ..domain.models import (
    EnterprisePerformanceCertificationReport,
    PerformanceVerificationManifest,
)


class PerformanceInfrastructureExporter(IPerformanceInfrastructureExporter):
    """Exports structured reports and SHA-256 metadata manifest to performance_verification/."""

    PHASE_TO_FILENAME_MAP: Dict[str, str] = {
        "3j.6.1": "architecture_report.json",
        "3j.6.2": "workload_model_report.json",
        "3j.6.3": "api_latency_report.json",
        "3j.6.4": "e2e_workflow_report.json",
        "3j.6.5": "throughput_scaling_report.json",
        "3j.6.6": "database_performance_report.json",
        "3j.6.7": "queue_capacity_report.json",
        "3j.6.8": "worker_efficiency_report.json",
        "3j.6.9": "resource_utilization_report.json",
        "3j.6.10": "memory_stability_report.json",
        "3j.6.11": "degradation_analysis_report.json",
        "3j.6.12": "capacity_boundary_report.json",
        "3j.6.13": "monitoring_integration_report.json",
    }

    KEYWORD_TO_FILENAME_MAP: Dict[str, str] = {
        "arch": "architecture_report.json",
        "workload": "workload_model_report.json",
        "api": "api_latency_report.json",
        "e2e": "e2e_workflow_report.json",
        "throughput": "throughput_scaling_report.json",
        "database": "database_performance_report.json",
        "queue": "queue_capacity_report.json",
        "worker": "worker_efficiency_report.json",
        "resource": "resource_utilization_report.json",
        "memory": "memory_stability_report.json",
        "degrad": "degradation_analysis_report.json",
        "capacity": "capacity_boundary_report.json",
        "monitor": "monitoring_integration_report.json",
    }

    ALIASES_MAP: Dict[str, str] = {
        "architecture_report.json": "test_architecture_report.json",
        "resource_utilization_report.json": "system_resource_report.json",
        "memory_stability_report.json": "soak_test_report.json",
    }

    def _resolve_filename(self, key: str, report: Any) -> str:
        # 1. First priority: Exact phase ID match via regex
        candidates = [key]
        if hasattr(report, "verifier_id") and report.verifier_id:
            candidates.append(report.verifier_id)
        if hasattr(report, "phase_id") and report.phase_id:
            candidates.append(report.phase_id)

        for cand in candidates:
            match = re.search(r"3j\.6\.\d+", str(cand), re.IGNORECASE)
            if match:
                phase_key = match.group(0).lower()
                if phase_key in self.PHASE_TO_FILENAME_MAP:
                    return self.PHASE_TO_FILENAME_MAP[phase_key]

        # 2. Second priority: Keyword match
        for cand in candidates:
            c_lower = str(cand).lower()
            for kw, fname in self.KEYWORD_TO_FILENAME_MAP.items():
                if kw in c_lower:
                    return fname

        return f"report_{key.replace('.', '_')}.json"

    def export(
        self,
        reports: Dict[str, Any],
        certification: EnterprisePerformanceCertificationReport,
        output_dir: str = "performance_verification",
    ) -> List[str]:
        manifest = self.export_all(reports, certification, output_dir=output_dir)
        return manifest.reports_generated

    def export_all(
        self,
        reports: Dict[str, Any],
        certification: EnterprisePerformanceCertificationReport,
        output_dir: str = "performance_verification",
    ) -> PerformanceVerificationManifest:
        safe_out = resolve_safe_path(Path.cwd(), output_dir)
        safe_out.mkdir(parents=True, exist_ok=True)
        file_hashes: Dict[str, str] = {}
        written_files: List[str] = []

        # 1. Export individual verification reports
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

            # Check aliases
            if fname in self.ALIASES_MAP:
                raw_alias = self.ALIASES_MAP[fname]
                alias_name = validate_safe_filename_segment(raw_alias)
                alias_path = resolve_safe_path(safe_out, alias_name)
                with open(alias_path, "w", encoding="utf-8") as f:
                    f.write(content)
                file_hashes[alias_name] = hashlib.sha256(content.encode("utf-8")).hexdigest()
                written_files.append(alias_name)

        # 2. Export certification report
        cert_name = "certification_report.json"
        cert_path = resolve_safe_path(safe_out, cert_name)
        cert_content = certification.model_dump_json(indent=2)
        with open(cert_path, "w", encoding="utf-8") as f:
            f.write(cert_content)
        file_hashes[cert_name] = hashlib.sha256(cert_content.encode("utf-8")).hexdigest()
        written_files.append(cert_name)

        # 3. Export metadata manifest
        manifest = PerformanceVerificationManifest(
            system="DocuTask Agent",
            version=certification.version,
            environment=certification.environment,
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
