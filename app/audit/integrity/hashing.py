"""Cryptographic Hash Chain Engine for Tamper-Evident Audit Trails."""

import hashlib
import json
from typing import Dict, Any, Optional
from ..core.events import AuditEvent


class HashChainCalculator:
    """Calculates deterministic SHA-256 hashes and chained integrity digests for audit events."""

    GENESIS_HASH = "0000000000000000000000000000000000000000000000000000000000000000"

    @staticmethod
    def canonical_serialize(event_dict: Dict[str, Any]) -> str:
        """Serializes event fields in deterministic sorted key order excluding volatile hash/signature fields."""
        excluded_fields = {"integrity_hash", "signature"}
        filtered = {k: v for k, v in event_dict.items() if k not in excluded_fields}
        
        # Convert datetimes and complex objects to string representation
        def serialize_helper(obj):
            if hasattr(obj, "isoformat"):
                return obj.isoformat()
            if hasattr(obj, "value"):  # Enum
                return obj.value
            if isinstance(obj, dict):
                return {k: serialize_helper(v) for k, v in sorted(obj.items())}
            if isinstance(obj, list):
                return [serialize_helper(i) for i in obj]
            return obj

        clean_dict = serialize_helper(filtered)
        return json.dumps(clean_dict, sort_keys=True, separators=(",", ":"))

    @classmethod
    def compute_event_hash(cls, event: AuditEvent, previous_hash: Optional[str] = None) -> str:
        """Computes SHA-256(canonical_payload + previous_hash)."""
        prev = previous_hash or cls.GENESIS_HASH
        event_dict = event.model_dump()
        event_dict["previous_hash"] = prev
        canonical_str = cls.canonical_serialize(event_dict)
        
        combined = f"{canonical_str}|{prev}".encode("utf-8")
        return hashlib.sha256(combined).hexdigest()
