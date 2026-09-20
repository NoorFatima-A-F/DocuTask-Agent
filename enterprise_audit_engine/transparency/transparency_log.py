"""Append-Only Cryptographic Certification Transparency Log."""

import hashlib
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class TransparencyLogEntry(BaseModel):
    """Immutable entry in the Certification Transparency Log."""
    entry_id: int
    certificate_id: str
    release_version: str
    merkle_root: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    issuer: str
    status: str
    prev_entry_hash: str
    entry_hash: str = ""

    def calculate_hash(self) -> str:
        data = {
            "entry_id": self.entry_id,
            "certificate_id": self.certificate_id,
            "release_version": self.release_version,
            "merkle_root": self.merkle_root,
            "timestamp": self.timestamp,
            "issuer": self.issuer,
            "status": self.status,
            "prev_entry_hash": self.prev_entry_hash,
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()


class CertificationTransparencyLog:
    """Manages an append-only, tamper-evident transparency ledger inspired by Rekor and Certificate Transparency."""

    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "transparency_log.jsonl"

    def append_entry(
        self,
        certificate_id: str,
        release_version: str,
        merkle_root: str,
        issuer: str,
        status: str,
    ) -> TransparencyLogEntry:
        """Appends a new verified certificate record to the cryptographic hash chain."""
        entries = self.load_entries()
        prev_hash = entries[-1].entry_hash if entries else hashlib.sha256(b"GENESIS_BLOCK").hexdigest()
        entry_id = len(entries) + 1

        entry = TransparencyLogEntry(
            entry_id=entry_id,
            certificate_id=certificate_id,
            release_version=release_version,
            merkle_root=merkle_root,
            issuer=issuer,
            status=status,
            prev_entry_hash=prev_hash,
        )
        entry = entry.model_copy(update={"entry_hash": entry.calculate_hash()})

        with open(self.log_file, "a", encoding="utf-8") as fp:
            fp.write(json.dumps(entry.model_dump(), sort_keys=True) + "\n")

        return entry

    def load_entries(self) -> List[TransparencyLogEntry]:
        """Loads all transparency entries from the JSONL log file."""
        if not self.log_file.exists():
            return []
        entries = []
        with open(self.log_file, "r", encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if line:
                    entries.append(TransparencyLogEntry.model_validate(json.loads(line)))
        return entries

    def verify_log_integrity(self) -> Dict[str, Any]:
        """Verifies the complete parent-hash cryptographic chain of the transparency log."""
        entries = self.load_entries()
        if not entries:
            return {"is_valid": True, "entries_count": 0, "status": "EMPTY_LOG"}

        tampered_entries = []
        expected_prev = hashlib.sha256(b"GENESIS_BLOCK").hexdigest()

        for entry in entries:
            # 1. Check prev hash
            if entry.prev_entry_hash != expected_prev:
                tampered_entries.append({
                    "entry_id": entry.entry_id,
                    "error": f"Invalid prev_entry_hash (expected {expected_prev}, got {entry.prev_entry_hash})",
                })
            # 2. Check entry hash computation
            calc_hash = entry.calculate_hash()
            if entry.entry_hash != calc_hash:
                tampered_entries.append({
                    "entry_id": entry.entry_id,
                    "error": f"Tampered entry_hash (expected {calc_hash}, got {entry.entry_hash})",
                })
            expected_prev = entry.entry_hash

        is_valid = len(tampered_entries) == 0
        return {
            "is_valid": is_valid,
            "entries_count": len(entries),
            "tampered_count": len(tampered_entries),
            "tampered_entries": tampered_entries,
            "latest_head_hash": entries[-1].entry_hash if entries else "",
            "status": "CHAIN_VALID_AND_TAMPER_FREE" if is_valid else "CHAIN_INTEGRITY_COMPROMISED",
        }
