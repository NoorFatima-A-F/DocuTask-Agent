"""
Evidence Provenance & Scientific Lineage Framework
Module: hashing.py

Provides multi-algorithm cryptographic hashing supporting:
- SHA-256 (NIST FIPS 180-4)
- SHA3-512 (NIST FIPS 202)
- BLAKE3 (Fast tree-hashing / fallback via hashlib blake2b or sha256 tree)
"""

from __future__ import annotations

import hashlib
import json
from enum import Enum
from typing import Any, Dict, List, Union


class HashAlgorithm(str, Enum):
    SHA256 = "SHA-256"
    SHA3_512 = "SHA3-512"
    BLAKE3 = "BLAKE3"


class ProvenanceHasher:
    """
    Standardized cryptographic hashing engine for provenance nodes and artifacts.
    """

    @classmethod
    def hash_bytes(cls, data: bytes, algorithm: HashAlgorithm = HashAlgorithm.SHA256) -> str:
        """Hash raw bytes using specified algorithm."""
        if algorithm == HashAlgorithm.SHA256:
            return hashlib.sha256(data).hexdigest()
        elif algorithm == HashAlgorithm.SHA3_512:
            return hashlib.sha3_512(data).hexdigest()
        elif algorithm == HashAlgorithm.BLAKE3:
            # Python standard library hashlib blake2b with 256-bit digest as robust tree-hash implementation
            return hashlib.blake2b(data, digest_size=32).hexdigest()
        else:
            return hashlib.sha256(data).hexdigest()

    @classmethod
    def hash_string(cls, text: str, algorithm: HashAlgorithm = HashAlgorithm.SHA256) -> str:
        """Hash UTF-8 string."""
        return cls.hash_bytes(text.encode("utf-8"), algorithm=algorithm)

    @classmethod
    def hash_canonical_json(cls, payload: Any, algorithm: HashAlgorithm = HashAlgorithm.SHA256) -> str:
        """
        Hash JSON object deterministically using sorted keys and compact separators.
        Guarantees bit-for-bit identical hashes across all platforms.
        """
        canonical_str = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        return cls.hash_string(canonical_str, algorithm=algorithm)

    @classmethod
    def combine_hashes(cls, hashes: List[str], algorithm: HashAlgorithm = HashAlgorithm.SHA256) -> str:
        """
        Combine multiple hashes into a parent Merkle node hash.
        """
        if not hashes:
            return cls.hash_string("", algorithm=algorithm)
        concatenated = ":".join(hashes)
        return cls.hash_string(concatenated, algorithm=algorithm)


def hash_canonical_json(payload: Any, algorithm: HashAlgorithm = HashAlgorithm.SHA256) -> str:
    """Deterministic JSON canonical hashing."""
    return ProvenanceHasher.hash_canonical_json(payload, algorithm=algorithm)


def compute_sha256(data: Union[bytes, str]) -> str:
    """Compute SHA-256 hash of string or bytes."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return ProvenanceHasher.hash_bytes(data, HashAlgorithm.SHA256)

