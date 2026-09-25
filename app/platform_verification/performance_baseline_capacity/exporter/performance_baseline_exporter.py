"""
3J.3.13: Performance Evidence Exporter.

Exports all performance baseline and capacity verification reports to `performance_verification/`:
- Granular JSON reports for baseline, load, capacity, AI pipeline, database, queue, scaling, regression, etc.
- Quality certification report
- Cryptographic SHA-256 metadata integrity manifest
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List

from ..domain.interfaces import IPerformanceExporter
from ..domain.models import PerformanceQualityCertificationReport


class PerformanceBaselineExporter(IPerformanceExporter):
    """Exports structured performance reports, certification summary, and SHA-256 signatures."""

    def __init__(self, export_dir: str = "performance_verification"):
        self.export_dir = export_dir

    def _to_dict(self, obj: Any) -> Any:
        """Recursively converts pydantic models, dataclasses, enums, or dicts to json-serializable dicts."""
        if hasattr(obj, "model_dump"):
            return obj.model_dump()
        elif hasattr(obj, "dict"):
            return obj.dict()
        elif hasattr(obj, "__dict__"):
            return {k: self._to_dict(v) for k, v in obj.__dict__.items()}
        elif isinstance(obj, list):
            return [self._to_dict(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: self._to_dict(v) for k, v in obj.items()}
        elif hasattr(obj, "value"):
            return obj.value
        return obj

    def _calculate_sha256(self, file_path: str) -> str:
        """Computes SHA-256 hash of a file on disk."""
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()

    def export(
        self,
        reports: Dict[str, Any],
        certification: PerformanceQualityCertificationReport,
    ) -> List[str]:
        """Exports all performance reports to the target directory and creates metadata.json."""
        os.makedirs(self.export_dir, exist_ok=True)
        exported_files: List[str] = []

        file_mapping = {
            "performance_architecture": "performance_architecture_report.json",
            "baseline_performance": "baseline_report.json",
            "ai_pipeline_performance": "ai_pipeline_report.json",
            "concurrent_load": "load_test_report.json",
            "capacity_model": "capacity_report.json",
            "latency_distribution": "latency_distribution_report.json",
            "resource_utilization": "resource_utilization_report.json",
            "database_performance": "database_report.json",
            "queue_capacity": "queue_report.json",
            "worker_scaling": "scaling_report.json",
            "performance_failure": "performance_failure_report.json",
            "performance_regression": "regression_report.json",
        }

        # 1. Export each verifier report
        for key, filename in file_mapping.items():
            report_obj = reports.get(key)
            if report_obj is not None:
                path = os.path.join(self.export_dir, filename)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(self._to_dict(report_obj), f, indent=2)
                exported_files.append(path)

        # 2. Export certification report
        cert_path = os.path.join(self.export_dir, "certification_report.json")
        with open(cert_path, "w", encoding="utf-8") as f:
            json.dump(self._to_dict(certification), f, indent=2)
        exported_files.append(cert_path)

        # 3. Generate and export metadata.json with cryptographic checksums
        file_hashes = {}
        for file_path in exported_files:
            rel_name = os.path.basename(file_path)
            file_hashes[rel_name] = self._calculate_sha256(file_path)

        metadata = {
            "system": "DocuTask Agent",
            "version": "v3.11.0",
            "commit": "HEAD",
            "phase": "3J.3",
            "name": "Enterprise Performance Baseline & Capacity Verification Framework",
            "environment": "Dedicated Performance Staging Sandbox",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "overall_score": certification.overall_score,
            "certification_tier": certification.certification_tier.value,
            "passed": certification.passed,
            "report_count": len(exported_files),
            "files": file_hashes,
        }

        meta_path = os.path.join(self.export_dir, "metadata.json")
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        exported_files.append(meta_path)

        return exported_files
