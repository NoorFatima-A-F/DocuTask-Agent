"""Digital Signatures and HMAC Proof of Authenticity for Audit Records."""

import hmac
import hashlib
from typing import Optional


class AuditSigner:
    """Signs and verifies HMAC integrity signatures for audit records."""

    DEFAULT_SECRET = "docutask_enterprise_audit_master_secret_key_2026"

    def __init__(self, secret_key: Optional[str] = None):
        self.secret_key = (secret_key or self.DEFAULT_SECRET).encode("utf-8")

    def sign_hash(self, integrity_hash: str) -> str:
        """Computes HMAC-SHA256 signature for the given integrity hash."""
        return hmac.new(self.secret_key, integrity_hash.encode("utf-8"), hashlib.sha256).hexdigest()

    def verify_signature(self, integrity_hash: str, signature: str) -> bool:
        """Verifies that the signature matches the calculated HMAC of the hash."""
        expected = self.sign_hash(integrity_hash)
        return hmac.compare_digest(expected, signature)
