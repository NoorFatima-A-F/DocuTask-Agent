"""
Event Serializer & Cryptographic Hash-Chain Validator.

Provides deterministic canonical JSON serialization and SHA-256 checksum / hash-chain calculation
to guarantee the immutability and tamper-evidence of execution event streams.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Tuple
from app.runtime.observability.schemas import BaseRuntimeEvent


class EventSerializer:
    """Canonical JSON serializer with cryptographic hash-chain verification."""

    @staticmethod
    def to_canonical_json(data: Dict[str, Any]) -> str:
        """Serializes dictionary to deterministic canonical JSON (sorted keys, no spaces)."""
        return json.dumps(data, sort_keys=True, separators=(",", ":"), default=str)

    @classmethod
    def compute_event_hash(
        cls, event: BaseRuntimeEvent, prev_event_hash: str = "GENESIS"
    ) -> str:
        """
        Computes SHA-256 hash for an event chained to the previous event hash.
        Hash = SHA256(prev_hash + ":" + canonical_json(event_payload_and_metadata))
        """
        event_dict = event.model_dump(
            exclude={"event_hash", "prev_event_hash"}
        )
        canonical = cls.to_canonical_json(event_dict)
        payload = f"{prev_event_hash}:{canonical}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    @classmethod
    def sign_and_chain_event(
        cls, event: BaseRuntimeEvent, prev_event_hash: str = "GENESIS"
    ) -> BaseRuntimeEvent:
        """Attaches prev_event_hash and calculates event_hash."""
        event.prev_event_hash = prev_event_hash
        event.event_hash = cls.compute_event_hash(event, prev_event_hash)
        return event

    @classmethod
    def verify_event_integrity(cls, event: BaseRuntimeEvent) -> bool:
        """Verifies if the event hash matches its canonical content and previous hash."""
        if not event.event_hash:
            return False
        prev_hash = event.prev_event_hash or "GENESIS"
        expected = cls.compute_event_hash(event, prev_hash)
        return event.event_hash == expected

    @classmethod
    def verify_stream_integrity(cls, events: list[BaseRuntimeEvent]) -> Tuple[bool, int, str]:
        """
        Verifies the cryptographic integrity of an entire event sequence.
        Returns: (is_valid, failing_index, failure_reason)
        """
        if not events:
            return True, -1, "Empty stream"

        prev_hash = "GENESIS"
        for idx, event in enumerate(events):
            if event.prev_event_hash != prev_hash:
                return False, idx, f"Broken chain link at index {idx}: expected prev {prev_hash}, got {event.prev_event_hash}"
            expected_hash = cls.compute_event_hash(event, prev_hash)
            if event.event_hash != expected_hash:
                return False, idx, f"Corrupted event content at index {idx}: hash mismatch"
            prev_hash = event.event_hash

        return True, -1, "Stream integrity verified"
