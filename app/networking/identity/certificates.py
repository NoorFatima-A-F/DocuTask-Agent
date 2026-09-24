"""X.509 Certificate and Multi-Backend Certificate Management."""

from __future__ import annotations

import hashlib
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class CertificateBackend(str, Enum):
    IN_MEMORY = "IN_MEMORY"
    VAULT = "VAULT"
    KUBERNETES_CSR = "KUBERNETES_CSR"
    CLOUD_CAS = "CLOUD_CAS"


@dataclass
class X509Certificate:
    serial_number: str
    subject: str
    issuer: str
    valid_from: float
    valid_to: float
    san_uris: List[str] = field(default_factory=list)
    cert_pem: str = ""
    private_key_pem: str = ""
    is_ca: bool = False
    revoked: bool = False
    revocation_reason: Optional[str] = None
    created_at: float = field(default_factory=time.time)

    @property
    def is_expired(self) -> bool:
        return time.time() > self.valid_to

    @property
    def is_active(self) -> bool:
        now = time.time()
        return not self.revoked and (self.valid_from <= now <= self.valid_to)


class CertificateManager:
    """Manages Root/Intermediate CA and dynamic leaf certificate issuance."""

    def __init__(
        self,
        backend: CertificateBackend = CertificateBackend.IN_MEMORY,
        ca_subject: str = "CN=DocuTask Root CA,O=DocuTask,C=US",
    ):
        self.backend = backend
        self.ca_subject = ca_subject
        self._certificates: Dict[str, X509Certificate] = {}
        self._root_ca = self._generate_root_ca()

    @property
    def root_ca(self) -> X509Certificate:
        return self._root_ca

    def _generate_root_ca(self) -> X509Certificate:
        serial = f"ca-{uuid.uuid4().hex[:12]}"
        now = time.time()
        cert = X509Certificate(
            serial_number=serial,
            subject=self.ca_subject,
            issuer=self.ca_subject,
            valid_from=now - 3600.0,
            valid_to=now + (365 * 86400.0 * 10),  # 10 years
            san_uris=["spiffe://docutask.internal/root-ca"],
            cert_pem=f"-----BEGIN CERTIFICATE-----\nMIIB_ROOT_CA_{serial}\n-----END CERTIFICATE-----",
            private_key_pem=f"-----BEGIN PRIVATE KEY-----\nMIIE_ROOT_KEY_{serial}\n-----END PRIVATE KEY-----",
            is_ca=True,
        )
        self._certificates[serial] = cert
        return cert

    def issue_certificate(
        self,
        subject: str,
        san_uris: List[str],
        validity_seconds: float = 86400.0 * 30,  # 30 days default
        issuer_cert: Optional[X509Certificate] = None,
    ) -> X509Certificate:
        """Issue a leaf X.509 certificate signed by CA."""
        issuer = issuer_cert or self._root_ca
        serial = f"cert-{uuid.uuid4().hex[:12]}"
        now = time.time()
        cert = X509Certificate(
            serial_number=serial,
            subject=subject,
            issuer=issuer.subject,
            valid_from=now,
            valid_to=now + validity_seconds,
            san_uris=san_uris,
            cert_pem=f"-----BEGIN CERTIFICATE-----\nMIIB_LEAF_{serial}_{hashlib.sha256(subject.encode()).hexdigest()[:8]}\n-----END CERTIFICATE-----",
            private_key_pem=f"-----BEGIN PRIVATE KEY-----\nMIIE_LEAF_KEY_{serial}\n-----END PRIVATE KEY-----",
            is_ca=False,
        )
        self._certificates[serial] = cert
        return cert

    def get_certificate(self, serial_number: str) -> Optional[X509Certificate]:
        return self._certificates.get(serial_number)

    def rotate_certificate(
        self,
        serial_number: str,
        renew_seconds: float = 86400.0 * 30,
    ) -> Optional[X509Certificate]:
        """Rotate an existing certificate seamlessly before expiration."""
        old_cert = self.get_certificate(serial_number)
        if not old_cert:
            return None

        new_cert = self.issue_certificate(
            subject=old_cert.subject,
            san_uris=old_cert.san_uris,
            validity_seconds=renew_seconds,
        )
        # Mark old certificate as rotated/revoked
        old_cert.revoked = True
        old_cert.revocation_reason = f"Rotated into {new_cert.serial_number}"
        return new_cert

    def revoke_certificate(self, serial_number: str, reason: str = "KeyCompromise") -> bool:
        """Revoke a certificate."""
        cert = self._certificates.get(serial_number)
        if cert:
            cert.revoked = True
            cert.revocation_reason = reason
            return True
        return False

    def verify_certificate(self, cert_serial: str, expected_san: Optional[str] = None) -> bool:
        """Verify certificate validity, non-revocation, and optional SAN match."""
        cert = self._certificates.get(cert_serial)
        if not cert or not cert.is_active:
            return False
        if expected_san and expected_san not in cert.san_uris:
            return False
        return True

    def list_certificates(self, active_only: bool = False) -> List[X509Certificate]:
        certs = list(self._certificates.values())
        if active_only:
            certs = [c for c in certs if c.is_active]
        return certs
