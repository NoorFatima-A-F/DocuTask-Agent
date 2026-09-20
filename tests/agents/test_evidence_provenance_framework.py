"""
Evidence Provenance & Scientific Lineage Framework
Comprehensive Automated Test Suite (Phase 71 + Evidence Quality Scoring)

Tests Merkle DAG integrity, W3C PROV/OpenLineage serialization, digital signatures,
tamper detection, immutable store versioning, visualizers, and quality level grading.
"""

import json
import math
import pytest
from pathlib import Path

from research_validation.provenance.hashing import HashAlgorithm, ProvenanceHasher
from research_validation.provenance.provenance_models import (
    EvidenceNode, EvidenceQualityLevel, LineageStage, EnvironmentFingerprint,
    ProvEntity, ProvActivity, ProvAgent, ProvRelationType
)
from research_validation.provenance.merkle_dag import MerkleDAG, MerkleVerificationResult
from research_validation.provenance.digital_signatures import (
    DetachedSignature, ProvenanceSigner, SignatureAlgorithm, CertificateInfo
)
from research_validation.provenance.provenance_schema import (
    ProvDocument, ProvRelation, OpenLineageJob, OpenLineageRun,
    OpenLineageDataset, OpenLineageInputDataset, OpenLineageOutputDataset,
    OpenLineageRunEvent, OpenLineageEventType
)
from research_validation.provenance.provenance_serialization import ProvenanceSerializer
from research_validation.provenance.evidence_graph import EvidenceGraph, LineageAncestryTrace
from research_validation.provenance.lineage_tracker import LineageTracker, CompleteLineageChain
from research_validation.provenance.evidence_store import EvidenceStore, VersionedEvidenceRecord
from research_validation.provenance.evidence_diff import EvidenceDiffer, EvidenceBundleDiffReport
from research_validation.provenance.provenance_validator import (
    ProvenanceValidator, ProvenanceAuditReport, ProvenanceValidationVerdict
)
from research_validation.provenance.provenance_visualizer import ProvenanceVisualizer
from research_validation.provenance.evidence_bundle import EvidenceBundleBuilder, SealedEvidenceBundle
from research_validation.provenance.provenance_api import ProvenanceAPI
from research_validation.provenance.provenance_engine import ProvenanceEngine


def test_hashing_algorithms():
    text = "Benchmark Observation Raw Data 2026"
    h_sha256 = ProvenanceHasher.hash_string(text, HashAlgorithm.SHA256)
    h_sha3 = ProvenanceHasher.hash_string(text, HashAlgorithm.SHA3_512)
    h_blake3 = ProvenanceHasher.hash_string(text, HashAlgorithm.BLAKE3)

    assert len(h_sha256) == 64
    assert len(h_sha3) == 128
    assert len(h_blake3) == 64

    # Canonical JSON hashing (order independent)
    obj1 = {"b": 2, "a": 1, "nested": {"y": 20, "x": 10}}
    obj2 = {"a": 1, "nested": {"x": 10, "y": 20}, "b": 2}
    assert ProvenanceHasher.hash_canonical_json(obj1) == ProvenanceHasher.hash_canonical_json(obj2)


def test_merkle_dag_construction_and_tampering():
    graph = EvidenceGraph()

    # 1. Add root observation node
    n1 = graph.record_node(
        node_id="raw_1",
        stage=LineageStage.RAW_OBSERVATION,
        name="Raw OCR Benchmarks",
        description="500 inference latency measurements",
        payload={"mean": 42.5},
        parent_node_ids=[],
        quality_level=EvidenceQualityLevel.LEVEL_B
    )

    # 2. Add child metric node
    n2 = graph.record_node(
        node_id="metric_1",
        stage=LineageStage.FINAL_METRIC,
        name="Latency P99",
        description="Measured P99 latency",
        payload={"p99": 110.2},
        parent_node_ids=["raw_1"],
        quality_level=EvidenceQualityLevel.LEVEL_B
    )

    assert n2.parent_hashes == [n1.node_hash]

    # Verify integrity
    res = graph.verify_graph_integrity()
    assert res.is_valid is True
    assert res.verified_nodes == 2
    assert len(res.root_merkle_digest) == 64

    # Tamper test: perturb n1 payload directly
    n1.payload["mean"] = 999.9
    res_tampered = graph.verify_graph_integrity()
    assert res_tampered.is_valid is False
    assert "raw_1" in res_tampered.corrupted_nodes


