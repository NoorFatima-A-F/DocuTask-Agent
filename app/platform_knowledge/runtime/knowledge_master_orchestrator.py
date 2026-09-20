"""
Knowledge Master Orchestrator
Unified facade orchestrating ingestion, indexing, graph queries, context retrieval, and memory.
"""
from typing import Dict, Any, List, Optional
from ..registry.knowledge_registry import KnowledgeRegistryService
from ..ingestion.ingestion_engine import KnowledgeIngestionEngine
from ..understanding.document_understanding_layer import DocumentUnderstandingLayer
from ..vector.semantic_vector_engine import SemanticVectorEngine
from ..knowledge_graph.enterprise_knowledge_graph import EnterpriseKnowledgeGraph
from ..context.context_engineering_engine import ContextEngineeringEngine
from ..memory.enterprise_memory_system import EnterpriseMemorySystem
from ..quality.knowledge_quality_intelligence import KnowledgeQualityIntelligence
from ..optimization.autonomous_knowledge_optimizer import AutonomousKnowledgeOptimizer
from ..security.knowledge_security_engine import KnowledgeSecurityEngine
from ..models.schemas import (
    KnowledgeAsset, KnowledgeSource, KnowledgeSourceType, SecurityClassification,
    ContextRetrievalRequest, ContextRetrievalResponse, MemoryTier
)

class KnowledgeMasterOrchestrator:
    def __init__(self):
        self.registry = KnowledgeRegistryService()
        self.ingestion = KnowledgeIngestionEngine(self.registry)
        self.understanding = DocumentUnderstandingLayer()
        self.vector_engine = SemanticVectorEngine()
        self.graph_engine = EnterpriseKnowledgeGraph()
        self.memory_system = EnterpriseMemorySystem()
        self.quality_intel = KnowledgeQualityIntelligence(self.registry)
        self.optimizer = AutonomousKnowledgeOptimizer(self.registry, self.quality_intel)
        self.security = KnowledgeSecurityEngine()
        
        # Seed initial enterprise graph
        self.graph_engine.seed_default_enterprise_ontology("default-tenant")

    def ingest_and_index_asset(
        self,
        tenant_id: str,
        name: str,
        content: str,
        source_type: KnowledgeSourceType = KnowledgeSourceType.LOCAL_DOCUMENT,
        security_classification: SecurityClassification = SecurityClassification.INTERNAL,
        author: Optional[str] = None,
        custom_tags: Optional[List[str]] = None
    ) -> KnowledgeAsset:
        # Ingest document
        asset = self.ingestion.ingest_document(
            tenant_id=tenant_id,
            name=name,
            raw_content=content,
            source_type=source_type,
            security_classification=security_classification,
            author=author,
            custom_tags=custom_tags
        )
        # Extract structured understanding
        self.understanding.extract_structured_intelligence(asset)
        # Index into vector engine
        self.vector_engine.index_asset(asset)
        return asset

    def retrieve_grounded_context(self, request: ContextRetrievalRequest) -> ContextRetrievalResponse:
        return ContextEngineeringEngine(
            self.vector_engine,
            self.graph_engine,
            self.memory_system
        ).assemble_grounded_context(request)

    def get_platform_health_overview(self, tenant_id: str) -> Dict[str, Any]:
        assets = self.registry.list_assets(tenant_id)
        sources = self.registry.list_sources(tenant_id)
        graph_ov = self.graph_engine.get_graph_overview(tenant_id)
        quality = self.quality_intel.generate_quality_report(tenant_id)
        memories = self.memory_system.list_all_memories(tenant_id)
        
        return {
            "tenant_id": tenant_id,
            "total_assets": len(assets),
            "total_sources": len(sources),
            "graph_nodes_count": graph_ov["total_nodes"],
            "graph_edges_count": graph_ov["total_edges"],
            "total_memories": len(memories),
            "freshness_index": quality.freshness_index,
            "reliability_score": quality.avg_reliability_score,
            "active_conflicts": len(quality.active_conflicts),
            "status": "OPERATIONAL"
        }

# Global singleton orchestrator
knowledge_orchestrator = KnowledgeMasterOrchestrator()
