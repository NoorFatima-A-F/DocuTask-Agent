"""
Cryptographic Signing and Verification Subsystem for Audit Records.
Produces deterministic HMAC-SHA256 signatures over canonical audit record payloads.
"""

from typing import Dict, Any
import json
import hmac
import hashlib

SECRET_SALT = b"docutask-enterprise-audit-secret-v2"


class AuditSignatureEngine:
    @staticmethod
    def canonical_json(data: Dict[str, Any]) -> str:
        clean = {k: v for k, v in data.items() if k not in {"sha256", "signature"}}
        return json.dumps(clean, sort_keys=True, default=str)

    @staticmethod
    def compute_sha256(data: Dict[str, Any], previous_hash: str) -> str:
        canonical = AuditSignatureEngine.canonical_json(data)
        combined = f"{previous_hash}:{canonical}".encode("utf-8")
        return hashlib.sha256(combined).hexdigest()

    @staticmethod
    def sign_record(data: Dict[str, Any], record_hash: str) -> str:
        h = hmac.new(SECRET_SALT, record_hash.encode("utf-8"), hashlib.sha256)
        return h.hexdigest()

    @staticmethod
    def verify_signature(record_hash: str, signature: str) -> bool:
        expected = AuditSignatureEngine.sign_record({}, record_hash)
        return hmac.compare_digest(expected, signature)
