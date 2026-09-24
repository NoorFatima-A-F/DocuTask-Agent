"""Mutual TLS (mTLS) Engine, Handshake Verification, and Cipher Suites."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional
import logging

from .certificates import CertificateAuthorityManager, X509Certificate

logger = logging.getLogger("app.infrastructure.networking.security.mtls")


@dataclass
class MTLSValidationResult:
    """Outcome of mutual TLS verification."""
    is_valid: bool
    caller_spiffe_id: str = ""
    destination_spiffe_id: str = ""
    caller_cert_serial: str = ""
    tls_version: str = "TLSv1.3"
    cipher_suite: str = "TLS_AES_256_GCM_SHA384"
    error_message: Optional[str] = None
    validated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class MTLSEngine:
    """Verifies peer certificates and enforces mTLS security requirements."""

    ALLOWED_TLS_VERSIONS = {"TLSv1.3", "TLSv1.2"}
    ALLOWED_CIPHERS = {
        "TLS_AES_256_GCM_SHA384",
        "TLS_CHACHA20_POLY1305_SHA256",
        "TLS_AES_128_GCM_SHA256",
        "ECDHE-ECDSA-AES256-GCM-SHA384",
    }

    def __init__(self, ca_manager: CertificateAuthorityManager) -> None:
        self.ca_manager = ca_manager

    def validate_connection(
        self,
        client_cert: Optional[X509Certificate],
        server_cert: Optional[X509Certificate],
        expected_destination_spiffe: Optional[str] = None,
        tls_version: str = "TLSv1.3",
        cipher_suite: str = "TLS_AES_256_GCM_SHA384",
    ) -> MTLSValidationResult:
        """Validate mutual TLS handshake parameters and client/server certificates."""
        if tls_version not in self.ALLOWED_TLS_VERSIONS:
            return MTLSValidationResult(
                is_valid=False,
                error_message=f"Disallowed TLS version: {tls_version}",
            )

        if cipher_suite not in self.ALLOWED_CIPHERS:
            return MTLSValidationResult(
                is_valid=False,
                error_message=f"Disallowed cipher suite: {cipher_suite}",
            )

        # 1. Validate Client Certificate
        if not client_cert:
            return MTLSValidationResult(
                is_valid=False,
                error_message="Client certificate missing (mTLS required)",
            )

        if not self.ca_manager.is_certificate_valid(client_cert.serial_number):
            return MTLSValidationResult(
                is_valid=False,
                caller_cert_serial=client_cert.serial_number,
                error_message="Client certificate is invalid, revoked, or expired",
            )

        # 2. Validate Server Certificate
        if not server_cert:
            return MTLSValidationResult(
                is_valid=False,
                error_message="Server certificate missing",
            )

        if not self.ca_manager.is_certificate_valid(server_cert.serial_number):
            return MTLSValidationResult(
                is_valid=False,
                error_message="Server certificate is invalid, revoked, or expired",
            )

        caller_spiffe = client_cert.san_spiffe_ids[0] if client_cert.san_spiffe_ids else ""
        dest_spiffe = server_cert.san_spiffe_ids[0] if server_cert.san_spiffe_ids else ""

        # 3. Optional Destination SPIFFE Match Check
        if expected_destination_spiffe and expected_destination_spiffe != dest_spiffe:
            return MTLSValidationResult(
                is_valid=False,
                caller_spiffe_id=caller_spiffe,
                destination_spiffe_id=dest_spiffe,
                error_message=f"Destination SPIFFE mismatch: expected {expected_destination_spiffe}, got {dest_spiffe}",
            )

        return MTLSValidationResult(
            is_valid=True,
            caller_spiffe_id=caller_spiffe,
            destination_spiffe_id=dest_spiffe,
            caller_cert_serial=client_cert.serial_number,
            tls_version=tls_version,
            cipher_suite=cipher_suite,
        )
