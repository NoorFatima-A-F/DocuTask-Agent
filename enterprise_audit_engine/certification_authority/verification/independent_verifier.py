"""Independent Certificate Verifier for Zero-Repo Third-Party Due Diligence."""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timezone

from enterprise_audit_engine.certification_authority.domain.models import (
    CertificationRecord,
    CertificationStatus,
)
from enterprise_audit_engine.certification_authority.signing.verifier import CertificateSignatureVerifier
from enterprise_audit_engine.certification_authority.registry.revocation_registry import CertificationRevocationRegistry


class IndependentCertificateVerifier:
    """Verifies audit certificates completely independently without requiring source code repository access."""

    @classmethod
    def verify_certificate_file(
        cls,
        certificate_path: Path,
        public_key_path: Optional[Path] = None,
        merkle_manifest_path: Optional[Path] = None,
        revocation_registry_dir: Optional[Path] = None,
    ) -> Dict[str, Any]:
        if not certificate_path.exists():
            return {
                "is_valid": False,
                "status": "CERTIFICATE_FILE_NOT_FOUND",
                "error": f"Path '{certificate_path}' does not exist.",
            }

        try:
            with open(certificate_path, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                record = CertificationRecord.model_validate(data)
        except Exception as ex:
            return {
                "is_valid": False,
                "status": "INVALID_CERTIFICATE_SCHEMA",
                "error": f"Failed to parse certificate: {str(ex)}",
            }

        now = datetime.now(timezone.utc)
        issues = []

        # 1. Check Expiry
        is_expired = False
        try:
            expiry_dt = datetime.fromisoformat(record.expiry_timestamp)
            if now > expiry_dt:
                is_expired = True
                issues.append(f"Certificate expired on {record.expiry_timestamp} (current: {now.isoformat()}).")
        except Exception:
            issues.append("Invalid or unparseable expiry_timestamp.")

        # 2. Check Revocation Registry
        is_revoked = False
        revocation_details = None
        if revocation_registry_dir and revocation_registry_dir.exists():
            crl = CertificationRevocationRegistry(revocation_registry_dir)
            if crl.is_revoked(record.certificate_id):
                is_revoked = True
                rev_rec = crl.get_revocation(record.certificate_id)
                revocation_details = rev_rec.model_dump() if rev_rec else {}
                issues.append(f"Certificate {record.certificate_id} is REVOKED in registry. Reason: {revocation_details.get('reason')}")

        # 3. Cryptographic Signature Verification
        pub_key_pem = ""
        if public_key_path and public_key_path.exists():
            pub_key_pem = public_key_path.read_text(encoding="utf-8")
        else:
            pub_key_pem = record.public_key_pem

        if not pub_key_pem:
            issues.append("No public key provided or embedded in certificate.")
            sig_valid = False
        else:
            sig_valid = CertificateSignatureVerifier.verify_record_signature(record, pub_key_pem)
            if not sig_valid:
                issues.append("Cryptographic Ed25519 digital signature validation FAILED (tampered content or invalid key).")

        # 4. Merkle Root Match Verification (if manifest provided)
        merkle_valid = True
        if merkle_manifest_path and merkle_manifest_path.exists():
            try:
                with open(merkle_manifest_path, "r", encoding="utf-8") as fp:
                    m_data = json.load(fp)
                    manifest_root = m_data.get("merkle_root")
                    if manifest_root != record.merkle_root:
                        merkle_valid = False
                        issues.append(f"Merkle root mismatch: manifest ({manifest_root}) != certificate ({record.merkle_root})")
            except Exception as ex:
                merkle_valid = False
                issues.append(f"Failed to verify Merkle manifest: {str(ex)}")

        # 5. Critical Findings & Policy Verification
        has_critical = len(record.critical_findings) > 0
        if has_critical:
            issues.append(f"Certificate contains unresolved critical findings: {record.critical_findings}")

        is_valid = (
            sig_valid
            and not is_expired
            and not is_revoked
            and merkle_valid
            and not has_critical
        )

        final_status = "CERTIFIED" if is_valid else (
            "REVOKED" if is_revoked else (
                "EXPIRED" if is_expired else "INVALID_SIGNATURE_OR_TAMPERED"
            )
        )

        return {
            "is_valid": is_valid,
            "status": final_status,
            "certificate_id": record.certificate_id,
            "system_name": record.system_name,
            "release_version": record.release_version,
            "audit_engine_version": record.audit_engine_version,
            "issued_timestamp": record.issued_timestamp,
            "expiry_timestamp": record.expiry_timestamp,
            "eqi_score": record.eqi_score,
            "merkle_root": record.merkle_root,
            "signature_valid": sig_valid,
            "merkle_valid": merkle_valid,
            "is_expired": is_expired,
            "is_revoked": is_revoked,
            "issues_count": len(issues),
            "issues": issues,
            "revocation_details": revocation_details,
        }
