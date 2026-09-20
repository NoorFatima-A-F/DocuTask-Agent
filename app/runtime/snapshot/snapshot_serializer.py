"""
Snapshot Serializer with Compression and Cryptographic Hashing.
Provides deterministic JSON encoding, zlib compression, and SHA-256 verification.
"""

from typing import Dict, Any, Tuple
import json
import zlib
import hashlib
from app.runtime.replay.replay_state_machine import ReconstructedMissionState


class SnapshotSerializer:
    """Encodes and decodes compressed snapshot payloads with checksum validation."""

    @staticmethod
    def serialize_state(state: ReconstructedMissionState, compress: bool = True) -> Tuple[bytes, str, int]:
        """
        Serializes state to bytes.
        Returns: (payload_bytes, sha256_checksum, uncompressed_size_bytes)
        """
        json_str = state.model_dump_json()
        raw_bytes = json_str.encode("utf-8")
        uncompressed_size = len(raw_bytes)
        checksum = hashlib.sha256(raw_bytes).hexdigest()

        if compress:
            payload = zlib.compress(raw_bytes, level=6)
        else:
            payload = raw_bytes

        return payload, checksum, uncompressed_size

    @staticmethod
    def deserialize_state(payload: bytes, compressed: bool = True, expected_checksum: str = None) -> ReconstructedMissionState:
        """Decompresses and parses state from payload bytes."""
        if compressed:
            raw_bytes = zlib.decompress(payload)
        else:
            raw_bytes = payload

        if expected_checksum:
            actual_checksum = hashlib.sha256(raw_bytes).hexdigest()
            if actual_checksum != expected_checksum:
                raise ValueError(f"Snapshot checksum mismatch: expected {expected_checksum[:8]}..., got {actual_checksum[:8]}...")

        json_dict = json.loads(raw_bytes.decode("utf-8"))
        return ReconstructedMissionState.model_validate(json_dict)
