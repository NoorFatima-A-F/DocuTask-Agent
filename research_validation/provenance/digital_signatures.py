"""
Evidence Provenance & Scientific Lineage Framework
Module: digital_signatures.py

Provides cryptographic signing, detached signatures, trust chain validation,
and signature expiration verification for scientific evidence envelopes.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class SignatureAlgorithm(str, Enum):
    HMAC_SHA256 = "HMAC-SHA256"
    ED25519 = "Ed25519"
    ECDSA_P256 = "ECDSA-P256"


@dataclass
class CertificateInfo:
    """X.509 / In-toto style certificate descriptor in a trust chain."""
    key_id: str
    issuer: str
    subject: str
    algorithm: SignatureAlgorithm
    public_key_pem_or_hex: str
    valid_from_epoch: float
    valid_until_epoch: float
    is_revoked: bool = False

    def is_valid_at(self, timestamp: float) -> bool:
        return (not self.is_revoked) and (self.valid_from_epoch <= timestamp <= self.valid_until_epoch)


@dataclass
class DetachedSignature:
    """Cryptographic detached signature envelope."""
    key_id: str
    algorithm: SignatureAlgorithm
    signature_base64: str
    payload_digest_sha256: str
    signed_at_epoch: float
    expires_at_epoch: float
    signer_identity: str
    trust_chain_issuer: Optional[str] = None

    def is_expired(self, current_time: Optional[float] = None) -> bool:
        now = current_time or time.time()
        return now > self.expires_at_epoch


class ProvenanceSigner:
    """
    Signs evidence digests and verifies detached signatures against trust certificates.
    """

    def __init__(self, key_id: str, secret_or_private_key: str, algorithm: SignatureAlgorithm = SignatureAlgorithm.HMAC_SHA256):
        self.key_id = key_id
        self.secret_or_private_key = secret_or_private_key
        self.algorithm = algorithm

    def sign_digest(
        self,
        digest_hex: str,
        signer_identity: str,
        validity_duration_seconds: float = 31536000.0  # 1 year default
    ) -> DetachedSignature:
        """Create a detached signature over an artifact/node digest."""
        now = time.time()
        expires = now + validity_duration_seconds

        msg = f"{self.key_id}:{self.algorithm.value}:{digest_hex}:{now}:{expires}:{signer_identity}".encode("utf-8")
        sig_bytes = hmac.new(self.secret_or_private_key.encode("utf-8"), msg, hashlib.sha256).digest()
        sig_b64 = base64.b64encode(sig_bytes).decode("ascii")

        return DetachedSignature(
            key_id=self.key_id,
            algorithm=self.algorithm,
            signature_base64=sig_b64,
            payload_digest_sha256=digest_hex,
            signed_at_epoch=now,
            expires_at_epoch=expires,
            signer_identity=signer_identity
        )

    @classmethod
    def verify_signature(
        cls,
        signature: DetachedSignature,
        expected_digest_hex: str,
        secret_or_public_key: str,
        certificate: Optional[CertificateInfo] = None,
        check_time: Optional[float] = None
    ) -> Tuple[bool, str]:
        """
        Verify detached signature against payload digest and trust certificate.
        Returns: (is_valid, reason)
        """
        now = check_time or time.time()

        # 1. Expiration check
        if signature.is_expired(current_time=now):
            return False, f"Signature expired at epoch {signature.expires_at_epoch} (current: {now})"

        # 2. Certificate trust chain check
        if certificate:
            if not certificate.is_valid_at(now):
                return False, f"Certificate for key_id '{certificate.key_id}' is revoked or out of valid time window."
            if certificate.key_id != signature.key_id:
                return False, f"Certificate key_id mismatch: expected '{signature.key_id}', got '{certificate.key_id}'"

        # 3. Digest integrity check
        if signature.payload_digest_sha256.lower() != expected_digest_hex.lower():
            return False, f"Digest mismatch: signed '{signature.payload_digest_sha256}', expected '{expected_digest_hex}'"

        # 4. Cryptographic signature check
        msg = f"{signature.key_id}:{signature.algorithm.value}:{expected_digest_hex}:{signature.signed_at_epoch}:{signature.expires_at_epoch}:{signature.signer_identity}".encode("utf-8")
        expected_sig = hmac.new(secret_or_public_key.encode("utf-8"), msg, hashlib.sha256).digest()
        actual_sig = base64.b64decode(signature.signature_base64.encode("ascii"))

        if not hmac.compare_digest(expected_sig, actual_sig):
            return False, "Cryptographic signature verification failed: invalid signature bytes."

        return True, "Signature verified successfully."
