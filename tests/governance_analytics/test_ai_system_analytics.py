"""Tests for AI System Intelligence (Agents, Models, and Workflows)."""

from app.governance.analytics.warehouse.repositories import GovernanceDataWarehouseRepository
from app.governance.analytics.events.normalizers import GovernanceAnalyticsEvent, AnalyticsEventType
from app.governance.analytics.ai_systems.agents import AgentAnalyticsEngine
from app.governance.analytics.ai_systems.models import ModelAnalyticsEngine
from app.governance.analytics.ai_systems.workflows import WorkflowAnalyticsEngine


def test_ai_system_analytics_engines():
    repo = GovernanceDataWarehouseRepository()
    agent_engine = AgentAnalyticsEngine(repo)
    model_engine = ModelAnalyticsEngine(repo)
    workflow_engine = WorkflowAnalyticsEngine(repo)

    # Ingest execution with agent, model, workflow
    repo.insert_event(
        GovernanceAnalyticsEvent(
            tenant_id="tenant_sys",
            event_type=AnalyticsEventType.WORKFLOW_EXECUTION,
            agent_id="agent_doc_parser",
            model_id="gemini-1.5-pro",
            workflow_id="wf_invoice_pipeline",
            cost_usd=0.02,
            latency_ms=800.0,
            risk_score=0.15,
            is_success=True,
        )
    )

    agent_analytics = agent_engine.analyze_agents("tenant_sys")
    assert agent_analytics.total_executions == 1
    assert len(agent_analytics.agent_records) == 1
    assert agent_analytics.agent_records[0].agent_id == "agent_doc_parser"

    model_analytics = model_engine.analyze_models("tenant_sys")
    assert model_analytics.total_invocations == 1
    assert model_analytics.models[0].model_id == "gemini-1.5-pro"

    workflow_analytics = workflow_engine.analyze_workflows("tenant_sys")
    assert workflow_analytics.total_executions == 1
    assert workflow_analytics.workflows[0].workflow_id == "wf_invoice_pipeline"
