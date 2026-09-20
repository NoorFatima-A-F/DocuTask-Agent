"""3J.5.17: Performance Quality Exporter.

Exports all structured performance reports, certification summary, and cryptographic SHA-256 metadata manifest.
"""

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..domain.interfaces import IPerformanceExporter
from ..domain.models import (
    BaseVerificationReport,
    EnterprisePerformanceCertificationReport,
    PerformanceVerificationManifest,
)


class PerformanceQualityExporter(IPerformanceExporter):
    """Exports structured reports and SHA-256 metadata manifest to performance_verification/."""

    PHASE_TO_FILENAME_MAP: Dict[str, str] = {
        "3j.5.1": "baseline_report.json",
        "3j.5.2": "latency_report.json",
        "3j.5.3": "throughput_report.json",
        "3j.5.4": "load_test_report.json",
        "3j.5.5": "load_test_report.json",
        "3j.5.6": "stress_test_report.json",
        "3j.5.7": "spike_test_report.json",
        "3j.5.8": "endurance_report.json",
        "3j.5.9": "ai_workload_report.json",
        "3j.5.10": "queue_report.json",
        "3j.5.11": "database_report.json",
        "3j.5.12": "storage_report.json",
        "3j.5.13": "resource_report.json",
        "3j.5.14": "bottleneck_report.json",
        "3j.5.15": "capacity_plan.json",
        "3j.5.16": "regression_report.json",
    }

    KEYWORD_TO_FILENAME_MAP: Dict[str, str] = {
        "baseline": "baseline_report.json",
        "latency": "latency_report.json",
        "throughput": "throughput_report.json",
        "load": "load_test_report.json",
        "stress": "stress_test_report.json",
        "spike": "spike_test_report.json",
        "endurance": "endurance_report.json",
        "ai": "ai_workload_report.json",
        "queue": "queue_report.json",
        "database": "database_report.json",
        "storage": "storage_report.json",
        "resource": "resource_report.json",
        "bottleneck": "bottleneck_report.json",
        "capacity": "capacity_plan.json",
        "regression": "regression_report.json",
    }

    ALIASES_MAP: Dict[str, str] = {
        "baseline_report.json": "performance_baseline_report.json",
        "ai_workload_report.json": "ai_pipeline_report.json",
        "resource_report.json": "resource_utilization_report.json",
    }

    def _resolve_filename(self, key: str, report: Any) -> str:
        # 1. First priority: Exact phase ID match (e.g. 3j.5.1, 3j.5.10, 3j.5.16)
        candidates = [key]
        if hasattr(report, "verifier_id") and report.verifier_id:
            candidates.append(report.verifier_id)
        if hasattr(report, "phase_id") and report.phase_id:
            candidates.append(report.phase_id)

        for cand in candidates:
            match = re.search(r"3j\.5\.\d+", str(cand), re.IGNORECASE)
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
        os.makedirs(output_dir, exist_ok=True)
        file_hashes: Dict[str, str] = {}
        written_files: List[str] = []

        # 1. Export individual verification reports
        for key, report in reports.items():
            fname = self._resolve_filename(key, report)
            fpath = os.path.join(output_dir, fname)

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
                alias_name = self.ALIASES_MAP[fname]
                alias_path = os.path.join(output_dir, alias_name)
                with open(alias_path, "w", encoding="utf-8") as f:
                    f.write(content)
                file_hashes[alias_name] = hashlib.sha256(content.encode("utf-8")).hexdigest()
                written_files.append(alias_name)

        # 2. Export certification report
        cert_name = "certification_report.json"
        cert_path = os.path.join(output_dir, cert_name)
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

        manifest_path = os.path.join(output_dir, "metadata.json")
        manifest_content = manifest.model_dump_json(indent=2)
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)

        return manifest
