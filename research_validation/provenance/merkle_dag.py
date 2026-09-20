"""
Evidence Provenance & Scientific Lineage Framework
Module: merkle_dag.py

Implements Merkle Directed Acyclic Graph (DAG) construction, recursive hash chaining,
and descendant tampering invalidation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple

from research_validation.provenance.hashing import HashAlgorithm, ProvenanceHasher
from research_validation.provenance.provenance_models import EvidenceNode, LineageStage


@dataclass
class MerkleVerificationResult:
    """Detailed verification outcome for a Merkle DAG."""
    is_valid: bool
    total_nodes: int
    verified_nodes: int
    corrupted_nodes: List[str]
    broken_edges: List[Tuple[str, str]]
    root_merkle_digest: str
    diagnostics: List[str]


class MerkleDAG:
    """
    Cryptographically sealed Directed Acyclic Graph of scientific evidence nodes.
    """

    def __init__(self, algorithm: HashAlgorithm = HashAlgorithm.SHA256):
        self.algorithm = algorithm
        self.nodes: Dict[str, EvidenceNode] = {}
        self.children_map: Dict[str, Set[str]] = {}  # parent_id -> set of child_ids
        self.parents_map: Dict[str, Set[str]] = {}   # child_id -> set of parent_ids

    def add_node(self, node: EvidenceNode) -> None:
        """Add an immutable evidence node to the Merkle DAG."""
        if node.node_id in self.nodes:
            raise ValueError(f"Node '{node.node_id}' already exists in Merkle DAG. Overwriting forbidden.")

        # Ensure parent nodes exist
        for parent_id in node.parent_node_ids:
            if parent_id not in self.nodes:
                raise KeyError(f"Parent node '{parent_id}' does not exist in Merkle DAG.")

        self.nodes[node.node_id] = node
        self.parents_map[node.node_id] = set(node.parent_node_ids)

        if node.node_id not in self.children_map:
            self.children_map[node.node_id] = set()

        for parent_id in node.parent_node_ids:
            if parent_id not in self.children_map:
                self.children_map[parent_id] = set()
            self.children_map[parent_id].add(node.node_id)

    def get_node(self, node_id: str) -> Optional[EvidenceNode]:
        return self.nodes.get(node_id)

    def compute_root_digest(self) -> str:
        """
        Compute root Merkle digest covering all terminal/sink nodes in the DAG.
        """
        if not self.nodes:
            return ProvenanceHasher.hash_string("EMPTY_MERKLE_DAG", algorithm=self.algorithm)

        # Terminal nodes are nodes with no outgoing children
        terminal_nodes = [n for node_id, n in self.nodes.items() if len(self.children_map.get(node_id, set())) == 0]
        terminal_hashes = sorted([n.node_hash for n in terminal_nodes])
        return ProvenanceHasher.combine_hashes(terminal_hashes, algorithm=self.algorithm)

    def verify_integrity(self) -> MerkleVerificationResult:
        """
        Walk all nodes and verify that:
        1. Each node's hash matches its recomputed canonical content.
        2. Each node's parent_hashes match the actual current hashes of its parents.
        """
        corrupted_nodes: List[str] = []
        broken_edges: List[Tuple[str, str]] = []
        diagnostics: List[str] = []
        verified_count = 0

        # Check topological order / cycles
        if self._has_cycle():
            diagnostics.append("CYCLES_DETECTED: Graph contains at least one circular dependency.")
            return MerkleVerificationResult(
                is_valid=False,
                total_nodes=len(self.nodes),
                verified_nodes=0,
                corrupted_nodes=[],
                broken_edges=[],
                root_merkle_digest="",
                diagnostics=diagnostics
            )

        for node_id, node in self.nodes.items():
            # 1. Verify parent hashes match parent nodes
            expected_parent_hashes = sorted([self.nodes[pid].node_hash for pid in node.parent_node_ids])
            if sorted(node.parent_hashes) != expected_parent_hashes:
                corrupted_nodes.append(node_id)
                for pid in node.parent_node_ids:
                    broken_edges.append((pid, node_id))
                diagnostics.append(f"Node '{node_id}' parent hashes mismatched with actual parent nodes.")
                continue

            # 2. Verify self hash
            content_to_hash = {
                "node_id": node.node_id,
                "stage": node.stage.value,
                "name": node.name,
                "description": node.description,
                "payload": node.payload,
                "parent_hashes": sorted(node.parent_hashes),
                "environment": node.environment.canonical_dict(),
                "quality_level": node.quality_level.value,
                "created_at_epoch": node.created_at_epoch,
            }
            recomputed_hash = ProvenanceHasher.hash_canonical_json(content_to_hash, algorithm=node.algorithm)
            if recomputed_hash != node.node_hash:
                corrupted_nodes.append(node_id)
                diagnostics.append(f"Node '{node_id}' payload/metadata altered. Recorded: {node.node_hash[:12]}..., Computed: {recomputed_hash[:12]}...")
            else:
                verified_count += 1

        is_valid = (len(corrupted_nodes) == 0 and len(broken_edges) == 0)
        root_digest = self.compute_root_digest() if is_valid else ""

        return MerkleVerificationResult(
            is_valid=is_valid,
            total_nodes=len(self.nodes),
            verified_nodes=verified_count,
            corrupted_nodes=corrupted_nodes,
            broken_edges=broken_edges,
            root_merkle_digest=root_digest,
            diagnostics=diagnostics
        )

    def get_descendant_node_ids(self, node_id: str) -> Set[str]:
        """Get all downstream descendant nodes that depend on a given node."""
        descendants: Set[str] = set()
        queue = list(self.children_map.get(node_id, set()))
        while queue:
            curr = queue.pop(0)
            if curr not in descendants:
                descendants.add(curr)
                queue.extend(list(self.children_map.get(curr, set())))
        return descendants

    def _has_cycle(self) -> bool:
        """Check for cycles using DFS color marking."""
        visited: Dict[str, int] = {k: 0 for k in self.nodes}  # 0=unvisited, 1=visiting, 2=visited

        def dfs(u: str) -> bool:
            visited[u] = 1
            for v in self.children_map.get(u, set()):
                if visited[v] == 1:
                    return True
                if visited[v] == 0 and dfs(v):
                    return True
            visited[u] = 2
            return False

        for n in self.nodes:
            if visited[n] == 0:
                if dfs(n):
                    return True
        return False
