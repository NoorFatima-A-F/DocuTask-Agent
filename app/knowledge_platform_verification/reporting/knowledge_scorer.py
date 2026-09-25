"""
Knowledge Platform Verification Scorer.
Executes all 18 verification engines, aggregates assertions, and calculates composite readiness score and indices.
"""

import time
from typing import Dict, Any
from ..domain.models import (
    KnowledgeReadinessScorecard,
    PartVerificationResult,
)
from ..ingestion.ingestion_verifier import IngestionVerifier
from ..registry.registry_verifier import RegistryVerifier
from ..embeddings.embedding_verifier import EmbeddingVerifier
from ..vectordb.vectordb_verifier import VectorDbVerifier
from ..retrieval.hybrid_retrieval_verifier import HybridRetrievalVerifier
from ..reranking.reranking_verifier import RerankingVerifier
from ..context.context_engineering_verifier import ContextEngineeringVerifier
from ..graph.knowledge_graph_verifier import KnowledgeGraphVerifier
from ..memory.memory_verifier import MemoryVerifier
from ..quality.quality_verifier import QualityVerifier
from ..freshness.freshness_verifier import FreshnessVerifier
from ..drift.drift_verifier import DriftVerifier
from ..security.security_verifier import SecurityVerifier
from ..optimization.optimization_verifier import OptimizationVerifier
from ..explainability.explainability_verifier import ExplainabilityVerifier
from ..scalability.scalability_verifier import ScalabilityVerifier
from ..benchmarking.benchmarking_verifier import BenchmarkingVerifier
from ..dashboards.dashboard_verifier import DashboardVerifier


class KnowledgePlatformScorer:
    """Executes all verifiers, aggregates empirical results, and produces the complete KnowledgeReadinessScorecard."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.verifiers = [
            IngestionVerifier(self.config),
            RegistryVerifier(self.config),
            EmbeddingVerifier(self.config),
            VectorDbVerifier(self.config),
            HybridRetrievalVerifier(self.config),
            RerankingVerifier(self.config),
            ContextEngineeringVerifier(self.config),
            KnowledgeGraphVerifier(self.config),
            MemoryVerifier(self.config),
            QualityVerifier(self.config),
            FreshnessVerifier(self.config),
            DriftVerifier(self.config),
            SecurityVerifier(self.config),
            OptimizationVerifier(self.config),
            ExplainabilityVerifier(self.config),
            ScalabilityVerifier(self.config),
            BenchmarkingVerifier(self.config),
            DashboardVerifier(self.config),
        ]

    def run_all(self) -> KnowledgeReadinessScorecard:
        start_time = time.perf_counter()
        part_results: Dict[str, PartVerificationResult] = {}
        total_assertions = 0
        passed_assertions = 0

        for verifier in self.verifiers:
            res = verifier.verify()
            part_results[res.part_id.value] = res
            total_assertions += res.total_assertions_count
            passed_assertions += res.passed_assertions_count

        total_elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # Calculate composite score
        total_weight = sum(p.weight for p in part_results.values())
        weighted_score = sum(p.score * p.weight for p in part_results.values()) / max(0.001, total_weight)

        grade = "A+" if weighted_score >= 95.0 else ("A" if weighted_score >= 90.0 else "B")

        # Calculate Pillar Indices
        indices = {
            "ingestion_and_registry_index": (part_results["PART_01_INGESTION"].score + part_results["PART_02_REGISTRY"].score) / 2.0,
            "vector_and_embedding_index": (part_results["PART_03_EMBEDDINGS"].score + part_results["PART_04_VECTORDB"].score) / 2.0,
            "retrieval_and_reranking_index": (part_results["PART_05_RETRIEVAL"].score + part_results["PART_06_RERANKING"].score) / 2.0,
            "context_and_graph_index": (part_results["PART_07_CONTEXT"].score + part_results["PART_08_GRAPH"].score) / 2.0,
            "memory_and_freshness_index": (part_results["PART_09_MEMORY"].score + part_results["PART_11_FRESHNESS"].score) / 2.0,
            "quality_and_drift_index": (part_results["PART_10_QUALITY"].score + part_results["PART_12_DRIFT"].score) / 2.0,
            "security_and_governance_index": part_results["PART_13_SECURITY"].score,
            "optimization_and_scalability_index": (part_results["PART_14_OPTIMIZATION"].score + part_results["PART_16_SCALABILITY"].score) / 2.0,
            "explainability_and_benchmarking_index": (part_results["PART_15_EXPLAINABILITY"].score + part_results["PART_17_BENCHMARKING"].score) / 2.0,
            "executive_dashboard_index": part_results["PART_18_DASHBOARDS"].score,
        }

        return KnowledgeReadinessScorecard(
            parts=part_results,
            indices=indices,
            composite_score=weighted_score,
            grade=grade,
            total_assertions=total_assertions,
            passed_assertions=passed_assertions,
            production_ready=(weighted_score >= 95.0 and passed_assertions == total_assertions),
            total_execution_time_ms=total_elapsed_ms,
        )
