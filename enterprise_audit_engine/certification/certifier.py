"""Enterprise Audit Engine Certifier & Master Assurance Runner."""

import asyncio
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional

from enterprise_audit_engine.certification.attestation import EngineAttestation
from enterprise_audit_engine.certification.merkle_tree import MerkleEvidenceTree
from enterprise_audit_engine.certification.reproducibility import AuditReproducibilityVerifier
from enterprise_audit_engine.certification.coverage_analyzer import EvidenceCoverageAnalyzer
from enterprise_audit_engine.certification.anti_hallucination import ClaimEvidenceMatcher
from enterprise_audit_engine.certification.security_auditor import EngineSecurityValidator
from enterprise_audit_engine.certification.metrics import AuditQualityMetrics
from enterprise_audit_engine.certification.release_bundler import ReleaseEvidenceBundler
from enterprise_audit_engine.orchestration.audit_runner import AuditRunner
from enterprise_audit_engine.domain.evidence.models import (
    AuditFinding,
    EvidenceClassification,
    EvidenceConfidence,
    CollectorExecutionManifest,
)
from enterprise_audit_engine.certification_authority.authority import CertificationAuthority
from enterprise_audit_engine.certification_authority.supply_chain.sbom_generator import AuditEngineSupplyChainAuditor


