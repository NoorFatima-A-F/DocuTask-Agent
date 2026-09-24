"""Evidence Graph and Merkle Tree Engine.

Maintains an immutable Directed Acyclic Graph (DAG) of execution evidence nodes,
computes binary Merkle tree roots, and verifies cryptographic parent-child lineages.
"""

from __future__ import annotations

import collections
import hashlib
from typing import Any, Dict, List, Optional, Tuple

from app.runtime.evidence.execution_evidence import (
    EvidenceNode,
    MerkleNode,
)


class EvidenceGraph:
    def __init__(self, graph_id: str = "runtime-evidence-dag"):
        self.graph_id = graph_id
        self._nodes_by_id: Dict[str, EvidenceNode] = {}
        self._nodes_by_hash: Dict[str, EvidenceNode] = {}
        self._children_by_hash: Dict[str, List[str]] = collections.defaultdict(list)
        self._merkle_root: Optional[str] = None

    def add_node(self, node: EvidenceNode) -> str:
        """Adds a sealed evidence node to the graph."""
        if not node.hash_digest:
            node.seal()
        
        self._nodes_by_id[node.evidence_id] = node
        self._nodes_by_hash[node.hash_digest] = node
        
        for parent_hash in node.parent_hashes:
            self._children_by_hash[parent_hash].append(node.hash_digest)
            
        self._merkle_root = None  # invalidate cache
        return node.hash_digest

    def get_node(self, evidence_id: str) -> Optional[EvidenceNode]:
        return self._nodes_by_id.get(evidence_id)

    def get_by_hash(self, hash_digest: str) -> Optional[EvidenceNode]:
        return self._nodes_by_hash.get(hash_digest)

    def get_children(self, hash_digest: str) -> List[EvidenceNode]:
        child_hashes = self._children_by_hash.get(hash_digest, [])
        return [self._nodes_by_hash[h] for h in child_hashes if h in self._nodes_by_hash]

    def count(self) -> int:
        return len(self._nodes_by_id)

    def list_nodes(self) -> List[EvidenceNode]:
        return list(self._nodes_by_id.values())

    def get_roots(self) -> List[EvidenceNode]:
        """Nodes with no parent hashes."""
        return [node for node in self._nodes_by_id.values() if not node.parent_hashes]

    def get_leaves(self) -> List[EvidenceNode]:
        """Nodes with no children."""
        all_child_parents = set(self._children_by_hash.keys())
        return [node for node in self._nodes_by_id.values() if node.hash_digest not in all_child_parents or not self._children_by_hash[node.hash_digest]]

    def compute_merkle_root(self) -> Tuple[str, List[MerkleNode]]:
        """Constructs a deterministic binary Merkle tree over all sorted leaf/node hashes."""
        if not self._nodes_by_hash:
            empty_hash = hashlib.sha256(b"empty_evidence_graph").hexdigest()
            self._merkle_root = empty_hash
            return empty_hash, []

        sorted_hashes = sorted(self._nodes_by_hash.keys())
        current_layer: List[MerkleNode] = [
            MerkleNode(hash_value=h, evidence_id=self._nodes_by_hash[h].evidence_id, level=0)
            for h in sorted_hashes
        ]
        all_tree_nodes: List[MerkleNode] = list(current_layer)
        level = 1

        while len(current_layer) > 1:
            next_layer: List[MerkleNode] = []
            for i in range(0, len(current_layer), 2):
                left = current_layer[i]
                if i + 1 < len(current_layer):
                    right = current_layer[i + 1]
                    combined = left.hash_value + right.hash_value
                    parent_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()
                    parent_node = MerkleNode(
                        hash_value=parent_hash,
                        left_child=left.hash_value,
                        right_child=right.hash_value,
                        level=level,
                    )
                else:
                    # Odd node is paired with duplicate self
                    combined = left.hash_value + left.hash_value
                    parent_hash = hashlib.sha256(combined.encode("utf-8")).hexdigest()
                    parent_node = MerkleNode(
                        hash_value=parent_hash,
                        left_child=left.hash_value,
                        right_child=left.hash_value,
                        level=level,
                    )
                next_layer.append(parent_node)
                all_tree_nodes.append(parent_node)
            current_layer = next_layer
            level += 1

        root_hash = current_layer[0].hash_value
        self._merkle_root = root_hash
        return root_hash, all_tree_nodes

    def verify_integrity(self) -> Tuple[bool, List[str]]:
        """Verifies hash consistency of every node and parent link."""
        errors: List[str] = []
        for node in self._nodes_by_id.values():
            recomputed = node.compute_hash()
            if recomputed != node.hash_digest:
                errors.append(f"Node {node.evidence_id} hash mismatch: computed {recomputed} != recorded {node.hash_digest}")
            for ph in node.parent_hashes:
                if ph not in self._nodes_by_hash:
                    errors.append(f"Node {node.evidence_id} references missing parent hash {ph}")
        return len(errors) == 0, errors

    def to_dict(self) -> Dict[str, Any]:
        root_hash, _ = self.compute_merkle_root()
        return {
            "graph_id": self.graph_id,
            "total_nodes": len(self._nodes_by_id),
            "merkle_root": root_hash,
            "roots": [n.evidence_id for n in self.get_roots()],
            "leaves": [n.evidence_id for n in self.get_leaves()],
            "nodes": [n.to_dict() for n in self._nodes_by_id.values()],
        }
