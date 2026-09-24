"""Phase 3J.8: Autoscaling Evidence Exporter with SHA-256 Integrity Manifest."""

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, List

from ..domain.interfaces import IAutoscalingExporter
from ..domain.models import (
    AutoscalingVerificationManifest,
    EnterpriseAutoscalingCertificationReport,
)


class AutoscalingExporter(IAutoscalingExporter):

    PHASE_TO_FILENAME_MAP: Dict[str, str] = {
        "3j.8.1": "autoscaling_architecture.json",
        "3j.8.2": "scaling_metrics.json",
        "3j.8.3": "worker_scaling.json",
        "3j.8.4": "queue_scaling.json",
        "3j.8.5": "api_scaling.json",
        "3j.8.6": "scaling_policy.json",
        "3j.8.7": "scale_up_report.json",
        "3j.8.8": "scale_down_report.json",
        "3j.8.9": "database_scaling_limit.json",
        "3j.8.10": "ai_scaling_report.json",
        "3j.8.11": "kubernetes_scaling_readiness.json",
        "3j.8.12": "cloud_scaling_compatibility.json",
        "3j.8.13": "cost_analysis.json",
        "3j.8.14": "failure_simulation.json",
    }

    ALIASES_MAP: Dict[str, str] = {
        "autoscaling_architecture.json": "autoscaling_architecture_report.json",
        "scaling_metrics.json": "scaling_metrics_report.json",
        "worker_scaling.json": "worker_scaling_report.json",
        "queue_scaling.json": "queue_autoscaling_report.json",
        "api_scaling.json": "api_scaling_report.json",
        "scaling_policy.json": "scaling_policy_report.json",
        "scale_up_report.json": "scale_up_validation_report.json",
        "scale_down_report.json": "scale_down_safety_report.json",
        "database_scaling_limit.json": "database_scaling_limit_report.json",
        "kubernetes_scaling_readiness.json": "kubernetes_scaling_readiness_report.json",
        "cloud_scaling_compatibility.json": "cloud_scaling_compatibility_report.json",
        "cost_analysis.json": "scaling_cost_efficiency_report.json",
        "failure_simulation.json": "scaling_failure_report.json",
    }

    def _resolve_filename(self, key: str, report: Any) -> str:
        candidates = [key]
        if hasattr(report, "verifier_id") and report.verifier_id:
            candidates.append(report.verifier_id)
        if hasattr(report, "phase_id") and report.phase_id:
            candidates.append(report.phase_id)

        for cand in candidates:
            match = re.search(r"3j\.8\.\d+", str(cand), re.IGNORECASE)
            if match:
                phase_key = match.group(0).lower()
                if phase_key in self.PHASE_TO_FILENAME_MAP:
                    return self.PHASE_TO_FILENAME_MAP[phase_key]

        return f"report_{key.replace('.', '_').replace('-', '_')}.json"

    def export(
        self,
        reports: Dict[str, Any],
        certification: EnterpriseAutoscalingCertificationReport,
        output_dir: str = "performance_scaling_verification",
    ) -> List[str]:
        manifest = self.export_all(reports, certification, output_dir=output_dir)
        return manifest.reports_generated

    def export_all(
        self,
        reports: Dict[str, Any],
        certification: EnterpriseAutoscalingCertificationReport,
        output_dir: str = "performance_scaling_verification",
    ) -> AutoscalingVerificationManifest:
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

        manifest = AutoscalingVerificationManifest(
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
