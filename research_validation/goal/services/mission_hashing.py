"""
Mission Hashing & Provenance Sealing Service
============================================
Computes deterministic canonical SHA-256 digests and digital signature placeholders.
"""

from typing import Any, Dict
from research_validation.provenance.hashing import hash_canonical_json


class MissionHashingService:
    """Computes deterministic cryptographic hashes for Goals and Missions."""

    @classmethod
    def hash_goal(cls, canonical_dict: Dict[str, Any]) -> str:
        """Computes SHA-256 over canonical goal representation."""
        return hash_canonical_json(canonical_dict)

    @classmethod
    def hash_mission(cls, canonical_dict: Dict[str, Any]) -> str:
        """Computes SHA-256 over canonical mission representation."""
        return hash_canonical_json(canonical_dict)

    @classmethod
    def create_digital_signature_placeholder(cls, payload_digest: str, author_key_id: str = "SYSTEM_ROOT") -> str:
        """Generates a cryptographic signature token placeholder."""
        sig_data = {"digest": payload_digest, "key_id": author_key_id, "algorithm": "Ed25519_SEAL"}
        return f"SIG_{hash_canonical_json(sig_data)[:32]}"
