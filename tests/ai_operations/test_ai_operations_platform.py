"""
Phase 13.17: Comprehensive Test Suite for Autonomous AI Operations Center (AAIOC)
Tests Telemetry, Continuous Evaluation, Root Cause Debugging, Pareto Model Routing,
Predictive Intelligence, A/B Canary Experimentation, HITL Improvements, AI Governance, and REST APIs.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.runtime.ai_operations import (
    TelemetryCollector,
    MetricAggregator,
    TelemetryEngine,
    EvaluationMetricsCalculator,
    LLMJudge,
    EvaluationEngine,
    FailureClassifier,
    DebuggingEngine,
    ModelCatalog,
    ModelRouter,
    PromptOptimizer,
    CostOptimizer,
    FailurePredictionEngine,
    ExperimentEngine,
    ImprovementEngine,
    ComplianceMonitor,
    AIGovernanceEngine,
    AIOperationsRuntime,
    SpanType,
    SpanStatus,
    AgentHealthStatus,
    FailureCategory,
    ProposalStatus,
)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def runtime():
    return AIOperationsRuntime()


# -----------------------------------------------------------------------------
# 1. Telemetry & Distributed Tracing Tests
# -----------------------------------------------------------------------------

def test_telemetry_trace_and_spans():
    collector = TelemetryCollector()
    trace = collector.start_trace("session_123", "agent_chief_architect", "System Refactor")
    assert trace.trace_id.startswith("trace_")
    assert trace.agent_id == "agent_chief_architect"

    span1 = collector.start_span(
        trace_id=trace.trace_id,
        name="LLM Context Prompt Generation",
        span_type=SpanType.LLM_CALL,
        agent_id="agent_chief_architect",
    )
    assert span1.span_id.startswith("span_")
    
    ended_span = collector.end_span(
        span_id=span1.span_id,
        status=SpanStatus.OK,
        token_usage={"prompt_tokens": 1200, "completion_tokens": 400, "total_tokens": 1600},
        cost_usd=0.0035,
    )
    assert ended_span is not None
    assert ended_span.status == SpanStatus.OK
    assert ended_span.duration_ms >= 0.0

    completed_trace = collector.end_trace(trace.trace_id, SpanStatus.OK)
    assert completed_trace.total_prompt_tokens == 1200
    assert completed_trace.total_completion_tokens == 400
    assert completed_trace.total_cost_usd == 0.0035


def test_metric_aggregator_percentiles():
    collector = TelemetryCollector()
    for i in range(10):
        t = collector.start_trace(f"sess_{i}", "agent_scientist", "Hypothesis Test")
        s = collector.start_span(t.trace_id, "Eval Step", SpanType.AGENT_RUN, "agent_scientist")
        collector.end_span(s.span_id, SpanStatus.OK, token_usage={"prompt_tokens": 500, "completion_tokens": 200, "total_tokens": 700})
        collector.end_trace(t.trace_id, SpanStatus.OK)

    telemetry = MetricAggregator.aggregate_agent_telemetry(
        "agent_scientist", "Chief Scientist", "Hypothesis Discovery", collector.list_traces()
    )
    assert telemetry.agent_id == "agent_scientist"
    assert telemetry.total_invocations == 10
    assert telemetry.success_rate == 1.0
    assert telemetry.error_rate == 0.0
    assert telemetry.p95_latency_ms >= 0.0
    assert telemetry.health_status == AgentHealthStatus.HEALTHY


def test_telemetry_engine_fleet_overview():
    engine = TelemetryEngine()
    overview = engine.get_overview_metrics()
    assert "total_agents" in overview
    assert overview["total_agents"] >= 5
    assert overview["fleet_health_score"] >= 0.0
    assert overview["sla_compliance_pct"] >= 90.0


# -----------------------------------------------------------------------------
# 2. Evaluation Subsystem Tests
# -----------------------------------------------------------------------------

def test_evaluation_metrics_calculations():
    # Grounding & Hallucination
    grounding = EvaluationMetricsCalculator.calculate_grounding_score(["fact1", "fact2"], ["fact1"])
    assert grounding == 0.5
    hallucination = EvaluationMetricsCalculator.calculate_hallucination_index(grounding)
    assert hallucination == 0.5

    # Tool efficiency
    tool_eff = EvaluationMetricsCalculator.calculate_tool_efficiency(tool_calls_count=1)
    assert tool_eff == 1.0
    tool_eff_excessive = EvaluationMetricsCalculator.calculate_tool_efficiency(tool_calls_count=5)
    assert tool_eff_excessive < 1.0

    # Composite Score
    composite = EvaluationMetricsCalculator.calculate_composite_score(
        task_success=1.0,
        accuracy=0.95,
        grounding=0.90,
        safety=1.0,
        tool_efficiency=0.90,
        llm_judge=0.92,
    )
    assert 0.90 <= composite <= 1.0


def test_llm_judge_and_evaluation_engine():
    judge_result = LLMJudge.evaluate("agent_doc_extractor", "Extract invoice", "Invoice total: $500")
    assert "judge_score" in judge_result
    assert 0.0 <= judge_result["judge_score"] <= 1.0
    assert len(judge_result["critique"]) > 10

    eval_engine = EvaluationEngine()
    history = eval_engine.get_evaluation_history(limit=10)
    assert len(history) > 0
    assert history[0].composite_quality_score >= 0.0


# -----------------------------------------------------------------------------
# 3. Debugging & Root Cause Analysis Tests
# -----------------------------------------------------------------------------

def test_failure_classification():
    collector = TelemetryCollector()
    trace = collector.start_trace("sess_err", "agent_doc_extractor", "OCR Extract")
    s = collector.start_span(trace.trace_id, "OCR API Call", SpanType.TOOL_EXECUTION, "agent_doc_extractor")
    collector.end_span(s.span_id, status=SpanStatus.TIMEOUT, error_message="Downstream endpoint timeout 5000ms")
    collector.end_trace(trace.trace_id, status=SpanStatus.TIMEOUT)

    analysis = FailureClassifier.classify_failure(trace)
    assert analysis.category == FailureCategory.TOOL_TIMEOUT
    assert "timeout" in analysis.root_cause_summary.lower()
    assert len(analysis.critical_path) > 0
    assert len(analysis.suggested_remediation) > 0


def test_debugging_engine():
    engine = DebuggingEngine()
    logs = engine.get_failure_logs()
    assert len(logs) >= 3
    assert logs[0].category in [
        FailureCategory.TOOL_TIMEOUT,
        FailureCategory.TOOL_SCHEMA_VIOLATION,
        FailureCategory.RECURSIVE_LOOP,
    ]


# -----------------------------------------------------------------------------
# 4. Optimization & Model Routing Tests
# -----------------------------------------------------------------------------

def test_pareto_model_router():
    # Balanced task
    decision = ModelRouter.route_task(
        task_id="task_test_01",
        estimated_prompt_tokens=1500,
        estimated_completion_tokens=500,
        weight_quality=0.50,
        weight_latency=0.30,
        weight_cost=0.20,
    )
    assert decision.selected_model in ModelCatalog.PROFILES
    assert decision.pareto_score >= 0.0
    assert len(decision.fallback_models) >= 1

    # Heavy cost constraint
    decision_cost = ModelRouter.route_task(
        task_id="task_test_cost",
        estimated_prompt_tokens=1000,
        estimated_completion_tokens=200,
        weight_quality=0.10,
        weight_latency=0.10,
        weight_cost=0.80,
    )
    assert decision_cost.selected_model in ["gemini-2.0-flash-lite", "gemini-2.0-flash"]


def test_prompt_optimizer_and_cost():
    prompt_opt = PromptOptimizer()
    prompts = prompt_opt.get_all_prompts()
    assert len(prompts) >= 2

    mutated = prompt_opt.propose_prompt_refinement(
        "agent_scientist", "Enforce empirical falsification criteria"
    )
    assert mutated.agent_id == "agent_scientist"
    assert "empirical falsification" in mutated.system_instruction

    telemetry = [
        MetricAggregator.aggregate_agent_telemetry("agent_chief_architect", "Chief Architect", "Architecture", [])
    ]
    cost_data = CostOptimizer.calculate_cost_analytics(telemetry)
    assert "projected_monthly_spend_usd" in cost_data
    assert len(cost_data["savings_recommendations"]) >= 1


# -----------------------------------------------------------------------------
# 5. Predictive Intelligence Tests
# -----------------------------------------------------------------------------

def test_failure_prediction_engine():
    engine = FailurePredictionEngine()
    preds = engine.get_active_predictions()
    assert len(preds) >= 2

    # High error telemetry
    collector = TelemetryCollector()
    t = collector.start_trace("err_t", "agent_risk_auditor", "Audit")
    collector.end_trace(t.trace_id, SpanStatus.ERROR)
    telemetry = MetricAggregator.aggregate_agent_telemetry("agent_risk_auditor", "Risk Agent", "Audit", collector.list_traces())

    pred = engine.analyze_agent_risk(telemetry)
    assert pred["agent_id"] == "agent_risk_auditor"
    assert "probability" in pred
    assert pred["severity"] in ["LOW", "MEDIUM", "HIGH"]


# -----------------------------------------------------------------------------
# 6. Improvement & A/B Canary Tests
# -----------------------------------------------------------------------------

def test_experiment_engine_stat_sig():
    exp_engine = ExperimentEngine()
    exp = exp_engine.run_experiment(
        name="Canary Benchmark Test",
        agent_id="agent_chief_architect",
        control_version="v1.0.0",
        candidate_version="v1.1.0",
        sample_size=100,
    )
    assert exp.sample_size == 100
    assert 0.0 <= exp.control_success_rate <= 1.0
    assert 0.0 <= exp.candidate_success_rate <= 1.0
    assert exp.p_value >= 0.0
    assert exp.effect_size_cohen_d is not None


def test_improvement_proposals_and_hitl_lifecycle():
    imp_engine = ImprovementEngine()
    props = imp_engine.list_proposals()
    assert len(props) >= 1

    # Create proposal
    prop = imp_engine.create_proposal_from_analysis(
        agent_id="agent_doc_extractor",
        title="Upgrade OCR Extraction Pipeline",
        description="Add secondary fallbacks",
        proposal_type="TOOL_ROUTING",
        changes={"fallback_enabled": True},
        diff_summary="+ Fallback enabled",
        expected_quality_delta=0.07,
    )
    assert prop.status == ProposalStatus.PENDING_HITL_APPROVAL

    # Approve (HITL)
    approved = imp_engine.approve_proposal(prop.proposal_id, approved_by="Security Officer")
    assert approved.status == ProposalStatus.APPROVED
    assert approved.approved_by == "Security Officer"

    # Deploy
    deployed = imp_engine.deploy_proposal(prop.proposal_id)
    assert deployed.status == ProposalStatus.DEPLOYED


# -----------------------------------------------------------------------------
# 7. Governance & Compliance Tests
# -----------------------------------------------------------------------------

def test_compliance_monitor_pii_sanitization():
    raw_prompt = "Contact user at john.doe@enterprise.com with secret token api_key: 'abc123456789012345'."
    redacted, detected = ComplianceMonitor.scan_and_redact(raw_prompt)
    assert "EMAIL" in detected
    assert "API_KEY" in detected
    assert "john.doe@enterprise.com" not in redacted
    assert "[REDACTED_EMAIL]" in redacted
    assert "[REDACTED_API_KEY]" in redacted


def test_ai_governance_engine_audit_log():
    gov_engine = AIGovernanceEngine()
    logs = gov_engine.get_audit_logs()
    assert len(logs) >= 3

    entry = gov_engine.log_event(
        event_type="POLICY_VERIFICATION",
        actor="sentinel_bot",
        action_summary="Audited agent output compliance.",
        compliance_passed=True,
    )
    assert entry.signature_hash is not None
    assert len(entry.signature_hash) == 64  # SHA-256


# -----------------------------------------------------------------------------
# 8. Master Runtime Cycle Test
# -----------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_full_operations_runtime_cycle(runtime):
    cycle_res = await runtime.execute_operations_cycle(target_agent_id="agent_chief_architect")
    assert cycle_res["cycle_status"] == "COMPLETED"
    assert cycle_res["agent_id"] == "agent_chief_architect"
    assert "telemetry_observed" in cycle_res
    assert "evaluation_result" in cycle_res
    assert "model_route_decision" in cycle_res
    assert "experiment_result" in cycle_res
    assert "improvement_proposal" in cycle_res
    assert "audit_record" in cycle_res


# -----------------------------------------------------------------------------
# 9. FastAPI Endpoints Integration Tests
# -----------------------------------------------------------------------------

def test_api_operations_overview(client):
    res = client.get("/api/v1/ai_operations/overview")
    assert res.status_code == 200
    data = res.json()
    assert "total_agents" in data
    assert "fleet_health_score" in data


def test_api_telemetry_and_traces(client):
    res_agents = client.get("/api/v1/ai_operations/telemetry/agents")
    assert res_agents.status_code == 200
    agents = res_agents.json()
    assert len(agents) >= 5

    res_traces = client.get("/api/v1/ai_operations/telemetry/traces?limit=10")
    assert res_traces.status_code == 200
    traces = res_traces.json()
    assert len(traces) > 0

    trace_id = traces[0]["trace_id"]
    res_single = client.get(f"/api/v1/ai_operations/telemetry/traces/{trace_id}")
    assert res_single.status_code == 200
    assert res_single.json()["trace_id"] == trace_id


def test_api_evaluation_and_optimization(client):
    res_eval = client.get("/api/v1/ai_operations/evaluation/results")
    assert res_eval.status_code == 200
    assert len(res_eval.json()) > 0

    route_req = {
        "task_id": "task_api_01",
        "estimated_prompt_tokens": 1200,
        "estimated_completion_tokens": 400,
        "weight_quality": 0.6,
        "weight_latency": 0.2,
        "weight_cost": 0.2,
    }
    res_route = client.post("/api/v1/ai_operations/optimization/model-route", json=route_req)
    assert res_route.status_code == 200
    assert "selected_model" in res_route.json()

    res_prompts = client.get("/api/v1/ai_operations/optimization/prompts")
    assert res_prompts.status_code == 200
    assert len(res_prompts.json()) > 0


def test_api_cost_and_failures(client):
    res_cost = client.get("/api/v1/ai_operations/cost/analytics")
    assert res_cost.status_code == 200
    assert "total_tokens_consumed" in res_cost.json()

    res_fails = client.get("/api/v1/ai_operations/debugging/failures")
    assert res_fails.status_code == 200
    assert len(res_fails.json()) > 0


def test_api_improvement_hitl_and_experiments(client):
    res_props = client.get("/api/v1/ai_operations/improvement/proposals")
    assert res_props.status_code == 200
    props = res_props.json()
    assert len(props) > 0

    prop_id = props[0]["proposal_id"]
    res_approve = client.post(
        f"/api/v1/ai_operations/improvement/proposals/{prop_id}/approve",
        json={"actor": "Enterprise Admin", "reason": "Verified performance metrics."},
    )
    assert res_approve.status_code == 200
    assert res_approve.json()["status"] == "APPROVED"

    res_exps = client.get("/api/v1/ai_operations/experiments")
    assert res_exps.status_code == 200
    assert len(res_exps.json()) > 0

    exp_req = {
        "name": "API Canary Run",
        "agent_id": "agent_chief_architect",
        "control_version": "v1.0.0",
        "candidate_version": "v1.1.0",
        "sample_size": 50,
    }
    res_run_exp = client.post("/api/v1/ai_operations/experiments/run", json=exp_req)
    assert res_run_exp.status_code == 200
    assert res_run_exp.json()["sample_size"] == 50


def test_api_governance_and_cycle(client):
    res_gov = client.get("/api/v1/ai_operations/governance/audit-logs")
    assert res_gov.status_code == 200
    assert len(res_gov.json()) > 0

    res_cycle = client.post("/api/v1/ai_operations/runtime/cycle", json={"agent_id": "agent_chief_architect"})
    assert res_cycle.status_code == 200
    assert res_cycle.json()["cycle_status"] == "COMPLETED"
