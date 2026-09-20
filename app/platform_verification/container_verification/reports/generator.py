"""
Container Verification Evidence Generator and Report Compiler.
"""
import hashlib
import json
from pathlib import Path
from typing import Dict, Any
from app.platform_verification.container_verification.models.verification_models import (
    ContainerVerificationEvidencePackage,
    ContainerCertificationReport,
    ContainerCertificationTier,
)
from app.platform_verification.container_verification.reports.schemas import serialize_evidence_package


class ContainerEvidenceGenerator:
    """Compiles all verification results into sealed JSON artifacts and calculates final certification score."""

    # Weights: Architecture (20%), Security (25%), Reproducibility (15%), Isolation (15%), Runtime Reliability (15%), Efficiency (10%)
    WEIGHT_ARCH = 0.20
    WEIGHT_SEC = 0.25
    WEIGHT_REPRO = 0.15
    WEIGHT_ISO = 0.15
    WEIGHT_RELIABILITY = 0.15
    WEIGHT_EFFICIENCY = 0.10

    def calculate_certification_score(
        self,
        arch_pass: bool,
        security_rep,
        repro_rep,
        boundary_rep,
        runtime_rep,
        failure_rep,
        efficiency_rep,
    ) -> ContainerCertificationReport:
        arch_s = 100.0 if arch_pass else 60.0

        sec_deductions = (security_rep.critical_vulnerabilities * 40.0) + (security_rep.high_vulnerabilities * 15.0)
        sec_s = max(0.0, 100.0 - sec_deductions)

        repro_s = 100.0 if repro_rep.is_deterministic else 50.0
        iso_s = boundary_rep.isolation_score * 100.0

        rel_s = 100.0 if runtime_rep.status == "PASS" and failure_rep.status == "PASS" else 70.0
        eff_s = 100.0 if efficiency_rep.meets_efficiency_target else 75.0

        composite = (
            (arch_s * self.WEIGHT_ARCH)
            + (sec_s * self.WEIGHT_SEC)
            + (repro_s * self.WEIGHT_REPRO)
            + (iso_s * self.WEIGHT_ISO)
            + (rel_s * self.WEIGHT_RELIABILITY)
            + (eff_s * self.WEIGHT_EFFICIENCY)
        )
        composite = round(composite, 2)

        if composite >= 95.0 and security_rep.critical_vulnerabilities == 0:
            tier = ContainerCertificationTier.ENTERPRISE_CONTAINER_READY
        elif composite >= 90.0:
            tier = ContainerCertificationTier.PRODUCTION_READY
        elif composite >= 80.0:
            tier = ContainerCertificationTier.NEEDS_IMPROVEMENT
        else:
            tier = ContainerCertificationTier.FAILED

        return ContainerCertificationReport(
            architecture_quality_score=round(arch_s, 2),
            security_score=round(sec_s, 2),
            reproducibility_score=round(repro_s, 2),
            isolation_score=round(iso_s, 2),
            runtime_reliability_score=round(rel_s, 2),
            efficiency_score=round(eff_s, 2),
            composite_score=composite,
            tier=tier,
        )

    def export_results_directory(self, package: ContainerVerificationEvidencePackage, output_dir: str) -> str:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        data = serialize_evidence_package(package)
        for key, val in data.items():
            if key not in ["package_id", "commit_sha", "package_sha256", "created_at"]:
                filename = f"{key}.json"
                with open(out_path / filename, "w", encoding="utf-8") as f:
                    json.dump(val, f, indent=2)

        meta = {
            "repository": "DocuTask-Agent",
            "commit": package.commit_sha,
            "package_id": package.package_id,
            "created_at": package.created_at,
            "package_sha256": package.package_sha256,
        }
        with open(out_path / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        return str(out_path)
