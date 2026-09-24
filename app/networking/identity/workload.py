"""Workload Attestation and SVID Verification."""

from __future__ import annotations

import base64
import hmac
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .certificates import CertificateManager
from .service_identity import SPIFFEIdentity


class SVIDType(str, Enum):
    X509 = "X509"
    JWT = "JWT"


@dataclass
class WorkloadSVID:
    svid_type: SVIDType
    spiffe_id: SPIFFEIdentity
    token_or_serial: str
    issued_at: float
    expires_at: float
    trust_bundle_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at


@dataclass
class AttestationEvidence:
    node_id: str
    pod_uid: Optional[str] = None
    container_id: Optional[str] = None
    platform: str = "kubernetes"
    attestation_token: str = ""
    attributes: Dict[str, Any] = field(default_factory=dict)


class WorkloadAttestationManager:
    """Attests workloads, validates SPIRE/SPIFFE trust bundles and generates SVIDs."""

    def __init__(
        self,
        cert_manager: Optional[CertificateManager] = None,
        signing_secret: str = "docutask-mesh-secret-key-32b",
        trust_domain: str = "docutask.internal",
    ):
        self.cert_manager = cert_manager or CertificateManager()
        self.signing_secret = signing_secret
        self.trust_domain = trust_domain
        self._trust_bundles: Dict[str, List[str]] = {
            self.trust_domain: [self.cert_manager.root_ca.serial_number]
        }
        self._svids: Dict[str, WorkloadSVID] = {}

    def attest_workload(
        self,
        service_name: str,
        namespace: str = "default",
        evidence: Optional[AttestationEvidence] = None,
        svid_type: SVIDType = SVIDType.X509,
        ttl_seconds: float = 3600.0,  # 1 hour short-lived SVID
    ) -> WorkloadSVID:
        """Attest a workload instance and issue an X509 or JWT SVID."""
        spiffe_id = SPIFFEIdentity(
            trust_domain=self.trust_domain,
            namespace=namespace,
            service_name=service_name,
        )

        now = time.time()
        expires_at = now + ttl_seconds

        if svid_type == SVIDType.X509:
            cert = self.cert_manager.issue_certificate(
                subject=f"CN={service_name}.{namespace}.svc.{self.trust_domain}",
                san_uris=[spiffe_id.uri],
                validity_seconds=ttl_seconds,
            )
            token_or_serial = cert.serial_number
        else:
            # Generate JWT-SVID representation with base64url encoding
            payload_str = f"{spiffe_id.uri}:{now}:{expires_at}:{uuid.uuid4().hex[:8]}"
            b64_payload = base64.urlsafe_b64encode(payload_str.encode()).decode().rstrip("=")
            sig = hmac.new(self.signing_secret.encode(), b64_payload.encode(), "sha256").hexdigest()
            token_or_serial = f"jwt-svid.{b64_payload}.{sig}"

        svid = WorkloadSVID(
            svid_type=svid_type,
            spiffe_id=spiffe_id,
            token_or_serial=token_or_serial,
            issued_at=now,
            expires_at=expires_at,
            trust_bundle_id=self.trust_domain,
            metadata={"node_id": evidence.node_id if evidence else "unknown"},
        )
        self._svids[token_or_serial] = svid
        return svid

    def validate_svid(self, token_or_serial: str, expected_spiffe_uri: Optional[str] = None) -> bool:
        """Validate an SVID's cryptographic authenticity, expiration, and trust bundle."""
        svid = self._svids.get(token_or_serial)
        if not svid or svid.is_expired:
            return False

        if expected_spiffe_uri and svid.spiffe_id.uri != expected_spiffe_uri:
            return False

        if svid.svid_type == SVIDType.X509:
            return self.cert_manager.verify_certificate(token_or_serial, expected_san=svid.spiffe_id.uri)
        else:
            # Verify JWT signature
            parts = token_or_serial.split(".")
            if len(parts) != 3 or parts[0] != "jwt-svid":
                return False
            b64_payload, sig = parts[1], parts[2]
            expected_sig = hmac.new(self.signing_secret.encode(), b64_payload.encode(), "sha256").hexdigest()
            return hmac.compare_digest(sig, expected_sig)

    def register_trust_bundle(self, trust_domain: str, root_ca_serials: List[str]) -> None:
        """Federate trust with an external trust domain."""
        self._trust_bundles[trust_domain] = root_ca_serials

    def get_trust_bundle(self, trust_domain: str) -> List[str]:
        return self._trust_bundles.get(trust_domain, [])
