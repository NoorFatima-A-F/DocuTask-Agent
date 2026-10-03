"""Tests for Execution Evidence Data Structures, Builders, Graphs, and Merkle Trees."""

from app.runtime.evidence.artifact_registry import ArtifactRegistry
from app.runtime.evidence.evidence_builder import EvidenceBuilder
from app.runtime.evidence.evidence_graph import EvidenceGraph
from app.runtime.evidence.evidence_validator import EvidenceValidator
from app.runtime.evidence.execution_evidence import (
    EvidenceNode,
    EvidenceStatus,
    EvidenceType,
)


def test_evidence_node_hashing_and_sealing():
    node = EvidenceNode(
        evidence_id="ev-test-001",
        evidence_type=EvidenceType.PLANNER_DECISION,
        inputs={"doc_type": "invoice", "pages": 2},
        outputs={"plan": "fast_path"},
        metrics={"latency_ms": 120.0},
    )
    digest1 = node.compute_hash()
    assert len(digest1) == 64
    assert node.status == EvidenceStatus.VALID

    node.seal(private_seed="test-seed-key")
    assert node.status == EvidenceStatus.VERIFIED
    assert node.crypto_proof is not None
    assert node.crypto_proof.hash_value == digest1
    assert node.crypto_proof.signature.startswith("sig_")


def test_evidence_builder_fluent_api():
    builder = EvidenceBuilder(EvidenceType.TOOL_EXECUTION, evidence_id="ev-tool-99")
    node = (
        builder.with_source("docutask-ocr-worker")
        .with_inputs({"bbox": [10, 20, 100, 200]})
        .with_outputs({"text": "TOTAL $100"})
        .with_metrics({"ocr_confidence": 0.99})
        .with_context({"session_id": "sess-123"})
        .build_and_seal()
    )

    assert node.evidence_id == "ev-tool-99"
    assert node.source_agent == "docutask-ocr-worker"
    assert node.inputs["bbox"] == [10, 20, 100, 200]
    assert node.outputs["text"] == "TOTAL $100"
    assert node.metrics["ocr_confidence"] == 0.99
    assert node.execution_context["session_id"] == "sess-123"
    assert node.status == EvidenceStatus.VERIFIED


def test_evidence_graph_and_merkle_tree():
    graph = EvidenceGraph(graph_id="test-dag")
    n1 = EvidenceBuilder(EvidenceType.PLANNER_DECISION).with_inputs({"step": 1}).build_and_seal()
    n2 = EvidenceBuilder(EvidenceType.TOOL_EXECUTION).with_parent(n1.hash_digest).with_inputs({"step": 2}).build_and_seal()
    n3 = EvidenceBuilder(EvidenceType.VALIDATION_CHECK).with_parent(n2.hash_digest).with_inputs({"step": 3}).build_and_seal()

    graph.add_node(n1)
    graph.add_node(n2)
    graph.add_node(n3)

    assert graph.count() == 3
    roots = graph.get_roots()
    assert len(roots) == 1
    assert roots[0].evidence_id == n1.evidence_id

    leaves = graph.get_leaves()
    assert len(leaves) == 1
    assert leaves[0].evidence_id == n3.evidence_id

    root_hash, merkle_nodes = graph.compute_merkle_root()
    assert len(root_hash) == 64
    assert len(merkle_nodes) >= 3

    valid, errs = graph.verify_integrity()
    assert valid is True
    assert len(errs) == 0


def test_evidence_validator_tamper_detection():
    graph = EvidenceGraph()
    n1 = EvidenceBuilder(EvidenceType.PLANNER_DECISION).with_inputs({"x": 10}).build_and_seal()
    graph.add_node(n1)

    rep = EvidenceValidator.validate_graph(graph)
    assert rep.is_valid is True

    # Tamper with the node content
    n1.inputs["x"] = 999
    rep_tampered = EvidenceValidator.validate_graph(graph)
    assert rep_tampered.is_valid is False
    assert any("Hash mismatch" in err for err in rep_tampered.errors)


def test_artifact_registry():
    reg = ArtifactRegistry()
    art1 = reg.register("extracted_data.json", {"vendor": "ACME Corp", "amount": 1500.0})
    assert len(art1.sha256) == 64
    assert reg.contains(art1.sha256)
    assert reg.get(art1.sha256).data["vendor"] == "ACME Corp"
    assert reg.count() == 1
