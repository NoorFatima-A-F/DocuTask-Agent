"""
Hash Verifier for Phase 13.4.
Verifies continuous cryptographic hash continuity across domain events.
"""

from typing import Dict, Any, List, Tuple


class HashVerifier:
    """
    Validates sequential parent-child hash integrity.
    """

    @classmethod
    def verify_hash_chain(cls, events: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        errors = []
        for idx, ev in enumerate(events):
            if idx > 0 and "parent_hash" in ev:
                prev_ev = events[idx - 1]
                expected_parent = prev_ev.get("hash") or prev_ev.get("provenance_hash")
                if expected_parent and ev["parent_hash"] != expected_parent:
                    errors.append(f"Event #{idx} parent hash break: expected {expected_parent}, got {ev['parent_hash']}")
        return len(errors) == 0, errors
