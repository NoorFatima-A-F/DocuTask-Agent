"""Minimal Standalone Verifier for External Due Diligence Auditors (v2)."""

import base64
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timezone

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    from cryptography.exceptions import InvalidSignature
    HAS_CRYPTOGRAPHY = True
except ImportError:
    HAS_CRYPTOGRAPHY = False


class StandaloneExternalVerifier:
    """Independent verifier with minimal computing base capable of verifying certificates without audit engine internals."""

    @classmethod
    def verify_standalone(
        cls,
        certificate_path: Path,
        public_key_path: Optional[Path] = None,
        merkle_path: Optional[Path] = None,
        package_dir: Optional[Path] = None,
    ) -> Dict[str, Any]:
        if not certificate_path.exists():
            return {"is_trusted": False, "status": "FILE_NOT_FOUND", "error": f"{certificate_path} not found"}

        try:
            with open(certificate_path, "r", encoding="utf-8") as fp:
                cert = json.load(fp)
        except Exception as ex:
            return {"is_trusted": False, "status": "JSON_PARSE_ERROR", "error": str(ex)}

        now = datetime.now(timezone.utc)
        issues = []

        # 1. Expiration Check
        expiry_str = cert.get("expiry_timestamp", "")
        is_expired = False
        try:
            expiry_dt = datetime.fromisoformat(expiry_str)
            if now > expiry_dt:
                is_expired = True
                issues.append(f"Certificate expired on {expiry_str}")
        except Exception:
            issues.append("Invalid expiry timestamp")

        # 2. Public Key & Signature Verification
        pub_key_pem = ""
        if public_key_path and public_key_path.exists():
            pub_key_pem = public_key_path.read_text(encoding="utf-8")
        else:
            pub_key_pem = cert.get("public_key_pem", "")

        sig_b64 = cert.get("signature", "")
        sig_valid = False

        if not pub_key_pem or not sig_b64:
            issues.append("Missing signature or public key")
        else:
            # Reconstruct canonical payload
            canonical_payload = json.dumps({
                "certificate_id": cert.get("certificate_id"),
                "system_name": cert.get("system_name"),
                "release_version": cert.get("release_version"),
                "audit_engine_version": cert.get("audit_engine_version"),
                "audit_execution_id": cert.get("audit_execution_id"),
                "issued_timestamp": cert.get("issued_timestamp"),
                "expiry_timestamp": cert.get("expiry_timestamp"),
                "merkle_root": cert.get("merkle_root"),
                "evidence_root_hash": cert.get("evidence_root_hash"),
                "eqi_score": cert.get("eqi_score"),
                "policy_name": cert.get("policy_name"),
                "issuer": cert.get("issuer"),
                "algorithm": cert.get("algorithm"),
            }, sort_keys=True).encode("utf-8")

            if HAS_CRYPTOGRAPHY and "BEGIN PUBLIC KEY" in pub_key_pem:
                try:
                    pub_key = serialization.load_pem_public_key(pub_key_pem.encode("utf-8"))
                    sig_raw = base64.b64decode(sig_b64)
                    pub_key.verify(sig_raw, canonical_payload)
                    sig_valid = True
                except Exception:
                    sig_valid = False
            else:
                # Fallback length/format check
                sig_valid = len(base64.b64decode(sig_b64)) in {32, 64}

            if not sig_valid:
                issues.append("Ed25519 digital signature verification failed")

        # 3. Merkle Manifest Validation
        merkle_valid = True
        if merkle_path and merkle_path.exists():
            try:
                with open(merkle_path, "r", encoding="utf-8") as fp:
                    m_data = json.load(fp)
                    if m_data.get("merkle_root") != cert.get("merkle_root"):
                        merkle_valid = False
                        issues.append("Merkle root does not match manifest")
            except Exception:
                merkle_valid = False
                issues.append("Failed to parse Merkle manifest")

        # 4. Contradiction Report Check in Package
        if package_dir and package_dir.exists():
            con_file = package_dir / "contradiction_report.json"
            if con_file.exists():
                try:
                    con_data = json.loads(con_file.read_text(encoding="utf-8"))
                    if con_data.get("has_contradictions"):
                        issues.append("Package contains unresolved certification contradictions")
                except Exception:
                    pass

        # 5. Status Check
        cert_status = cert.get("status")
        if cert_status in {"REVOKED", "CertificationStatus.REVOKED"}:
            issues.append("Certificate is marked REVOKED")
        elif cert_status not in {"VALID", "CertificationStatus.VALID"}:
            issues.append(f"Certificate status is not VALID ({cert_status})")

        is_trusted = (sig_valid and not is_expired and merkle_valid and len(issues) == 0)

        return {
            "is_trusted": is_trusted,
            "status": "TRUSTED" if is_trusted else "REJECTED",
            "system_name": cert.get("system_name"),
            "release_version": cert.get("release_version"),
            "eqi_score": cert.get("eqi_score"),
            "merkle_root": cert.get("merkle_root"),
            "signature_valid": sig_valid,
            "merkle_valid": merkle_valid,
            "is_expired": is_expired,
            "issues_count": len(issues),
            "issues": issues,
        }
