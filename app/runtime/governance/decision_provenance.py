"""Decision Provenance Engine for DocuTask ADIP.

Maintains a cryptographic Merkle DAG connecting Goal Intent -> Evidence Chain -> Belief State ->
Forward Forecast -> SMT Verification -> Strategy Decision -> Execution -> Learning.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ProvenanceNode(BaseModel):
    """Immutable audit node in the decision Merkle tree."""
    node_id: str = Field(default_factory=lambda: f"prov_{uuid.uuid4().hex[:8]}")
    phase: str  # 'GOAL', 'EVIDENCE', 'BELIEF', 'FORECAST', 'SMT_VERIFICATION', 'DECISION', 'EXECUTION'
    summary: str
    details: Dict[str, Any] = Field(default_factory=dict)
    parent_node_id: Optional[str] = None
    node_hash: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def compute_hash(self, parent_hash: str = "") -> str:
        payload = f"{self.node_id}:{self.phase}:{self.summary}:{json.dumps(self.details, sort_keys=True)}:{parent_hash}"
        self.node_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        return self.node_hash


class DecisionProvenanceTree(BaseModel):
    """Complete traceable decision audit trail for a mission."""
    mission_id: str
    nodes: List[ProvenanceNode] = Field(default_factory=list)
    merkle_root: str = ""
    is_tamper_evident: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DecisionProvenanceEngine:
    """Constructs and cryptographically seals complete decision audit chains."""

    def __init__(self) -> None:
        self._trees: Dict[str, DecisionProvenanceTree] = {}

    def get_or_create_tree(self, mission_id: str) -> DecisionProvenanceTree:
        if mission_id not in self._trees:
            self._trees[mission_id] = DecisionProvenanceTree(mission_id=mission_id)
        return self._trees[mission_id]

    def record_step(
        self,
        mission_id: str,
        phase: str,
        summary: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> ProvenanceNode:
        tree = self.get_or_create_tree(mission_id)
        parent_id = tree.nodes[-1].node_id if tree.nodes else None
        parent_hash = tree.nodes[-1].node_hash if tree.nodes else "genesis_root_00000000"

        node = ProvenanceNode(
            phase=phase,
            summary=summary,
            details=details or {},
            parent_node_id=parent_id,
        )
        node_hash = node.compute_hash(parent_hash)
        tree.nodes.append(node)
        tree.merkle_root = node_hash
        return node

    def verify_integrity(self, mission_id: str) -> bool:
        tree = self._trees.get(mission_id)
        if not tree or not tree.nodes:
            return True

        current_parent_hash = "genesis_root_00000000"
        for node in tree.nodes:
            expected = hashlib.sha256(
                f"{node.node_id}:{node.phase}:{node.summary}:{json.dumps(node.details, sort_keys=True)}:{current_parent_hash}".encode("utf-8")
            ).hexdigest()
            if node.node_hash != expected:
                return False
            current_parent_hash = node.node_hash

        return True
