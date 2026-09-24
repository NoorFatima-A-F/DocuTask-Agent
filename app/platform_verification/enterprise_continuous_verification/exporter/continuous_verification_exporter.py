"""
Phase 3Q: CI/CD Continuous Verification Pipeline Artifact Exporter.
"""

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Union

from app.core.security import resolve_safe_path, validate_safe_filename_segment
from ..domain.models import (
    BuildArtifactReport,
    ChangeImpactReport,
    ChaosPipelineReport,
    DisposableEnvReport,
    InfrastructureDriftReport,
    IntegrationWorkflowReport,
    ManifestEntry,
    PerformanceRegressionReport,
    ProductionReadinessCertificate,
    ReleaseDecision,
    SecurityGateReport,
    VerificationManifest,
)


class ContinuousVerificationExporter:
    """
    Exports structured pipeline evidence artifacts across the CI/CD lifecycle
    conforming to the Section 3Q.10 layout with SHA-256 integrity validation.
    """

    def __init__(self, base_dir: Optional[Union[str, Path]] = None):
        self.set_base_dir(base_dir or "pipeline_evidence")

    def set_base_dir(self, base_dir: Union[str, Path]) -> None:
        self.base_dir = Path(base_dir) if base_dir else Path.cwd() / "pipeline_evidence"
        self.build_dir = self.base_dir / "build"
        self.security_dir = self.base_dir / "security"
        self.infra_dir = self.base_dir / "infrastructure"
        self.perf_dir = self.base_dir / "performance"
        self.chaos_dir = self.base_dir / "chaos"
        self.deploy_dir = self.base_dir / "deployment"
        self.cert_dir = self.base_dir / "certification"

        for d in [self.build_dir, self.security_dir, self.infra_dir, self.perf_dir, self.chaos_dir, self.deploy_dir, self.cert_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def _compute_sha256(self, file_path: Union[str, Path]) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def export_all(
        self,
        change_impact: ChangeImpactReport,
        build: BuildArtifactReport,
        security: SecurityGateReport,
        disposable_env: DisposableEnvReport,
        integration: IntegrationWorkflowReport,
        performance: PerformanceRegressionReport,
        chaos: ChaosPipelineReport,
        drift: InfrastructureDriftReport,
        decision: ReleaseDecision,
        certificate: ProductionReadinessCertificate,
        export_dir: Optional[Union[str, Path]] = None,
    ) -> VerificationManifest:
        if export_dir is not None:
            self.set_base_dir(export_dir)

        # 1. Build & Security
        with open(self.build_dir / "build_report.json", "w", encoding="utf-8") as f:
            json.dump(build.model_dump(), f, indent=2, default=str)

        with open(self.security_dir / "security_gate_report.json", "w", encoding="utf-8") as f:
            json.dump(security.model_dump(), f, indent=2, default=str)

        # 2. Infrastructure & Drift
        with open(self.infra_dir / "change_impact_report.json", "w", encoding="utf-8") as f:
            json.dump(change_impact.model_dump(), f, indent=2, default=str)

        with open(self.infra_dir / "drift_report.json", "w", encoding="utf-8") as f:
            json.dump(drift.model_dump(), f, indent=2, default=str)

        # 3. Performance & Chaos
        with open(self.perf_dir / "performance_regression_report.json", "w", encoding="utf-8") as f:
            json.dump(performance.model_dump(), f, indent=2, default=str)

        with open(self.chaos_dir / "chaos_pipeline_report.json", "w", encoding="utf-8") as f:
            json.dump(chaos.model_dump(), f, indent=2, default=str)

        # 4. Deployment
        with open(self.deploy_dir / "disposable_env_report.json", "w", encoding="utf-8") as f:
            json.dump(disposable_env.model_dump(), f, indent=2, default=str)

        with open(self.deploy_dir / "integration_report.json", "w", encoding="utf-8") as f:
            json.dump(integration.model_dump(), f, indent=2, default=str)

        # 5. Certification & Release
        with open(self.cert_dir / "release_decision.json", "w", encoding="utf-8") as f:
            json.dump(decision.model_dump(), f, indent=2, default=str)

        with open(self.cert_dir / "production_readiness_certificate.json", "w", encoding="utf-8") as f:
            json.dump(certificate.model_dump(), f, indent=2, default=str)

        # 6. Build Manifest
        entries: List[ManifestEntry] = []
        for root, _, files in os.walk(self.base_dir):
            for file_name in sorted(files):
                if file_name in ["metadata.json", "manifest.json"]:
                    continue
                full_p = Path(root) / file_name
                rel_p = str(full_p.relative_to(self.base_dir)).replace("\\", "/")
                sha = self._compute_sha256(full_p)
                entries.append(
                    ManifestEntry(
                        filename=rel_p,
                        report_title=full_p.stem.replace("_", " ").title(),
                        sha256=sha,
                        size_bytes=full_p.stat().st_size,
                    )
                )

        manifest = VerificationManifest(
            project="DocuTask-Agent",
            framework="Enterprise Continuous Infrastructure Verification & CI/CD Pipeline",
            version=decision.release_version,
            commit=build.commit_hash,
            environment="CI/CD Ephemeral Production Assurance Environment",
            timestamp=datetime.now(timezone.utc).isoformat(),
            overall_score=decision.confidence_score,
            decision=decision.decision.value,
            deployment_approved=decision.decision.value == "APPROVED",
            files=entries,
        )

        manifest_data = manifest.model_dump()
        for mf_name in ["metadata.json", "manifest.json"]:
            with open(self.base_dir / mf_name, "w", encoding="utf-8") as f:
                json.dump(manifest_data, f, indent=2, default=str)

        return manifest
