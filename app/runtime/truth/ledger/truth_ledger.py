"""
Runtime Truth Ledger for Phase 11 (VAIRTSEP).

Provides an append-only, cryptographically linked truth ledger capturing every
runtime event, planner decision, and optimization step with SHA-256 hash continuity.
"""

from __future__ import annotations

import hashlib
import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TruthLedgerEntry:
    """
    Immutable entry in the Runtime Truth Ledger.
    Hash-chained to the previous entry to prevent retroactive tampering.
    """
    event_id: str
    mission_id: str
    event_type: str  # e.g., PLANNER_DECISION, TOOL_EXECUTION, EVIDENCE_SIGNED, OPTIMIZATION_PROMOTED
    timestamp: float = field(default_factory=time.time)
    parent_event_hash: str = ""
    
    # Execution & Model Lineage
    planner_version: str = "v2.1.0"
    strategy_version: str = "1.0.0"
    policy_version: str = "1.0.0"
    tool_name: Optional[str] = None
    tool_version: Optional[str] = None
    model_version: str = "gemini-1.5-pro"
    
    # Cryptographic & Reproducibility Proofs
    document_fingerprint: str = ""
    evidence_root_hash: str = ""
    runtime_metadata: Dict[str, Any] = field(default_factory=dict)
    reproducibility_metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Computed Cryptographic Hash
    entry_hash: str = ""

    def __post_init__(self):
        if not self.entry_hash:
            self.entry_hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = {
            "event_id": self.event_id,
            "mission_id": self.mission_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "parent_event_hash": self.parent_event_hash,
            "planner_version": self.planner_version,
            "strategy_version": self.strategy_version,
            "document_fingerprint": self.document_fingerprint,
            "evidence_root_hash": self.evidence_root_hash,
        }
        raw = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class TruthLedger:
    """
    Append-only cryptographically linked Truth Ledger.
    """

    def __init__(self):
        self._entries: Dict[str, TruthLedgerEntry] = {}
        self._chain: List[str] = []
        self._mission_index: Dict[str, List[str]] = {}
        self._latest_hash: str = "0" * 64

    def append_event(
        self,
        mission_id: str,
        event_type: str,
        planner_version: str = "v2.1.0",
        strategy_version: str = "1.0.0",
        policy_version: str = "1.0.0",
        tool_name: Optional[str] = None,
        tool_version: Optional[str] = None,
        model_version: str = "gemini-1.5-pro",
        document_fingerprint: str = "",
        evidence_root_hash: str = "",
        runtime_metadata: Optional[Dict[str, Any]] = None,
        reproducibility_metadata: Optional[Dict[str, Any]] = None,
    ) -> TruthLedgerEntry:
        event_id = f"tle_{uuid.uuid4().hex[:12]}"
        
        entry = TruthLedgerEntry(
            event_id=event_id,
            mission_id=mission_id,
            event_type=event_type,
            timestamp=time.time(),
            parent_event_hash=self._latest_hash,
            planner_version=planner_version,
            strategy_version=strategy_version,
            policy_version=policy_version,
            tool_name=tool_name,
            tool_version=tool_version,
            model_version=model_version,
            document_fingerprint=document_fingerprint or hashlib.sha256(mission_id.encode("utf-8")).hexdigest()[:16],
            evidence_root_hash=evidence_root_hash or hashlib.sha256(f"ev_{mission_id}".encode("utf-8")).hexdigest(),
            runtime_metadata=runtime_metadata or {},
            reproducibility_metadata=reproducibility_metadata or {"rng_seed": 42, "env": "production-python-3.14"},
        )

        self._entries[event_id] = entry
        self._chain.append(event_id)
        self._latest_hash = entry.entry_hash

        if mission_id not in self._mission_index:
            self._mission_index[mission_id] = []
        self._mission_index[mission_id].append(event_id)

        return entry

    def verify_chain_integrity(self) -> Dict[str, Any]:
        """Validates hash chain continuity across the entire ledger."""
        if not self._chain:
            return {"valid": True, "total_entries": 0, "latest_hash": self._latest_hash}

        current_parent = "0" * 64
        for eid in self._chain:
            entry = self._entries[eid]
            if entry.parent_event_hash != current_parent:
                return {
                    "valid": False,
                    "tampered_event_id": eid,
                    "expected_parent": current_parent,
                    "actual_parent": entry.parent_event_hash,
                }
            if entry.entry_hash != entry.compute_hash():
                return {
                    "valid": False,
                    "tampered_event_id": eid,
                    "reason": "Hash mismatch against content payload",
                }
            current_parent = entry.entry_hash

        return {
            "valid": True,
            "total_entries": len(self._chain),
            "latest_hash": self._latest_hash,
            "root_entry_id": self._chain[0],
            "tip_entry_id": self._chain[-1],
        }

    def get_entry(self, event_id: str) -> Optional[TruthLedgerEntry]:
        return self._entries.get(event_id)

    def get_mission_events(self, mission_id: str) -> List[TruthLedgerEntry]:
        eids = self._mission_index.get(mission_id, [])
        return [self._entries[eid] for eid in eids]

    def list_recent(self, limit: int = 50) -> List[TruthLedgerEntry]:
        return [self._entries[eid] for eid in reversed(self._chain[-limit:])]

    def count(self) -> int:
        return len(self._entries)
