"""Software Supply Chain Signature Policy Engine (Req 23, 70, 71)."""
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set
from .sigstore_adapter import SigstoreCosignAdapter


@dataclass
class SupplyChainVerificationReport:
    """Detailed audit report of supply chain verification gates."""
    artifact_digest: str
    digest_valid: bool
    signature_valid: bool
    signer_trusted: bool
    sbom_present: bool
    provenance_present: bool
    security_scan_passed: bool
    passed: bool
    denial_reasons: List[str] = field(default_factory=list)


class SupplyChainPolicyEnforcer:
    """Enforces zero-trust supply-chain gate before allowing production deployment."""

    def __init__(
        self,
        sigstore: SigstoreCosignAdapter,
        trusted_identities: Optional[Set[str]] = None,
    ):
        self.sigstore = sigstore
        self.trusted_identities = trusted_identities or {
            "release-engineer@docutask.com",
            "https://github.com/docutask/actions@v1",
        }

    def verify_supply_chain(
        self,
        artifact_digest: str,
        has_sbom: bool,
        has_provenance: bool,
        security_scan_passed: bool,
    ) -> SupplyChainVerificationReport:
        denial_reasons: List[str] = []

        # 1. Digest validity
        digest_valid = artifact_digest.startswith("sha256:") and len(artifact_digest) == 71
        if not digest_valid:
            denial_reasons.append("Invalid artifact digest format")

        # 2. Cryptographic signature check
        sig_bundle = self.sigstore.get_signature(artifact_digest)
        signature_valid = self.sigstore.verify_signature(artifact_digest) if sig_bundle else False
        if not signature_valid:
            denial_reasons.append("Missing or cryptographically invalid artifact signature")

        # 3. Signer trust
        signer_trusted = sig_bundle.signer_identity in self.trusted_identities if sig_bundle else False
        if not signer_trusted:
            denial_reasons.append(f"Signer identity '{sig_bundle.signer_identity if sig_bundle else 'none'}' is not trusted")

        # 4. SBOM presence
        if not has_sbom:
            denial_reasons.append("Missing mandatory SBOM document")

        # 5. Provenance presence
        if not has_provenance:
            denial_reasons.append("Missing mandatory SLSA provenance attestation")

        # 6. Security scan
        if not security_scan_passed:
            denial_reasons.append("Critical or high severity vulnerabilities detected in security scan")

        passed = len(denial_reasons) == 0

        return SupplyChainVerificationReport(
            artifact_digest=artifact_digest,
            digest_valid=digest_valid,
            signature_valid=signature_valid,
            signer_trusted=signer_trusted,
            sbom_present=has_sbom,
            provenance_present=has_provenance,
            security_scan_passed=security_scan_passed,
            passed=passed,
            denial_reasons=denial_reasons,
        )
