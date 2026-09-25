"""Execution Evidence Core Data Structures.

Defines immutable evidence nodes, cryptographic proofs, and Merkle tree structures
forming the backbone of Phase 8 AEEERP runtime transparency.
"""

from __future__ import annotations

import enum
import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class EvidenceType(str, enum.Enum):
    PLANNER_DECISION = "planner_decision"
    TOOL_EXECUTION = "tool_execution"
    MEMORY_RETRIEVAL = "memory_retrieval"
    VALIDATION_CHECK = "validation_check"
    REFLECTION_MUTATION = "reflection_mutation"
    GOVERNANCE_AUDIT = "governance_audit"
    RESOURCE_AUCTION = "resource_auction"
    ENVIRONMENT_SNAPSHOT = "environment_snapshot"
    BENCHMARK_ASSERTION = "benchmark_assertion"
    ARTIFACT_MUTATION = "artifact_mutation"


class EvidenceStatus(str, enum.Enum):
    VERIFIED = "verified"
    VALID = "valid"
    TAMPERED = "tampered"
    PENDING = "pending"
    ORPHANED = "orphaned"


@dataclass(frozen=True)
class CryptoProof:
    algorithm: str
    hash_value: str
    signature: str
    public_key: str
    merkle_root: Optional[str] = None
    nonce: int = 0
    timestamp_utc: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "algorithm": self.algorithm,
            "hash_value": self.hash_value,
            "signature": self.signature,
            "public_key": self.public_key,
            "merkle_root": self.merkle_root,
            "nonce": self.nonce,
            "timestamp_utc": self.timestamp_utc,
        }


@dataclass
class MerkleNode:
    hash_value: str
    left_child: Optional[str] = None
    right_child: Optional[str] = None
    evidence_id: Optional[str] = None
    level: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "hash_value": self.hash_value,
            "left_child": self.left_child,
            "right_child": self.right_child,
            "evidence_id": self.evidence_id,
            "level": self.level,
        }


@dataclass
class EvidenceNode:
    evidence_id: str
    evidence_type: EvidenceType
    parent_hashes: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)
    source_agent: str = "docutask-agent-runtime"
    execution_context: Dict[str, Any] = field(default_factory=dict)
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    metrics: Dict[str, float] = field(default_factory=dict)
    hash_digest: str = ""
    status: EvidenceStatus = EvidenceStatus.VALID
    crypto_proof: Optional[CryptoProof] = None

    def compute_hash(self) -> str:
        """Computes deterministic SHA-256 hash digest of all node attributes."""
        payload = {
            "evidence_id": self.evidence_id,
            "evidence_type": self.evidence_type.value,
            "parent_hashes": sorted(self.parent_hashes),
            "timestamp": round(self.timestamp, 6),
            "source_agent": self.source_agent,
            "execution_context": self.execution_context,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "metrics": {k: round(v, 6) for k, v in sorted(self.metrics.items())},
        }
        serialized = json.dumps(payload, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def seal(self, private_seed: str = "docutask-aeeerp-root-key-2026") -> EvidenceNode:
        """Computes hash digest and attaches deterministic cryptographic proof."""
        digest = self.compute_hash()
        self.hash_digest = digest
        sig_data = f"{digest}:{private_seed}:{self.timestamp}"
        sig_hash = hashlib.sha256(sig_data.encode("utf-8")).hexdigest()
        pub_key = hashlib.sha256(private_seed.encode("utf-8")).hexdigest()[:32]
        
        self.crypto_proof = CryptoProof(
            algorithm="SHA-256+Ed25519-Sim",
            hash_value=digest,
            signature=f"sig_{sig_hash[:48]}",
            public_key=f"pub_{pub_key}",
            timestamp_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.timestamp)),
            nonce=int(digest[:8], 16) % 1000000,
        )
        self.status = EvidenceStatus.VERIFIED
        return self

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "evidence_type": self.evidence_type.value,
            "parent_hashes": self.parent_hashes,
            "timestamp": self.timestamp,
            "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.timestamp)),
            "source_agent": self.source_agent,
            "execution_context": self.execution_context,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "metrics": self.metrics,
            "hash_digest": self.hash_digest,
            "status": self.status.value,
            "crypto_proof": self.crypto_proof.to_dict() if self.crypto_proof else None,
        }
