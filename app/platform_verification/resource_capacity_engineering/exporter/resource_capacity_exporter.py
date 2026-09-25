"""
3J.4.12: Resource Evidence Exporter.

Exports all resource utilization and capacity reports to `performance_verification/`:
- Granular JSON reports for resource profile, CPU capacity, memory endurance, worker scaling, queue capacity, database capacity, AI profile, capacity model, autoscaling readiness, and alerting.
- Resource quality certification report
- Cryptographic SHA-256 metadata manifest
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List

from ..domain.interfaces import IResourceExporter
from ..domain.models import ResourceCapacityCertificationReport


class ResourceCapacityExporter(IResourceExporter):
    """Exports structured resource verification reports, certification summary, and SHA-256 signatures."""

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
        certification: ResourceCapacityCertificationReport,
    ) -> List[str]:
        """Exports all performance reports to the target directory and creates metadata.json."""
        os.makedirs(self.export_dir, exist_ok=True)
        exported_files: List[str] = []

        file_mapping = {
            "resource_profiling": "resource_profile.json",
            "container_policy": "container_resource_policy_report.json",
            "cpu_capacity": "cpu_capacity.json",
            "memory_leak": "memory_analysis.json",
            "worker_capacity": "worker_capacity.json",
            "queue_capacity": "queue_capacity.json",
            "database_capacity": "database_capacity.json",
            "ai_resource_profile": "ai_profile.json",
            "capacity_modeling": "capacity_model.json",
            "autoscaling_readiness": "scaling_report.json",
            "resource_alerting": "alert_report.json",
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
            "phase": "3J.4",
            "name": "Enterprise Resource Utilization & Capacity Engineering Verification Framework",
            "environment": "Dedicated Performance Staging Sandbox",
            "commit": "HEAD",
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
