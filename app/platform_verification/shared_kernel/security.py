"""
Cryptographic Utilities and Canonical Hashing.
"""
import hashlib
import hmac
import json
from typing import Any

class CanonicalHasher:
    @staticmethod
    def hash_payload(data: Any) -> str:
        if isinstance(data, (bytes, bytearray)):
            raw = data
        elif isinstance(data, str):
            raw = data.encode("utf-8")
        else:
            raw = json.dumps(data, sort_keys=True, default=str).encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    @staticmethod
    def calculate_merkle_root(leaf_hashes: list[str]) -> str:
        if not leaf_hashes:
            return hashlib.sha256(b"EMPTY_MERKLE_TREE").hexdigest()
        if len(leaf_hashes) == 1:
            return leaf_hashes[0]

        current = leaf_hashes
        while len(current) > 1:
            next_level = []
            for i in range(0, len(current), 2):
                if i + 1 < len(current):
                    combined = (current[i] + current[i+1]).encode("utf-8")
                else:
                    combined = (current[i] + current[i]).encode("utf-8")
                next_level.append(hashlib.sha256(combined).hexdigest())
            current = next_level
        return current[0]


class HMACSigner:
    @staticmethod
    def sign(secret_key: str, message: str) -> str:
        return hmac.new(
            secret_key.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    @staticmethod
    def verify(secret_key: str, message: str, expected_signature: str) -> bool:
        actual = HMACSigner.sign(secret_key, message)
        return hmac.compare_digest(actual, expected_signature)


CryptoUtils = CanonicalHasher
