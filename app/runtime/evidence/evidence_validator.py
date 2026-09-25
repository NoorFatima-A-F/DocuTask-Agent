"""Evidence Validator and Tamper Detection Engine.

Validates the cryptographic integrity, parent hash continuity, schema validity,
and non-repudiation of EvidenceNodes across the execution graph.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Tuple

from app.runtime.evidence.evidence_graph import EvidenceGraph
from app.runtime.evidence.execution_evidence import EvidenceNode


class ValidationReport:
    def __init__(self, is_valid: bool, total_checked: int, errors: List[str], warnings: List[str]):
        self.is_valid = is_valid
        self.total_checked = total_checked
        self.errors = errors
        self.warnings = warnings
        self.timestamp = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "total_checked": self.total_checked,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "errors": self.errors,
            "warnings": self.warnings,
            "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.timestamp)),
        }


class EvidenceValidator:
    @staticmethod
    def validate_node(node: EvidenceNode) -> Tuple[bool, List[str]]:
        errors: List[str] = []
        # 1. Verify computed SHA-256 matches recorded hash_digest
        computed = node.compute_hash()
        if computed != node.hash_digest:
            errors.append(
                f"Hash mismatch for {node.evidence_id}: expected {node.hash_digest}, got {computed}"
            )

        # 2. Verify crypto proof
        if not node.crypto_proof:
            errors.append(f"Node {node.evidence_id} is missing cryptographic proof")
        else:
            if node.crypto_proof.hash_value != node.hash_digest:
                errors.append(
                    f"CryptoProof hash mismatch for {node.evidence_id}: "
                    f"{node.crypto_proof.hash_value} != {node.hash_digest}"
                )

        # 3. Verify inputs and outputs are dicts
        if not isinstance(node.inputs, dict):
            errors.append(f"Node {node.evidence_id} inputs must be a dictionary")
        if not isinstance(node.outputs, dict):
            errors.append(f"Node {node.evidence_id} outputs must be a dictionary")

        return len(errors) == 0, errors

    @classmethod
    def validate_graph(cls, graph: EvidenceGraph) -> ValidationReport:
        errors: List[str] = []
        warnings: List[str] = []
        nodes = graph.list_nodes()

        if not nodes:
            warnings.append("Evidence graph is empty")
            return ValidationReport(True, 0, errors, warnings)

        for node in nodes:
            valid, node_errs = cls.validate_node(node)
            if not valid:
                errors.extend(node_errs)

            # Check parent references exist in the graph
            for ph in node.parent_hashes:
                if not graph.get_by_hash(ph):
                    errors.append(
                        f"Dangling parent hash {ph} in evidence node {node.evidence_id}"
                    )

        # Check for cycles
        visited = set()
        rec_stack = set()

        def has_cycle(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)
            node = graph.get_node(node_id)
            if node:
                for ph in node.parent_hashes:
                    parent_node = graph.get_by_hash(ph)
                    if parent_node:
                        p_id = parent_node.evidence_id
                        if p_id not in visited:
                            if has_cycle(p_id):
                                return True
                        elif p_id in rec_stack:
                            return True
            rec_stack.remove(node_id)
            return False

        for node in nodes:
            if node.evidence_id not in visited:
                if has_cycle(node.evidence_id):
                    errors.append("Cycle detected in evidence graph lineage")
                    break

        is_valid = len(errors) == 0
        return ValidationReport(is_valid, len(nodes), errors, warnings)
