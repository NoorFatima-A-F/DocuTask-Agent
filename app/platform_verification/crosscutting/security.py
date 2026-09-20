"""
Security, Sanitization, and HMAC-SHA256 Cryptographic Tools.
"""
import hmac
import hashlib
import json
from typing import Any

SECRET_KEY = b"enterprise-verification-master-secret-key-2026"

def compute_payload_hash(payload: Any) -> str:
    if isinstance(payload, (dict, list)):
        payload_str = json.dumps(payload, sort_keys=True)
    else:
        payload_str = str(payload)
    return hashlib.sha256(payload_str.encode("utf-8")).hexdigest()

def sign_canonical_hash(canonical_str: str) -> str:
    return hmac.new(SECRET_KEY, canonical_str.encode("utf-8"), hashlib.sha256).hexdigest()

def verify_canonical_signature(canonical_str: str, signature: str) -> bool:
    expected = sign_canonical_hash(canonical_str)
    return hmac.compare_digest(expected, signature)
