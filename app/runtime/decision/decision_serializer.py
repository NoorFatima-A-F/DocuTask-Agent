"""
Decision Serializer with Cryptographic Hash Generation.
Ensures every planner decision object is canonically serialized and tamper-evident.
"""

from typing import Dict, Any
import json
import hashlib


class DecisionSerializer:
    @staticmethod
    def canonical_json(data: Dict[str, Any]) -> str:
        """Produces canonical sorted JSON string."""
        return json.dumps(data, sort_keys=True, default=str)

    @staticmethod
    def compute_decision_hash(decision_dict: Dict[str, Any]) -> str:
        """Computes deterministic SHA-256 hash of decision payload excluding the hash itself."""
        clean = {k: v for k, v in decision_dict.items() if k != "decision_hash"}
        canonical = DecisionSerializer.canonical_json(clean)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
