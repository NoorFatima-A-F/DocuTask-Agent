"""
Unit and integration tests for Phase V6 — Enterprise Knowledge Platform Verification & Validation Program (EKPVVP).
"""

import os
import json
import pytest
from app.knowledge_platform_verification import (
    PartId,
    KnowledgeAssetType,
    MemoryTier,
    RetrievalMode,
    VerificationStatus,
    KnowledgeAsset,
    RetrievalResult,
    GraphNode,
    GraphEdge,
    MemoryEntry,
    KnowledgePlatformScorer,
    EvidenceGenerator,
)
from app.knowledge_platform_verification.ingestion.ingestion_verifier import IngestionVerifier
from app.knowledge_platform_verification.registry.registry_verifier import RegistryVerifier
from app.knowledge_platform_verification.embeddings.embedding_verifier import EmbeddingVerifier
from app.knowledge_platform_verification.vectordb.vectordb_verifier import VectorDbVerifier
from app.knowledge_platform_verification.retrieval.hybrid_retrieval_verifier import HybridRetrievalVerifier
from app.knowledge_platform_verification.reranking.reranking_verifier import RerankingVerifier
from app.knowledge_platform_verification.context.context_engineering_verifier import ContextEngineeringVerifier
from app.knowledge_platform_verification.graph.knowledge_graph_verifier import KnowledgeGraphVerifier
from app.knowledge_platform_verification.memory.memory_verifier import MemoryVerifier
from app.knowledge_platform_verification.quality.quality_verifier import QualityVerifier
from app.knowledge_platform_verification.freshness.freshness_verifier import FreshnessVerifier
from app.knowledge_platform_verification.drift.drift_verifier import DriftVerifier
from app.knowledge_platform_verification.security.security_verifier import SecurityVerifier
from app.knowledge_platform_verification.optimization.optimization_verifier import OptimizationVerifier
from app.knowledge_platform_verification.explainability.explainability_verifier import ExplainabilityVerifier
from app.knowledge_platform_verification.scalability.scalability_verifier import ScalabilityVerifier
from app.knowledge_platform_verification.benchmarking.benchmarking_verifier import BenchmarkingVerifier
from app.knowledge_platform_verification.dashboards.dashboard_verifier import DashboardVerifier


def test_domain_models():
    asset = KnowledgeAsset(
        asset_id="ast_101",
        tenant_id="tenant_alpha",
        asset_type=KnowledgeAssetType.PDF,
        title="Enterprise Security Policy 2026",
        content="All data must be encrypted with AES-256.",
    )
    d = asset.to_dict()
    assert d["asset_id"] == "ast_101"
    assert d["asset_type"] == "PDF"

    retrieval = RetrievalResult(
        chunk_id="chk_01",
        asset_id="ast_101",
        content="AES-256 requirement",
        score=0.985,
        rank=1,
        retrieval_mode=RetrievalMode.HYBRID_WEIGHTED,
    )
    assert retrieval.to_dict()["rank"] == 1

    node = GraphNode(node_id="n1", entity_type="Policy", name="GDPR")
    edge = GraphEdge(source_id="n1", target_id="n2", relation_type="GOVERNS")
    assert node.to_dict()["name"] == "GDPR"
    assert edge.to_dict()["relation_type"] == "GOVERNS"

    mem = MemoryEntry(
        entry_id="mem_1",
        tier=MemoryTier.ORGANIZATIONAL,
        tenant_id="tenant_alpha",
        agent_id="agent_1",
        key="fiscal_year_end",
        value="12-31",
    )
    assert mem.to_dict()["tier"] == "ORGANIZATIONAL"


def test_part_01_ingestion():
    v = IngestionVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_01_INGESTION
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_02_registry():
    v = RegistryVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_02_REGISTRY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_03_embeddings():
    v = EmbeddingVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_03_EMBEDDINGS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_04_vectordb():
    v = VectorDbVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_04_VECTORDB
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_05_retrieval():
    v = HybridRetrievalVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_05_RETRIEVAL
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_06_reranking():
    v = RerankingVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_06_RERANKING
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_07_context():
    v = ContextEngineeringVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_07_CONTEXT
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_08_graph():
    v = KnowledgeGraphVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_08_GRAPH
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_09_memory():
    v = MemoryVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_09_MEMORY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_10_quality():
    v = QualityVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_10_QUALITY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_11_freshness():
    v = FreshnessVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_11_FRESHNESS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_12_drift():
    v = DriftVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_12_DRIFT
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_13_security():
    v = SecurityVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_13_SECURITY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_14_optimization():
    v = OptimizationVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_14_OPTIMIZATION
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_15_explainability():
    v = ExplainabilityVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_15_EXPLAINABILITY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_16_scalability():
    v = ScalabilityVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_16_SCALABILITY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_17_benchmarking():
    v = BenchmarkingVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_17_BENCHMARKING
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_18_dashboards():
    v = DashboardVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_18_DASHBOARDS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_knowledge_scorer_and_scorecard():
    scorer = KnowledgePlatformScorer()
    scorecard = scorer.run_all()

    assert scorecard.composite_score == 100.0
    assert scorecard.grade == "A+"
    assert scorecard.production_ready is True
    assert scorecard.total_assertions == 72
    assert scorecard.passed_assertions == 72
    assert len(scorecard.parts) == 18
    assert len(scorecard.indices) == 10
    assert scorecard.total_execution_time_ms < 1000.0


def test_evidence_export_and_manifest(tmp_path):
    out_dir = tmp_path / "evidence"
    report_file = tmp_path / "docs" / "report.md"

    scorer = KnowledgePlatformScorer()
    scorecard = scorer.run_all()

    exporter = EvidenceGenerator(output_dir=str(out_dir), report_path=str(report_file))
    summary = exporter.export_all(scorecard)

    assert os.path.exists(summary["manifest_file"])
    assert os.path.exists(summary["report_path"])

    with open(summary["manifest_file"], "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["composite_score"] == 100.0
    assert manifest["production_ready"] is True
    assert len(manifest["checksums"]) == 19  # 1 summary + 18 parts
