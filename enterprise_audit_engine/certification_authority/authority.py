"""Enterprise Audit Certification Authority (ACA) Master Controller."""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from enterprise_audit_engine.certification_authority.domain.models import (
    CertificationRecord,
    CertificationStatus,
    RevocationReason,
)
from enterprise_audit_engine.certification_authority.signing.signer import CertificateSigner
from enterprise_audit_engine.certification_authority.policy.policy_engine import CertificationPolicyEngine
from enterprise_audit_engine.certification_authority.metrics.eqi_calculator import EvidenceQualityIndexCalculator
from enterprise_audit_engine.certification_authority.registry.audit_registry import AuditRegistry
from enterprise_audit_engine.certification_authority.registry.revocation_registry import CertificationRevocationRegistry
from enterprise_audit_engine.certification_authority.registry.regression_detector import AuditRegressionDetector
from enterprise_audit_engine.certification_authority.verification.independent_verifier import IndependentCertificateVerifier
from enterprise_audit_engine.certification_authority.exporter.review_package_exporter import ExternalReviewPackageExporter
from enterprise_audit_engine.domain.evidence.models import EvidenceRecord


class CertificationAuthority:
    """Master Authority issuing, digitally signing, verifying, and managing certification lifecycles."""

    def __init__(self, repo_root: Path, registry_dir: Optional[Path] = None):
        self.repo_root = repo_root.resolve()
        self.registry_dir = (registry_dir or (self.repo_root / ".audit_registry")).resolve()
        self.registry = AuditRegistry(self.registry_dir)
        self.revocations = CertificationRevocationRegistry(self.registry_dir)

    def issue_and_sign_certificate(
        self,
        audit_execution_id: str,
        records: List[EvidenceRecord],
        merkle_root: str,
        overall_classification: str,
        overall_confidence: str,
        critical_findings: List[str],
        policy_name: str = "enterprise_grade",
        release_version: str = "1.0.0",
        validity_days: int = 180,
    ) -> Dict[str, Any]:
        """Evaluates policy, computes EQI, issues and signs an Ed25519 CertificationRecord."""
        
        # 1. Compute EQI Breakdown
        active_domains = list({r.category for r in records})
        eqi_breakdown = EvidenceQualityIndexCalculator.calculate_eqi(
            records=records,
            coverage_pct=100.0,
            is_reproducible=True,
        )

        # 2. Policy Evaluation
        policy_eval = CertificationPolicyEngine.evaluate_policy(
            policy_name=policy_name,
            overall_confidence=overall_confidence,
            overall_classification=overall_classification,
            critical_findings=critical_findings,
            eqi=eqi_breakdown,
            is_reproducible=True,
            active_domains=active_domains,
        )

        cert_id = f"CERT-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        pending_record = CertificationRecord.create_pending(
            certificate_id=cert_id,
            system_name="DocuTask Agent",
            release_version=release_version,
            audit_engine_version="2.1.0",
            audit_execution_id=audit_execution_id,
            merkle_root=merkle_root,
            evidence_root_hash=merkle_root,
            validity_days=validity_days,
            classification_summary={r.category: r.classification.value for r in records},
            critical_findings=critical_findings,
            eqi_score=eqi_breakdown.total_eqi,
            eqi_breakdown=eqi_breakdown,
            policy_name=policy_name,
            policy_compliance=policy_eval["passed"],
        )

        # 3. Digital Signing with Ed25519
        signed_record, pub_key_pem = CertificateSigner.sign_certificate(pending_record)
        
        # Set status based on policy pass
        if not policy_eval["passed"]:
            signed_record = signed_record.model_copy(update={"status": CertificationStatus.FAILED_VERIFICATION})

        # 4. Register in AuditRegistry
        self.registry.register_certificate(signed_record)

        return {
            "record": signed_record,
            "public_key_pem": pub_key_pem,
            "policy_evaluation": policy_eval,
            "eqi": eqi_breakdown.model_dump(),
        }

    def verify_certificate(
        self,
        certificate_path: Path,
        public_key_path: Optional[Path] = None,
        merkle_manifest_path: Optional[Path] = None,
    ) -> Dict[str, Any]:
        """Runs independent certificate verification."""
        return IndependentCertificateVerifier.verify_certificate_file(
            certificate_path=certificate_path,
            public_key_path=public_key_path,
            merkle_manifest_path=merkle_manifest_path,
            revocation_registry_dir=self.registry_dir,
        )

    def revoke_certificate(
        self,
        certificate_id: str,
        reason: RevocationReason,
        details: str,
    ) -> Dict[str, Any]:
        """Revokes an issued certificate."""
        rev_rec = self.revocations.revoke_certificate(certificate_id, reason, details)
        return {
            "status": "REVOKED",
            "revocation": rev_rec.model_dump(),
        }

    def export_review_package(
        self,
        output_dir: Path,
        record: CertificationRecord,
        public_key_pem: str,
        evidence_dir: Path,
        reports_dir: Path,
        merkle_manifest_path: Path,
    ) -> Dict[str, Path]:
        """Packages standalone bundle for external auditors."""
        return ExternalReviewPackageExporter.export_review_package(
            output_dir=output_dir,
            record=record,
            public_key_pem=public_key_pem,
            evidence_dir=evidence_dir,
            reports_dir=reports_dir,
            merkle_manifest_path=merkle_manifest_path,
        )

    def compare_releases(self, v1: str, v2: str) -> Dict[str, Any]:
        """Compares two historical release audits."""
        cert_1 = self.registry.get_certificate(v1)
        cert_2 = self.registry.get_certificate(v2)

        if not cert_1:
            return {"error": f"Certificate for version '{v1}' not found in registry."}
        if not cert_2:
            return {"error": f"Certificate for version '{v2}' not found in registry."}

        return AuditRegressionDetector.compare_certifications(cert_1, cert_2)
