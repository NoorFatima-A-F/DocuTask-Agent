"""
Comprehensive Pytest Suite for Phase 13.21 Enterprise AI Knowledge & Context Intelligence Platform (EAKCIP)
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.platform_knowledge.models.schemas import (
    KnowledgeAsset, KnowledgeSource, KnowledgeSourceType, SecurityClassification,
    ContextRetrievalRequest, GraphNode, GraphEdge, EntityType, MemoryTier,
    KnowledgeLifecycleState
)
from app.platform_knowledge.runtime.knowledge_master_orchestrator import knowledge_orchestrator

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_knowledge():
    # Setup test seed assets
    tenant_id = "test-corp"
    knowledge_orchestrator.ingest_and_index_asset(
        tenant_id=tenant_id,
        name="Global Procurement Policy 2026",
        content="All vendor contracts exceeding $50,000 must have dual VP approval and compliance sign-off. Renewal policy is manual review.",
        security_classification=SecurityClassification.INTERNAL,
        author="Procurement Council",
        custom_tags=["procurement", "compliance"]
    )
    knowledge_orchestrator.ingest_and_index_asset(
        tenant_id=tenant_id,
        name="HR Vacation & Benefits Guide",
        content="Standard full-time employees accrue 25 days of annual paid leave and 10 days of sick leave.",
        security_classification=SecurityClassification.INTERNAL,
        author="People Ops",
        custom_tags=["hr", "policy"]
    )
    knowledge_orchestrator.graph_engine.seed_default_enterprise_ontology(tenant_id)
    yield

def test_knowledge_registry_and_ingestion():
    tenant = "test-corp"
    asset = knowledge_orchestrator.ingest_and_index_asset(
        tenant_id=tenant,
        name="Security Architecture Standard",
        content="Zero trust network architecture mandated for all Kubernetes worker pods and API microservices.",
        security_classification=SecurityClassification.CONFIDENTIAL,
        author="SecOps",
        custom_tags=["security", "k8s"]
    )
    assert asset.id is not None
    assert asset.state == KnowledgeLifecycleState.AVAILABLE
    assert "Security" in asset.name
    
    fetched = knowledge_orchestrator.registry.get_asset(asset.id, tenant)
    assert fetched is not None
    assert fetched.name == "Security Architecture Standard"

def test_semantic_vector_search_and_clearance_filtering():
    tenant = "test-corp"
    # Query with CONFIDENTIAL clearance
    results = knowledge_orchestrator.vector_engine.hybrid_search(
        tenant_id=tenant,
        query="procurement approval threshold for vendor contracts",
        top_k=5,
        user_clearance=SecurityClassification.CONFIDENTIAL
    )
    assert len(results) >= 1
    assert "Procurement Policy" in results[0].title
    assert results[0].score > 0.1

    # Query with PUBLIC clearance should filter out CONFIDENTIAL assets
    results_public = knowledge_orchestrator.vector_engine.hybrid_search(
        tenant_id=tenant,
        query="Security Architecture Zero trust",
        top_k=5,
        user_clearance=SecurityClassification.PUBLIC
    )
    # Confidential doc should not be visible to PUBLIC clearance
    titles = [r.title for r in results_public]
    assert "Security Architecture Standard" not in titles

def test_enterprise_knowledge_graph_traversal():
    tenant = "test-corp"
    overview = knowledge_orchestrator.graph_engine.get_graph_overview(tenant)
    assert overview["total_nodes"] >= 4
    assert overview["total_edges"] >= 3
    
    # Query subgraph starting from first node
    start_node = overview["nodes"][0]["id"]
    subgraph = knowledge_orchestrator.graph_engine.query_subgraph(tenant, start_node, max_depth=2)
    assert len(subgraph["nodes"]) >= 1

def test_context_engineering_and_compression():
    tenant = "test-corp"
    req = ContextRetrievalRequest(
        tenant_id=tenant,
        goal="Reconcile vendor invoice exceeding $50k threshold",
        top_k=3,
        include_graph_context=True,
        include_memory=True
    )
    resp = knowledge_orchestrator.retrieve_grounded_context(req)
    assert resp.optimized_context_prompt != ""
    assert "GROUNDED ENTERPRISE CONTEXT" in resp.optimized_context_prompt
    assert resp.total_tokens_estimated > 0
    assert resp.retrieval_latency_ms >= 0

def test_enterprise_memory_tiers():
    tenant = "test-corp"
    mem_short = knowledge_orchestrator.memory_system.store_memory(
        tenant_id=tenant,
        key="active_task_state",
        content="Agent processing invoice #INV-99014",
        tier=MemoryTier.SHORT_TERM
    )
    mem_org = knowledge_orchestrator.memory_system.store_memory(
        tenant_id=tenant,
        key="sop_invoice_reconciliation",
        content="Step 1: Parse OCR, Step 2: Validate PO, Step 3: Match line items",
        tier=MemoryTier.PROCEDURAL
    )
    
    assert mem_short.id is not None
    assert mem_org.id is not None
    
    retrieved = knowledge_orchestrator.memory_system.retrieve_memory(
        tenant_id=tenant,
        query="invoice reconciliation SOP",
        tier=MemoryTier.PROCEDURAL
    )
    assert len(retrieved) >= 1
    assert "sop_invoice_reconciliation" in retrieved[0].key

def test_knowledge_quality_and_conflict_detection():
    tenant = "test-corp"
    # Ingest a second conflicting HR document
    knowledge_orchestrator.ingest_and_index_asset(
        tenant_id=tenant,
        name="HR Vacation Policy Update 2027",
        content="Employees will now accrue 30 days of annual vacation leave.",
        security_classification=SecurityClassification.INTERNAL,
        author="HR Director"
    )
    report = knowledge_orchestrator.quality_intel.generate_quality_report(tenant)
    assert report.total_assets >= 3
    assert len(report.active_conflicts) >= 1
    assert "Vacation" in report.active_conflicts[0].conflict_topic

def test_autonomous_knowledge_optimization():
    tenant = "test-corp"
    res = knowledge_orchestrator.optimizer.run_optimization_cycle(tenant)
    assert res["status"] == "OPTIMIZATION_COMPLETED"
    assert res["healthy_after_optimization"] is True

def test_fastapi_knowledge_endpoints():
    # 1. Search endpoint
    resp = client.post("/api/v1/knowledge/search?tenant_id=test-corp&query=procurement")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)

    # 2. Context retrieval endpoint
    ctx_payload = {
        "tenant_id": "test-corp",
        "goal": "Explain vendor approval policy",
        "top_k": 3
    }
    resp = client.post("/api/v1/knowledge/context", json=ctx_payload)
    assert resp.status_code == 200
    ctx_data = resp.json()
    assert "optimized_context_prompt" in ctx_data

    # 3. Graph overview
    resp = client.get("/api/v1/knowledge/graph/overview?tenant_id=test-corp")
    assert resp.status_code == 200
    assert "total_nodes" in resp.json()

    # 4. Health
    resp = client.get("/api/v1/knowledge/health?tenant_id=test-corp")
    assert resp.status_code == 200
    assert resp.json()["status"] == "OPERATIONAL"

    # 5. Quality Report
    resp = client.get("/api/v1/knowledge/quality/report?tenant_id=test-corp")
    assert resp.status_code == 200
    assert "freshness_index" in resp.json()

    # 6. Evaluation Run
    resp = client.post("/api/v1/knowledge/evaluation/run", json={"tenant_id": "test-corp"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "EVALUATION_PASSED"
