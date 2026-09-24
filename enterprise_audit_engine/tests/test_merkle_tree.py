"""Tests for Cryptographic Merkle Evidence Tree and Proof Verification."""

from enterprise_audit_engine.certification.merkle_tree import MerkleEvidenceTree
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceSourceType,
    EvidenceClassification,
    EvidenceConfidence,
)


def _create_dummy_record(eid: str, summary: str) -> EvidenceRecord:
    rec = EvidenceRecord(
        id=eid,
        collector="test_col",
        source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
        category="ArchitectureAndDesign",
        summary=summary,
        raw_payload={"summary": summary},
        confidence=EvidenceConfidence.HIGH,
        classification=EvidenceClassification.VERIFIED,
    )
    return rec.model_copy(update={"content_hash": rec.calculate_hash()})


def test_merkle_tree_construction_and_root():
    records = [
        _create_dummy_record("EV-001", "Summary 1"),
        _create_dummy_record("EV-002", "Summary 2"),
        _create_dummy_record("EV-003", "Summary 3"),
    ]
    tree = MerkleEvidenceTree(records)
    assert tree.merkle_root is not None
    assert len(tree.merkle_root) == 64  # SHA-256 hex string

    # Tree depth for 3 leaves is 3
    assert len(tree.levels) == 3


def test_merkle_proof_verification_success():
    records = [
        _create_dummy_record("EV-001", "Summary 1"),
        _create_dummy_record("EV-002", "Summary 2"),
        _create_dummy_record("EV-003", "Summary 3"),
        _create_dummy_record("EV-004", "Summary 4"),
    ]
    tree = MerkleEvidenceTree(records)
    root = tree.merkle_root

    for rec in records:
        proof = tree.get_proof(rec.id)
        assert len(proof) > 0
        leaf_hash = MerkleEvidenceTree.compute_leaf_hash(rec)
        is_valid = MerkleEvidenceTree.verify_proof(leaf_hash, proof, root)
        assert is_valid is True


def test_merkle_proof_tampered_leaf_failure():
    records = [
        _create_dummy_record("EV-001", "Summary 1"),
        _create_dummy_record("EV-002", "Summary 2"),
    ]
    tree = MerkleEvidenceTree(records)
    root = tree.merkle_root

    proof = tree.get_proof("EV-001")
    tampered_hash = "deadbeef" * 8

    is_valid = MerkleEvidenceTree.verify_proof(tampered_hash, proof, root)
    assert is_valid is False
