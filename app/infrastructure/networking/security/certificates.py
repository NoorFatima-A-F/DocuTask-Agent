"""Certificate Authority (CA) Manager, X.509 Rotation, and Trust Bundles."""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
import hashlib
import threading
from typing import Any, Dict, List, Optional, Set
import uuid

from ..control_plane.registry import CertificateStatus


@dataclass
class X509Certificate:
    """Represents an X.509 certificate and private key bundle."""
    cert_id: str
    subject_cn: str
    san_dns_names: List[str]
    san_spiffe_ids: List[str]
    issuer_cn: str
    serial_number: str
    fingerprint_sha256: str
    status: CertificateStatus = CertificateStatus.ACTIVE
    issued_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(days=90))
    cert_pem: str = ""
    private_key_pem: str = ""
    is_ca: bool = False

    @property
    def is_expired(self) -> bool:
        """Check if certificate has exceeded expiration timestamp."""
        return datetime.now(timezone.utc) > self.expires_at


class CertificateAuthorityManager:
    """Manages Root CA, Intermediate CAs, automated certificate issuance, rotation, and revocation."""

    def __init__(self, root_ca_name: str = "DocuTask Root CA", trust_domain: str = "docutask.internal") -> None:
        self.root_ca_name = root_ca_name
        self.trust_domain = trust_domain
        self._lock = threading.RLock()
        self._certificates: Dict[str, X509Certificate] = {}
        self._revocation_list: Set[str] = set()  # Set of revoked serial numbers

        # Initialize Root CA
        self.root_ca = self._issue_ca_certificate(root_ca_name, is_root=True)

    def _issue_ca_certificate(self, ca_name: str, is_root: bool = False) -> X509Certificate:
        """Issue a CA certificate."""
        now = datetime.now(timezone.utc)
        expires = now + timedelta(days=3650 if is_root else 730)
        serial = uuid.uuid4().hex.upper()
        raw = f"{ca_name}:{serial}:{now.isoformat()}"
        fingerprint = hashlib.sha256(raw.encode("utf-8")).hexdigest()

        cert = X509Certificate(
            cert_id=f"ca-{serial[:8]}",
            subject_cn=ca_name,
            san_dns_names=[f"{ca_name.lower().replace(' ', '-')}.internal"],
            san_spiffe_ids=[f"spiffe://{self.trust_domain}/ca"],
            issuer_cn=ca_name if is_root else self.root_ca_name,
            serial_number=serial,
            fingerprint_sha256=fingerprint,
            status=CertificateStatus.ACTIVE,
            issued_at=now,
            expires_at=expires,
            cert_pem=f"-----BEGIN CERTIFICATE-----\nCA:{fingerprint[:32]}\n-----END CERTIFICATE-----",
            is_ca=True,
        )
        self._certificates[cert.serial_number] = cert
        return cert

    def issue_workload_certificate(
        self,
        service_name: str,
        namespace: str = "default",
        validity_days: int = 30,
        extra_dns: Optional[List[str]] = None,
    ) -> X509Certificate:
        """Issue an mTLS X.509 certificate for a service workload."""
        now = datetime.now(timezone.utc)
        expires = now + timedelta(days=validity_days)
        serial = uuid.uuid4().hex.upper()
        spiffe_id = f"spiffe://{self.trust_domain}/ns/{namespace}/sa/{service_name}"
        dns_names = [f"{service_name}.{namespace}.svc.cluster.local", f"{service_name}.internal"]
        if extra_dns:
            dns_names.extend(extra_dns)

        raw = f"{service_name}:{serial}:{spiffe_id}:{now.isoformat()}"
        fingerprint = hashlib.sha256(raw.encode("utf-8")).hexdigest()

        cert = X509Certificate(
            cert_id=f"cert-{service_name}-{serial[:6]}",
            subject_cn=f"{service_name}.{namespace}",
            san_dns_names=dns_names,
            san_spiffe_ids=[spiffe_id],
            issuer_cn=self.root_ca.subject_cn,
            serial_number=serial,
            fingerprint_sha256=fingerprint,
            status=CertificateStatus.ACTIVE,
            issued_at=now,
            expires_at=expires,
            cert_pem=f"-----BEGIN CERTIFICATE-----\nWORKLOAD:{fingerprint[:32]}\n-----END CERTIFICATE-----",
            private_key_pem=f"-----BEGIN PRIVATE KEY-----\nKEY:{uuid.uuid4().hex}\n-----END PRIVATE KEY-----",
            is_ca=False,
        )

        with self._lock:
            self._certificates[cert.serial_number] = cert

        return cert

    def rotate_certificate(self, serial_number: str) -> Optional[X509Certificate]:
        """Rotate an active certificate, reissuing with new serial and updating status."""
        with self._lock:
            old_cert = self._certificates.get(serial_number)
            if not old_cert:
                return None

            old_cert.status = CertificateStatus.ROTATING
            parts = old_cert.subject_cn.split(".")
            service_name = parts[0]
            namespace = parts[1] if len(parts) > 1 else "default"

            new_cert = self.issue_workload_certificate(
                service_name=service_name,
                namespace=namespace,
                extra_dns=old_cert.san_dns_names,
            )
            old_cert.status = CertificateStatus.REVOKED
            self._revocation_list.add(old_cert.serial_number)
            return new_cert

    def revoke_certificate(self, serial_number: str, reason: str = "key_compromise") -> bool:
        """Revoke a certificate and add to CRL."""
        with self._lock:
            cert = self._certificates.get(serial_number)
            if cert:
                cert.status = CertificateStatus.REVOKED
                self._revocation_list.add(serial_number)
                return True
            return False

    def is_certificate_valid(self, serial_number: str) -> bool:
        """Validate whether certificate is active, unexpired, and not revoked."""
        with self._lock:
            if serial_number in self._revocation_list:
                return False
            cert = self._certificates.get(serial_number)
            if not cert:
                return False
            if cert.is_expired:
                cert.status = CertificateStatus.EXPIRED
                return False
            return cert.status == CertificateStatus.ACTIVE

    def get_trust_bundle(self) -> Dict[str, Any]:
        """Return root CA trust bundle for distributing to all mesh proxies and workers."""
        with self._lock:
            return {
                "trust_domain": self.trust_domain,
                "root_ca_cn": self.root_ca.subject_cn,
                "root_ca_fingerprint": self.root_ca.fingerprint_sha256,
                "root_ca_pem": self.root_ca.cert_pem,
                "revoked_serials_count": len(self._revocation_list),
            }