def test_digital_signatures():
    signer = ProvenanceSigner(
        key_id="KEY-TEST-01",
        secret_or_private_key="super_secret_signing_key"
    )
    digest = ProvenanceHasher.hash_string("Report Summary Claims")
    sig = signer.sign_digest(digest, signer_identity="Auditor A")

    assert sig.key_id == "KEY-TEST-01"
    assert sig.payload_digest_sha256 == digest
    assert sig.is_expired() is False

    # Valid verification
    is_valid, reason = ProvenanceSigner.verify_signature(sig, digest, "super_secret_signing_key")
    assert is_valid is True

    # Tampered digest verification
    bad_digest = ProvenanceHasher.hash_string("Tampered Claims")
    is_valid_bad, reason_bad = ProvenanceSigner.verify_signature(sig, bad_digest, "super_secret_signing_key")
    assert is_valid_bad is False
    assert "Digest mismatch" in reason_bad

    # Expired signature verification
    sig_expired = DetachedSignature(
        key_id="KEY-TEST-01",
        algorithm=SignatureAlgorithm.HMAC_SHA256,
        signature_base64=sig.signature_base64,
        payload_digest_sha256=digest,
        signed_at_epoch=1000.0,
        expires_at_epoch=2000.0,
        signer_identity="Auditor A"
    )
    is_exp, reason_exp = ProvenanceSigner.verify_signature(
        sig_expired, digest, "super_secret_signing_key", check_time=3000.0
    )
    assert is_exp is False
    assert "expired" in reason_exp


def test_w3c_prov_serialization():
    doc = ProvDocument(document_id="doc_prov_001")
    e1 = ProvEntity("e_data", "Raw Document Dataset", {"size": "50MB"})
    a1 = ProvActivity("a_parse", "OCR Extraction", 1000.0, 1050.0, ["e_data"])
    ag1 = ProvAgent("ag_parser", "Deterministic Parser Service", "SoftwareAgent")

    doc.add_entity(e1)
    doc.add_activity(a1)
    doc.add_agent(ag1)
    doc.add_relation(ProvRelation(ProvRelationType.USED, "a_parse", "e_data"))
    doc.add_relation(ProvRelation(ProvRelationType.WAS_ASSOCIATED_WITH, "a_parse", "ag_parser"))

    json_ld = ProvenanceSerializer.to_json_ld(doc)
    assert "@context" in json_ld
    assert "prov:Entity" in json_ld

    prov_n = ProvenanceSerializer.to_prov_n(doc)
    assert "entity(rvisf:e_data" in prov_n
    assert "activity(rvisf:a_parse" in prov_n

    prov_xml = ProvenanceSerializer.to_prov_xml(doc)
    assert "<prov:entity" in prov_xml
    assert "<prov:activity" in prov_xml


def test_openlineage_schema_serialization():
    event = OpenLineageRunEvent(
        eventType=OpenLineageEventType.COMPLETE,
        eventTime="2026-09-08T12:00:00Z",
        run=OpenLineageRun(runId="run-abc-123", facets={"environment": "Cloud Run"}),
        job=OpenLineageJob(namespace="rvisf.provenance", name="document_benchmark_job"),
        inputs=[OpenLineageInputDataset(OpenLineageDataset("gcs://bucket", "invoices_test"))],
        outputs=[OpenLineageOutputDataset(OpenLineageDataset("gcs://bucket", "metrics_f1"))]
    )
    ol_json = ProvenanceSerializer.to_openlineage_json(event)
    data = json.loads(ol_json)
    assert data["eventType"] == "COMPLETE"
    assert data["job"]["name"] == "document_benchmark_job"
    assert len(data["inputs"]) == 1


def test_evidence_store_immutability_and_versioning(tmp_path: Path):
    store = EvidenceStore(storage_dir=tmp_path)
    env = EvidenceGraph.capture_current_environment()

    n1 = EvidenceNode("node_v1", LineageStage.FINAL_METRIC, "F1 Score", "Run 1", {"f1": 0.95}, [], [], env, EvidenceQualityLevel.LEVEL_B)
    n2 = EvidenceNode("node_v2", LineageStage.FINAL_METRIC, "F1 Score", "Run 2", {"f1": 0.96}, ["node_v1"], [n1.node_hash], env, EvidenceQualityLevel.LEVEL_B)

    # Store version 1
    r1 = store.store_evidence_node(n1, logical_key="f1_metric")
    assert r1.version_number == 1
    assert r1.previous_version_record_id is None

    # Store version 2 under same logical key
    r2 = store.store_evidence_node(n2, logical_key="f1_metric")
    assert r2.version_number == 2
    assert r2.previous_version_record_id == "node_v1"

    # Attempting to re-insert node_v1 must raise PermissionError
    with pytest.raises(PermissionError):
        store.store_evidence_node(n1, logical_key="f1_metric")

    # Retrieve history
    history = store.get_version_history("f1_metric")
    assert len(history) == 2
    assert history[0].evidence_node.payload["f1"] == 0.95
    assert history[1].evidence_node.payload["f1"] == 0.96


def test_evidence_differ():
    env1 = EvidenceGraph.capture_current_environment(git_commit_sha="commit_aaa")
    env2 = EvidenceGraph.capture_current_environment(git_commit_sha="commit_bbb")

    node1 = EvidenceNode("n1", LineageStage.FINAL_METRIC, "F1 Metric", "Run 1", {"f1": 0.92, "latency_ms": 50.0}, [], [], env1, EvidenceQualityLevel.LEVEL_C)
    node2 = EvidenceNode("n2", LineageStage.FINAL_METRIC, "F1 Metric", "Run 2", {"f1": 0.96, "latency_ms": 45.0}, ["n1"], [node1.node_hash], env2, EvidenceQualityLevel.LEVEL_B)

    diff = EvidenceDiffer.compare_nodes(node1, node2)
    assert len(diff.metric_deltas) == 2
    assert diff.environment_delta.git_commit_changed is True
    assert diff.quality_level_changed is True
    assert "| `f1` | 0.9200 | 0.9600 |" in diff.summary_markdown