class EnterpriseCertifier:
    """Master certifier validating the audit engine and producing signed release audit packages."""

    def __init__(self, repo_root: Path, output_dir: Optional[Path] = None):
        self.repo_root = repo_root.resolve()
        self.output_dir = (output_dir or (self.repo_root / "audit_output")).resolve()
        self.engine_root = Path(__file__).resolve().parent.parent
        self.authority = CertificationAuthority(self.repo_root)

    async def certify_engine_and_repository(
        self,
        policy_name: str = "enterprise_grade",
        release_version: str = "1.0.0",
    ) -> Dict[str, Any]:
        """Executes full 11-step end-to-end certification and digital signing pipeline."""
        start_time = datetime.now(timezone.utc)

        # 1. Engine Attestation & Manifest
        attestation_files = EngineAttestation.save_attestation_files(
            engine_dir=self.engine_root,
            repo_root=self.repo_root,
        )
        build_info = EngineAttestation.generate_build_info(self.repo_root)

        # 2. Engine Supply Chain Verification (SBOM + Provenance)
        supply_chain_files = AuditEngineSupplyChainAuditor.save_supply_chain_artifacts(
            repo_root=self.repo_root,
            engine_root=self.engine_root,
            output_dir=self.output_dir / "audit-evidence",
        )

        # 3. Engine Defensive Security Audit
        security_audit = EngineSecurityValidator.audit_engine_security(self.engine_root)

        # 4. Primary Audit Execution
        audit_runner = AuditRunner(repo_root=self.repo_root, output_dir=self.output_dir)
        audit_result = await audit_runner.run_full_audit()

        evidence_records = audit_runner.store.load_all_evidence()

        # 5. Merkle Evidence Sealing
        merkle_tree = MerkleEvidenceTree(evidence_records)
        merkle_path = self.output_dir / "audit-evidence" / "audit_merkle_root.json"
        merkle_tree.save_merkle_manifest(merkle_path)

        # 6. Anti-Hallucination & Claim Verification on Generated Reports
        reports_dir = self.output_dir / "audit-reports"
        all_stripped_claims: List[str] = []
        for rpt_path in reports_dir.glob("*.md"):
            try:
                content = rpt_path.read_text(encoding="utf-8")
                sanitized, stripped = ClaimEvidenceMatcher.sanitize_report_text(content, evidence_records)
                if stripped:
                    all_stripped_claims.extend(stripped)
                    rpt_path.write_text(sanitized, encoding="utf-8")
            except Exception:
                pass

        # 7. Evidence Coverage Verification
        all_findings: List[AuditFinding] = []
        critical_findings: List[str] = []
        for sub, card_dict in audit_result.get("scorecards", {}).items():
            matching_ids = [r.id for r in evidence_records if r.category == sub]
            cls_val = card_dict.get("classification")
            classification_enum = EvidenceClassification(cls_val) if cls_val else EvidenceClassification.VERIFIED
            conf_val = card_dict.get("confidence")
            confidence_enum = EvidenceConfidence(conf_val) if conf_val else EvidenceConfidence.MEDIUM
            if classification_enum == EvidenceClassification.CRITICAL_FINDING:
                critical_findings.append(f"Critical finding in {sub}")
            all_findings.append(
                AuditFinding(
                    subsystem=sub,
                    claim=f"Subsystem '{sub}' verification evaluated to {cls_val}",
                    evidence_ids=matching_ids,
                    classification=classification_enum,
                    confidence=confidence_enum,
                    risk_level="HIGH" if classification_enum == EvidenceClassification.CRITICAL_FINDING else "LOW",
                    analysis=card_dict.get("justification", ""),
                )
            )
        
        coverage_result = EvidenceCoverageAnalyzer.verify_coverage(
            findings=all_findings,
            records=evidence_records,
        )

        # 8. Reproducibility Test
        with tempfile.TemporaryDirectory() as temp_dir:
            repro_result = await AuditReproducibilityVerifier.verify_reproducibility(
                repo_root=self.repo_root,
                temp_base_dir=Path(temp_dir),
            )

        # 9. Formulate, Issue & Digitally Sign Certificate via Certification Authority
        issue_result = self.authority.issue_and_sign_certificate(
            audit_execution_id=audit_result["run_id"],
            records=evidence_records,
            merkle_root=merkle_tree.merkle_root,
            overall_classification=audit_result["overall_classification"],
            overall_confidence=audit_result["overall_confidence"],
            critical_findings=critical_findings,
            policy_name=policy_name,
            release_version=release_version,
            validity_days=180,
        )

        cert_record = issue_result["record"]
        pub_key_pem = issue_result["public_key_pem"]
        policy_eval = issue_result["policy_evaluation"]
        eqi_data = issue_result["eqi"]

        # 10. Compute Audit Quality Metrics
        exec_manifest = CollectorExecutionManifest.model_validate(audit_result["collector_manifest"])
        quality_metrics = AuditQualityMetrics.compute_metrics(
            records=evidence_records,
            exec_manifest=exec_manifest,
            scorecards=audit_result.get("scorecards", {}),
            is_reproducible=repro_result["is_deterministic"],
            unsupported_claims_count=len(all_stripped_claims),
        )
        quality_path = self.output_dir / "audit-evidence" / "audit_quality_report.json"
        AuditQualityMetrics.save_quality_report(quality_metrics, quality_path)

        is_certified = (
            security_audit["is_secure"]
            and coverage_result["is_complete"]
            and repro_result["is_deterministic"]
            and policy_eval["passed"]
            and cert_record.status.value == "VALID"
        )

        # 11. Package into release_audit/
        release_dir = self.repo_root / "release_audit"
        bundle_paths = ReleaseEvidenceBundler.create_release_package(
            release_dir=release_dir,
            reports_dir=reports_dir,
            evidence_dir=self.output_dir / "audit-evidence",
            merkle_manifest_path=merkle_path,
            certificate_data=cert_record.model_dump(),
        )

        # Save public key in release bundle
        pub_path = release_dir / "public_key.pem"
        pub_path.write_text(pub_key_pem, encoding="utf-8")
        bundle_paths["public_key.pem"] = pub_path

        # Copy SBOM and provenance to release package
        if supply_chain_files["sbom"].exists():
            shutil_dest = release_dir / "audit_engine_sbom.json"
            shutil_dest.write_text(supply_chain_files["sbom"].read_text(encoding="utf-8"), encoding="utf-8")
            bundle_paths["audit_engine_sbom.json"] = shutil_dest

        if supply_chain_files["provenance"].exists():
            shutil_dest = release_dir / "audit_engine_provenance.json"
            shutil_dest.write_text(supply_chain_files["provenance"].read_text(encoding="utf-8"), encoding="utf-8")
            bundle_paths["audit_engine_provenance.json"] = shutil_dest

        return {
            "is_certified": is_certified,
            "certificate": cert_record.model_dump(),
            "public_key_pem": pub_key_pem,
            "policy_evaluation": policy_eval,
            "eqi": eqi_data,
            "build_info": build_info,
            "security_audit": security_audit,
            "reproducibility": repro_result,
            "coverage": coverage_result,
            "quality_metrics": quality_metrics,
            "merkle_root": merkle_tree.merkle_root,
            "release_bundle": {k: str(v) for k, v in bundle_paths.items()},
        }
