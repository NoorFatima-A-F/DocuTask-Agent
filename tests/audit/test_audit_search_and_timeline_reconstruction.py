"""Tests for Multi-Facet Search Engine, Full-Text Token Indexing, and Timeline Reconstruction."""

from app.audit.storage.repository import AuditRepository
from app.audit.search.engine import AuditSearchEngine
from app.audit.search.filters import AuditSearchFilter
from app.audit.core.events import AuditEvent, EventCategory, AuditSeverity, OutcomeType


def test_multi_facet_audit_search():
    repo = AuditRepository()
    engine = AuditSearchEngine(repository=repo)

    for i in range(10):
        repo.record(
            AuditEvent(
                event_id=f"search_evt_{i}",
                event_type="document.extract" if i % 2 == 0 else "workflow.execute",
                category=EventCategory.DATA if i % 2 == 0 else EventCategory.WORKFLOW,
                tenant_id="tenant_search",
                actor_id="user_alice" if i < 5 else "user_bob",
                action="extract" if i % 2 == 0 else "execute",
                resource_type="document" if i % 2 == 0 else "workflow",
                resource_id=f"res_{i}",
                severity=AuditSeverity.HIGH if i == 0 else AuditSeverity.INFO,
                outcome=OutcomeType.FAILURE if i == 9 else OutcomeType.SUCCESS,
                payload_summary=f"Processed invoice #{1000 + i} with vendor Acme",
            )
        )

    # 1. Filter by actor_id
    res1 = engine.search(AuditSearchFilter(tenant_id="tenant_search", actor_id="user_alice"))
    assert res1.matched_count == 5

    # 2. Filter by category
    res2 = engine.search(AuditSearchFilter(tenant_id="tenant_search", category="DATA"))
    assert res2.matched_count == 5

    # 3. Full-text token query
    res3 = engine.search(AuditSearchFilter(tenant_id="tenant_search", query="Acme"))
    assert res3.matched_count == 10


def test_execution_timeline_reconstruction():
    repo = AuditRepository()
    engine = AuditSearchEngine(repository=repo)

    corr_id = "corr_exec_graph_999"

    # Root request
    repo.record(
        AuditEvent(
            event_id="e_req",
            event_type="request.received",
            tenant_id="tenant_tree",
            actor_id="client_app",
            action="receive",
            resource_type="api",
            resource_id="endpoint",
            correlation_id=corr_id,
        )
    )

    # Child workflow
    repo.record(
        AuditEvent(
            event_id="e_wf",
            parent_event_id="e_req",
            event_type="workflow.start",
            tenant_id="tenant_tree",
            actor_id="workflow_engine",
            action="start",
            resource_type="workflow",
            resource_id="invoice_wf",
            correlation_id=corr_id,
        )
    )

    # Child tool call
    repo.record(
        AuditEvent(
            event_id="e_tool",
            parent_event_id="e_wf",
            event_type="tool.invoke",
            tenant_id="tenant_tree",
            actor_id="agent_1",
            action="invoke",
            resource_type="tool",
            resource_id="ocr_reader",
            correlation_id=corr_id,
        )
    )

    graph = engine.reconstruct_timeline(correlation_id=corr_id, tenant_id="tenant_tree")
    assert graph.total_events == 3
    assert len(graph.root_nodes) == 1
    assert graph.root_nodes[0].event_id == "e_req"
    assert len(graph.root_nodes[0].children) == 1
    assert graph.root_nodes[0].children[0].event_id == "e_wf"
    assert len(graph.root_nodes[0].children[0].children) == 1
    assert graph.root_nodes[0].children[0].children[0].event_id == "e_tool"