def test_provenance_validator():
    graph = EvidenceGraph()
    n1 = graph.record_node("r1", LineageStage.RAW_OBSERVATION, "Raw", "Raw data", {}, [], EvidenceQualityLevel.LEVEL_B)
    n2 = graph.record_node("m1", LineageStage.FINAL_METRIC, "Metric", "Metric data", {}, ["r1"], EvidenceQualityLevel.LEVEL_B)

    audit = ProvenanceValidator.audit_graph(graph)
    assert audit.is_valid is True
    assert audit.verdict == ProvenanceValidationVerdict.VALIDATION_PASSED
    assert audit.quality_score == EvidenceQualityLevel.LEVEL_B.numeric_weight


def test_provenance_visualizer():
    graph = EvidenceGraph()
    n1 = graph.record_node("r1", LineageStage.RAW_OBSERVATION, "Raw Observations", "500 samples", {}, [], EvidenceQualityLevel.LEVEL_A)
    n2 = graph.record_node("m1", LineageStage.FINAL_METRIC, "Entity Macro F1", "F1=0.96", {}, ["r1"], EvidenceQualityLevel.LEVEL_A)

    # Mermaid
    mermaid_str = ProvenanceVisualizer.to_mermaid(graph)
    assert "flowchart TD" in mermaid_str
    assert "r1 --> m1" in mermaid_str

    # DOT
    dot_str = ProvenanceVisualizer.to_graphviz_dot(graph)
    assert "digraph ProvenanceLineage" in dot_str
    assert '"r1" -> "m1"' in dot_str

    # SVG
    svg_str = ProvenanceVisualizer.to_svg(graph)
    assert "<svg" in svg_str
    assert "Scientific Lineage Merkle DAG" in svg_str

    # Interactive HTML
    html_str = ProvenanceVisualizer.to_interactive_html(graph)
    assert "<!DOCTYPE html>" in html_str
    assert "mermaid" in html_str


def test_sealed_evidence_bundle():
    graph = EvidenceGraph()
    graph.record_node("r1", LineageStage.RAW_OBSERVATION, "Raw", "desc", {}, [], EvidenceQualityLevel.LEVEL_A)
    graph.record_node("m1", LineageStage.FINAL_METRIC, "F1", "desc", {}, ["r1"], EvidenceQualityLevel.LEVEL_A)

    signer = ProvenanceSigner("KEY-BUNDLE", "test_key_123")
    bundle = EvidenceBundleBuilder.build_bundle(graph, signer=signer)

    assert bundle.overall_quality_level == EvidenceQualityLevel.LEVEL_A
    assert len(bundle.root_merkle_digest) == 64

    # Verify bundle
    is_ok, reason = bundle.verify("test_key_123")
    assert is_ok is True


def test_complete_7_stage_lineage_pipeline_and_quality_scoring():
    engine = ProvenanceEngine()
    raw_samples = [10.0, 12.0, 11.0, 13.0, 10.5, 11.5]

    chain = engine.record_empirical_pipeline(
        chain_name="Document Parser Latency",
        raw_samples=raw_samples,
        transformation_fn=lambda xs: [x for x in xs if x > 0],
        aggregation_fn=lambda xs: sum(xs) / len(xs),
        metric_name="Mean Latency ms",
        report_title="Document Ingestion Benchmark Report",
        quality_level=EvidenceQualityLevel.LEVEL_A
    )

    assert chain.raw_observation_node.stage == LineageStage.RAW_OBSERVATION
    assert chain.transformation_node.stage == LineageStage.TRANSFORMATION
    assert chain.intermediate_artifact_node.stage == LineageStage.INTERMEDIATE_ARTIFACT
    assert chain.aggregation_node.stage == LineageStage.AGGREGATION
    assert chain.final_metric_node.stage == LineageStage.FINAL_METRIC
    assert chain.scientific_report_node.stage == LineageStage.SCIENTIFIC_REPORT
    assert chain.digital_signature_node.stage == LineageStage.DIGITAL_SIGNATURE

    # Trace unbroken lineage
    trace = chain.ancestry_trace
    assert trace.is_unbroken_merkle_chain is True
    assert trace.overall_quality_level == EvidenceQualityLevel.LEVEL_A
    assert trace.evidence_quality_score == 1.0

    # Compute quality-weighted readiness
    readiness = engine.compute_quality_weighted_readiness()
    assert readiness["total_evidence_nodes"] == 7
    assert readiness["weighted_readiness_score"] == 1.0
    assert readiness["overall_quality_grade"] == "LEVEL_A"
    assert readiness["is_ready_for_external_review"] is True
