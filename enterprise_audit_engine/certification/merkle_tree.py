"""Cryptographic Merkle Evidence Tree & Root Sealer."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any
from enterprise_audit_engine.domain.evidence.models import EvidenceRecord


class MerkleEvidenceTree:
    """Builds an enterprise cryptographic Merkle tree over collected evidence records."""

    @classmethod
    def compute_leaf_hash(cls, r: EvidenceRecord) -> str:
        """Computes a deterministic semantic hash for an evidence record across runs."""
        semantic_data = {
            "category": r.category,
            "collector": r.collector,
            "source_type": r.source_type.value,
            "summary": r.summary,
            "classification": r.classification.value,
            "raw_payload": r.raw_payload,
        }
        serialized = json.dumps(semantic_data, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def __init__(self, records: List[EvidenceRecord]):
        self.records = records
        # Normalize and sort deterministically by (category, collector, summary)
        sorted_records = sorted(records, key=lambda r: (r.category, r.collector, r.summary))
        self.leaf_map: Dict[str, str] = {r.id: self.compute_leaf_hash(r) for r in sorted_records}
        self.leaves: List[str] = [self.compute_leaf_hash(r) for r in sorted_records]
        self.levels: List[List[str]] = []
        self._build_tree()

    def _hash_pair(self, left: str, right: str) -> str:
        combined = f"{left}:{right}".encode("utf-8")
        return hashlib.sha256(combined).hexdigest()

    def _build_tree(self):
        if not self.leaves:
            self.root = hashlib.sha256(b"empty_merkle_tree").hexdigest()
            self.levels = [[self.root]]
            return

        current_level = list(self.leaves)
        self.levels.append(current_level)

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                next_level.append(self._hash_pair(left, right))
            current_level = next_level
            self.levels.append(current_level)

        self.root = self.levels[-1][0] if self.levels else ""

    @property
    def merkle_root(self) -> str:
        return self.root

    def get_proof(self, evidence_id: str) -> List[Dict[str, str]]:
        """Generates an audit proof path for a given evidence record."""
        if evidence_id not in self.leaf_map:
            return []

        target_hash = self.leaf_map[evidence_id]
        if target_hash not in self.leaves:
            return []

        idx = self.leaves.index(target_hash)
        proof = []

        for level in self.levels[:-1]:
            is_right = idx % 2 == 1
            sibling_idx = idx - 1 if is_right else (idx + 1 if idx + 1 < len(level) else idx)
            sibling_hash = level[sibling_idx]
            proof.append({
                "position": "left" if is_right else "right",
                "hash": sibling_hash,
            })
            idx = idx // 2

        return proof

    @classmethod
    def verify_proof(cls, leaf_hash: str, proof: List[Dict[str, str]], root_hash: str) -> bool:
        """Verifies that a leaf hash is part of the Merkle Tree with the given root."""
        current = leaf_hash
        for step in proof:
            pos = step.get("position")
            sibling = step.get("hash", "")
            if pos == "left":
                combined = f"{sibling}:{current}".encode("utf-8")
            else:
                combined = f"{current}:{sibling}".encode("utf-8")
            current = hashlib.sha256(combined).hexdigest()
        return current == root_hash

    def export_merkle_manifest(self) -> Dict[str, Any]:
        """Generates the sealed audit_merkle_root.json payload."""
        return {
            "merkle_root": self.root,
            "total_leaves": len(self.leaves),
            "tree_depth": len(self.levels),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "leaf_evidence_map": self.leaf_map,
        }

    def save_merkle_manifest(self, target_path: Path) -> Path:
        data = self.export_merkle_manifest()
        with open(target_path, "w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2, sort_keys=True)
        return target_path
