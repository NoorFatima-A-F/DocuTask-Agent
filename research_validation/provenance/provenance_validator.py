"""
Evidence Provenance & Scientific Lineage Framework
Module: provenance_validator.py

Formal validator auditing scientific evidence graphs for:
- Missing lineage trails
- Cryptographic hash corruptions (Merkle tampering)
- Invalid or expired digital signatures
- Cyclic graph dependencies
- Missing parent entity pointers
- Orphan unattached nodes
- Duplicate node IDs
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Set

from research_validation.provenance.digital_signatures import DetachedSignature, ProvenanceSigner
from research_validation.provenance.evidence_graph import EvidenceGraph
from research_validation.provenance.merkle_dag import MerkleVerificationResult
from research_validation.provenance.provenance_models import LineageStage


class ProvenanceValidationVerdict(str, Enum):
    VALIDATION_PASSED = "VALIDATION_PASSED"
    TAMPERING_DETECTED = "TAMPERING_DETECTED"
    BROKEN_LINEAGE = "BROKEN_LINEAGE"
    CYCLE_DETECTED = "CYCLE_DETECTED"
    INVALID_SIGNATURE = "INVALID_SIGNATURE"
    ORPHAN_NODES_FOUND = "ORPHAN_NODES_FOUND"


@dataclass
class ProvenanceAuditReport:
    """Comprehensive scientific provenance validation audit report."""
    verdict: ProvenanceValidationVerdict
    is_valid: bool
    total_nodes_audited: int
    merkle_verification: MerkleVerificationResult
    orphan_node_ids: List[str]
    missing_parent_ids: List[str]
    broken_signature_node_ids: List[str]
    diagnostics: List[str]
    quality_score: float


class ProvenanceValidator:
    """
    Zero-trust validation engine for evidence lineage integrity.
    """

    @classmethod
    def audit_graph(
        cls,
        graph: EvidenceGraph,
        expected_secret_or_pubkey: Optional[str] = None
    ) -> ProvenanceAuditReport:
        """
        Execute comprehensive zero-trust audit across an Evidence Graph.
        """
        diagnostics: List[str] = []
        orphan_nodes: List[str] = []
        missing_parents: List[str] = []
        broken_signatures: List[str] = []

        # 1. Merkle DAG integrity
        merkle_res = graph.verify_graph_integrity()
        if not merkle_res.is_valid:
            diagnostics.extend(merkle_res.diagnostics)

        # 2. Check for missing parents and orphan nodes
        all_ids = set(graph.merkle_dag.nodes.keys())
        all_referenced_parents: Set[str] = set()

        for node_id, node in graph.merkle_dag.nodes.items():
            for pid in node.parent_node_ids:
                all_referenced_parents.add(pid)
                if pid not in all_ids:
                    missing_parents.append(pid)
                    diagnostics.append(f"Node '{node_id}' references non-existent parent '{pid}'.")

        # Orphan nodes (nodes that have no parents and are never referenced by any child, except single-node graphs)
        if len(all_ids) > 1:
            for node_id, node in graph.merkle_dag.nodes.items():
                if len(node.parent_node_ids) == 0 and node_id not in all_referenced_parents and node.stage != LineageStage.RAW_OBSERVATION:
                    orphan_nodes.append(node_id)
                    diagnostics.append(f"Orphan node '{node_id}' is unattached to any lineage chain.")

        # 3. Signature verification for DIGITAL_SIGNATURE nodes
        if expected_secret_or_pubkey:
            for node_id, node in graph.merkle_dag.nodes.items():
                if node.stage == LineageStage.DIGITAL_SIGNATURE:
                    sig_b64 = node.payload.get("signature_b64")
                    key_id = node.payload.get("key_id")
                    signed_dig = node.payload.get("signed_digest")
                    exp_at = node.payload.get("expires_at", 0.0)

                    if sig_b64 and key_id and signed_dig:
                        sig_obj = DetachedSignature(
                            key_id=key_id,
                            algorithm=node.payload.get("algorithm", "HMAC-SHA256"),
                            signature_base64=sig_b64,
                            payload_digest_sha256=signed_dig,
                            signed_at_epoch=node.created_at_epoch,
                            expires_at_epoch=exp_at,
                            signer_identity=node.environment.author
                        )
                        # Verify against parent node (which is the scientific report)
                        parent_digests = node.parent_hashes
                        if not parent_digests or signed_dig not in parent_digests:
                            broken_signatures.append(node_id)
                            diagnostics.append(f"Digital signature node '{node_id}' signed digest does not match parent report digest.")
                        else:
                            is_ok, reason = ProvenanceSigner.verify_signature(
                                sig_obj,
                                expected_digest_hex=signed_dig,
                                secret_or_public_key=expected_secret_or_pubkey
                            )
                            if not is_ok:
                                broken_signatures.append(node_id)
                                diagnostics.append(f"Digital signature node '{node_id}' failed cryptographic verification: {reason}")

        # Determine verdict
        if not merkle_res.is_valid:
            verdict = ProvenanceValidationVerdict.TAMPERING_DETECTED if "altered" in " ".join(diagnostics) else ProvenanceValidationVerdict.CYCLE_DETECTED
        elif missing_parents:
            verdict = ProvenanceValidationVerdict.BROKEN_LINEAGE
        elif broken_signatures:
            verdict = ProvenanceValidationVerdict.INVALID_SIGNATURE
        elif orphan_nodes:
            verdict = ProvenanceValidationVerdict.ORPHAN_NODES_FOUND
        else:
            verdict = ProvenanceValidationVerdict.VALIDATION_PASSED

        is_valid = (verdict == ProvenanceValidationVerdict.VALIDATION_PASSED)

        # Graph quality score
        weights = [n.quality_level.numeric_weight for n in graph.merkle_dag.nodes.values()]
        score = sum(weights) / len(weights) if weights else 0.0

        return ProvenanceAuditReport(
            verdict=verdict,
            is_valid=is_valid,
            total_nodes_audited=len(all_ids),
            merkle_verification=merkle_res,
            orphan_node_ids=orphan_nodes,
            missing_parent_ids=missing_parents,
            broken_signature_node_ids=broken_signatures,
            diagnostics=diagnostics,
            quality_score=score
        )
